#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
N:N Intent-to-Template 매핑 시스템
"""

from typing import Dict, List, Optional, Tuple
from intent_similarity_classifier import similarity_classifier
import os
import json

class TemplateMapper:
    """
    N:N Intent-to-Template 매핑 시스템
    """
    
    def __init__(self, templates_dir: str = "templates"):
        """초기화"""
        self.templates_dir = templates_dir
        
        # 자동으로 템플릿 매핑 생성
        self.intent_template_mapping = self._auto_load_templates()
        
        # Fallback 템플릿 정의
        self.fallback_templates = {
            "general": "unknown.txt",
            "code_related": "code_run.txt"
        }
        
        # 템플릿 우선순위 정의 (자동 생성된 템플릿에 맞게 조정)
        self.template_priority = self._generate_template_priority()
        
        print(f"자동 로드된 템플릿 매핑: {len(self.intent_template_mapping)} 개의 intent에 대해 {sum(len(templates) for templates in self.intent_template_mapping.values())} 개의 템플릿")
        
        # 디버깅: 모든 intent-to-template 매핑 출력
        print("\n=== 의도-템플릿 매핑 디버깅 정보 ===")
        for k, v in self.intent_template_mapping.items():
            print(f"[{k}] → {v}")
        print("=" * 50)
        
        # 템플릿 파일 존재 여부 확인
        print("\n=== 템플릿 파일 존재 여부 확인 ===")
        missing_files = []
        for file_list in self.intent_template_mapping.values():
            for file in file_list:
                file_path = os.path.join(self.templates_dir, file)
                if os.path.exists(file_path):
                    print(f"✅ {file} → Exists")
                else:
                    print(f"❌ {file} → Missing")
                    missing_files.append(file)
        
        if missing_files:
            print(f"\n⚠️  경고: {len(missing_files)}개의 파일이 누락되었습니다:")
            for file in missing_files:
                print(f"   - {file}")
        else:
            print(f"\n✅ 모든 템플릿 파일이 정상적으로 존재합니다.")
        print("=" * 50)
    
    def _auto_load_templates(self) -> Dict[str, List[str]]:
        """
        templates 폴더를 스캔하여 자동으로 템플릿 매핑을 생성합니다.
        
        Returns:
            Dict[str, List[str]]: intent -> 템플릿 파일명 리스트 매핑
        """
        mapping = {}
        
        if not os.path.exists(self.templates_dir):
            print(f"경고: {self.templates_dir} 폴더가 존재하지 않습니다.")
            return mapping
        
        # 모든 .txt 파일을 재귀적으로 찾기
        for root, dirs, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith('.txt'):
                    # 상대 경로 계산
                    rel_path = os.path.relpath(os.path.join(root, file), self.templates_dir)
                    
                    # 파일명에서 .txt 제거하여 intent 키 생성
                    intent_key = os.path.splitext(file)[0]
                    
                    # 하위 폴더가 있는 경우 intent 키에 포함
                    if root != self.templates_dir:
                        # templates/proposal/ai/ai.txt -> proposal_ai_ai
                        rel_dir = os.path.relpath(root, self.templates_dir)
                        intent_key = f"{rel_dir.replace(os.sep, '_')}_{intent_key}"
                    
                    # 매핑에 추가
                    if intent_key not in mapping:
                        mapping[intent_key] = []
                    
                    if rel_path not in mapping[intent_key]:
                        mapping[intent_key].append(rel_path)
        
        # 특별한 매핑 규칙 추가 (기존 로직과의 호환성)
        self._add_special_mappings(mapping)
        
        return mapping
    
    def _add_special_mappings(self, mapping: Dict[str, List[str]]):
        """
        특별한 매핑 규칙을 추가합니다 (기존 로직과의 호환성).
        """
        # summary 관련 통합 매핑
        if "summary" in mapping or "summary_meeting" in mapping:
            summary_templates = []
            if "summary" in mapping:
                summary_templates.extend(mapping["summary"])
            if "summary_meeting" in mapping:
                summary_templates.extend(mapping["summary_meeting"])
            
            mapping["summary"] = list(set(summary_templates))
        
        # self_intro 관련 통합 매핑
        if "self_intro" in mapping or "self_intro_engineer" in mapping:
            intro_templates = []
            if "self_intro" in mapping:
                intro_templates.extend(mapping["self_intro"])
            if "self_intro_engineer" in mapping:
                intro_templates.extend(mapping["self_intro_engineer"])
            
            mapping["self_intro"] = list(set(intro_templates))
        
        # customer_reply 관련 통합 매핑
        if "customer_reply" in mapping or "customer_reply_apology" in mapping:
            reply_templates = []
            if "customer_reply" in mapping:
                reply_templates.extend(mapping["customer_reply"])
            if "customer_reply_apology" in mapping:
                reply_templates.extend(mapping["customer_reply_apology"])
            
            mapping["customer_reply"] = list(set(reply_templates))
        
        # proposal 관련 통합 매핑
        proposal_templates = []
        for key in mapping.keys():
            if key.startswith("proposal_"):
                proposal_templates.extend(mapping[key])
        
        if proposal_templates:
            mapping["grant_proposal"] = list(set(proposal_templates))
        
        # business_plan 관련 매핑 (fallback용)
        if "business_plan" in mapping:
            business_templates = mapping["business_plan"].copy()
            # proposal 템플릿들도 business_plan에 추가
            if "grant_proposal" in mapping:
                business_templates.extend(mapping["grant_proposal"])
            mapping["business_plan"] = list(set(business_templates))
        
        # general_request 관련 매핑 (fallback용)
        general_templates = []
        if "unknown" in mapping:
            general_templates.extend(mapping["unknown"])
        if "summary" in mapping:
            general_templates.extend(mapping["summary"])
        if "self_intro" in mapping:
            general_templates.extend(mapping["self_intro"])
        
        if general_templates:
            mapping["general_request"] = list(set(general_templates))
    
    def _generate_template_priority(self) -> Dict[str, int]:
        """
        자동 로드된 템플릿에 맞는 우선순위를 생성합니다.
        
        Returns:
            Dict[str, int]: 템플릿 파일명 -> 우선순위 매핑
        """
        priority = {}
        base_priority = 1
        
        # 모든 템플릿에 기본 우선순위 할당
        for templates in self.intent_template_mapping.values():
            for template in templates:
                if template not in priority:
                    priority[template] = base_priority
                    base_priority += 1
        
        # 특별한 우선순위 설정
        special_priorities = {
            "unknown.txt": 999,  # 가장 낮은 우선순위
            "code_run.txt": 998,
            "business_plan.txt": 1,  # business_plan 전용 템플릿
            "marketing_copy.txt": 1,  # marketing_copy 전용 템플릿
        }
        
        for template, pri in special_priorities.items():
            if template in priority:
                priority[template] = pri
        
        return priority
    
    def get_templates_for_intent(self, intent: str) -> List[str]:
        """
        특정 intent에 대한 템플릿 목록을 반환합니다.
        
        Args:
            intent: 의도
            
        Returns:
            List[str]: 템플릿 파일명 리스트
        """
        return self.intent_template_mapping.get(intent, [])
    
    def get_best_template_for_intent(self, intent: str, utterance: str = "") -> Optional[str]:
        """
        특정 intent에 대한 최적의 템플릿을 반환합니다.
        
        Args:
            intent: 의도
            utterance: 사용자 발화 (선택적, 유사도 계산용)
            
        Returns:
            Optional[str]: 최적의 템플릿 파일명
        """
        templates = self.get_templates_for_intent(intent)
        
        if not templates:
            return None
        
        # 템플릿이 하나뿐이면 바로 반환
        if len(templates) == 1:
            return templates[0]
        
        # 여러 템플릿이 있는 경우 우선순위 기반 선택
        if utterance:
            # 유사도 기반 선택
            return self._select_template_by_similarity(templates, utterance)
        else:
            # 우선순위 기반 선택
            return self._select_template_by_priority(templates)
    
    def _select_template_by_priority(self, templates: List[str]) -> str:
        """우선순위 기반으로 템플릿을 선택합니다."""
        best_template = templates[0]
        best_priority = self.template_priority.get(best_template, 999)
        
        for template in templates[1:]:
            priority = self.template_priority.get(template, 999)
            if priority < best_priority:
                best_template = template
                best_priority = priority
        
        return best_template
    
    def _select_template_by_similarity(self, templates: List[str], utterance: str) -> str:
        """유사도 기반으로 템플릿을 선택합니다."""
        # 템플릿 내용을 임시로 로드하여 유사도 계산
        # 실제 구현에서는 템플릿 메타데이터나 키워드를 활용할 수 있음
        return self._select_template_by_priority(templates)
    
    def get_fallback_template(self, utterance: str = "") -> str:
        """
        Fallback 템플릿을 반환합니다.
        
        Args:
            utterance: 사용자 발화 (선택적)
            
        Returns:
            str: Fallback 템플릿 파일명
        """
        # 코드 관련 키워드가 있으면 코드 템플릿 반환
        code_keywords = ["코드", "프로그램", "실행", "개발", "프로그래밍", "알고리즘"]
        if any(keyword in utterance for keyword in code_keywords):
            return self.fallback_templates["code_related"]
        
        return self.fallback_templates["general"]
    
    def get_similar_intent_templates(self, utterance: str, top_k: int = 3) -> List[Tuple[str, float, str]]:
        """
        입력 문장과 유사한 intent의 템플릿들을 반환합니다.
        
        Args:
            utterance: 사용자 발화
            top_k: 반환할 상위 intent 개수
            
        Returns:
            List[Tuple[str, float, str]]: (intent, 유사도, 템플릿) 리스트
        """
        # 유사한 intent들 찾기
        similar_intents = similarity_classifier.get_similar_intents(utterance, top_k)
        
        results = []
        for intent, similarity in similar_intents:
            templates = self.get_templates_for_intent(intent)
            if templates:
                best_template = self.get_best_template_for_intent(intent, utterance)
                results.append((intent, similarity, best_template))
        
        return results
    
    def add_intent_template_mapping(self, intent: str, template: str):
        """새로운 intent-template 매핑을 추가합니다."""
        if intent not in self.intent_template_mapping:
            self.intent_template_mapping[intent] = []
        
        if template not in self.intent_template_mapping[intent]:
            self.intent_template_mapping[intent].append(template)
    
    def remove_intent_template_mapping(self, intent: str, template: str):
        """intent-template 매핑을 제거합니다."""
        if intent in self.intent_template_mapping:
            if template in self.intent_template_mapping[intent]:
                self.intent_template_mapping[intent].remove(template)
    
    def get_all_mappings(self) -> Dict[str, List[str]]:
        """모든 intent-template 매핑을 반환합니다."""
        return self.intent_template_mapping.copy()

# 전역 인스턴스 생성
template_mapper = TemplateMapper() 