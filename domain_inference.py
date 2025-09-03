#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
네이밍 기반 도메인 추론 시스템
"""

import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from intent_similarity_classifier import similarity_classifier

class DomainInference:
    """
    네이밍 기반 도메인 추론 시스템
    """
    
    def __init__(self):
        """초기화"""
        # 도메인 키워드 사전
        self.domain_keywords = {
            "ai": [
                "AI", "인공지능", "머신러닝", "딥러닝", "ML", "DL", "알고리즘", "모델",
                "ChatGPT", "GPT", "LLM", "대화형AI", "생성AI", "추천시스템",
                "컴퓨터비전", "자연어처리", "NLP", "CV", "로봇", "자율주행"
            ],
            "government": [
                "정부", "공공", "행정", "정책", "법령", "규정", "지자체", "중앙정부",
                "부처", "청", "원", "위원회", "공무원", "행정서비스", "전자정부",
                "스마트시티", "디지털정부", "공공데이터", "오픈데이터"
            ],
            "private": [
                "기업", "회사", "스타트업", "벤처", "투자", "금융", "은행", "보험",
                "증권", "펀드", "벤처캐피탈", "엔젤투자", "IPO", "M&A", "합병",
                "사업화", "상용화", "수익화", "비즈니스모델", "수익모델"
            ],
            "education": [
                "교육", "학습", "강의", "수업", "학교", "대학", "대학교", "학원",
                "온라인교육", "이러닝", "모바일러닝", "플립러닝", "블렌디드러닝",
                "교육과정", "커리큘럼", "교재", "학습자료", "튜토리얼", "가이드"
            ],
            "healthcare": [
                "의료", "건강", "병원", "의원", "약국", "제약", "바이오", "생명공학",
                "진단", "치료", "예방", "웰빙", "헬스케어", "디지털헬스", "원격의료",
                "의료AI", "정밀의료", "개인화의료", "유전체", "바이오마커"
            ],
            "finance": [
                "금융", "은행", "보험", "증권", "투자", "펀드", "대출", "예금",
                "핀테크", "블록체인", "암호화폐", "가상화폐", "디지털자산",
                "금융서비스", "모바일뱅킹", "온라인뱅킹", "결제", "송금"
            ],
            "environment": [
                "환경", "기후", "친환경", "그린", "탄소", "에너지", "재생에너지",
                "태양광", "풍력", "수소", "전기차", "배터리", "폐기물", "재활용",
                "지속가능", "ESG", "탄소중립", "기후변화", "대기질", "수질"
            ],
            "technology": [
                "기술", "IT", "소프트웨어", "하드웨어", "플랫폼", "앱", "웹",
                "모바일", "클라우드", "빅데이터", "IoT", "5G", "6G", "네트워크",
                "보안", "암호화", "블록체인", "메타버스", "AR", "VR", "XR"
            ]
        }
        
        # 신조어 및 고유명사 사전
        self.neologism_dict = {
            "프롬프트OS": {
                "description": "프롬프트 기반 운영체제 또는 프롬프트 관리 시스템",
                "domain": "technology",
                "related_intents": ["education_content", "marketing_copy"]
            },
            "ChatGPT": {
                "description": "OpenAI의 대화형 인공지능 모델",
                "domain": "ai",
                "related_intents": ["education_content", "marketing_copy"]
            },
            "스마트시티": {
                "description": "ICT 기술을 활용한 지능형 도시",
                "domain": "government",
                "related_intents": ["policy_brief", "grant_proposal"]
            },
            "메타버스": {
                "description": "가상과 현실이 융합된 3차원 가상세계",
                "domain": "technology",
                "related_intents": ["marketing_copy", "startup_pitch"]
            },
            "핀테크": {
                "description": "금융과 기술의 결합",
                "domain": "finance",
                "related_intents": ["startup_pitch", "grant_proposal"]
            },
            "바이오": {
                "description": "생명공학 기술",
                "domain": "healthcare",
                "related_intents": ["grant_proposal", "startup_pitch"]
            }
        }
        
        # 도메인별 관련 intent 매핑
        self.domain_intent_mapping = {
            "ai": ["startup_pitch", "grant_proposal", "education_content"],
            "government": ["policy_brief", "grant_proposal"],
            "private": ["startup_pitch", "marketing_copy"],
            "education": ["education_content", "summary"],
            "healthcare": ["grant_proposal", "startup_pitch"],
            "finance": ["startup_pitch", "grant_proposal"],
            "environment": ["policy_brief", "grant_proposal"],
            "technology": ["startup_pitch", "marketing_copy", "education_content"]
        }
    
    def infer_domain(self, utterance: str) -> Tuple[str, float, Dict]:
        """
        입력 문장에서 도메인을 추론합니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            Tuple[str, float, Dict]: (추론된 도메인, 신뢰도, 추가 정보)
        """
        # 1. 신조어/고유명사 검사
        neologism_info = self._check_neologism(utterance)
        if neologism_info:
            return neologism_info["domain"], 0.9, neologism_info
        
        # 2. 키워드 기반 도메인 추론
        domain_scores = self._calculate_domain_scores(utterance)
        
        if not domain_scores:
            return "general", 0.0, {}
        
        # 가장 높은 점수의 도메인 선택
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        
        # 신뢰도 계산 (점수가 0.3 이상일 때만 유효)
        confidence = min(best_domain[1] / 10.0, 1.0) if best_domain[1] > 0.3 else 0.0
        
        return best_domain[0], confidence, {"scores": domain_scores}
    
    def _check_neologism(self, utterance: str) -> Optional[Dict]:
        """신조어/고유명사를 검사합니다."""
        for term, info in self.neologism_dict.items():
            if term.lower() in utterance.lower():
                return info
        return None
    
    def _calculate_domain_scores(self, utterance: str) -> Dict[str, float]:
        """키워드 기반으로 도메인 점수를 계산합니다."""
        scores = {}
        utterance_lower = utterance.lower()
        
        for domain, keywords in self.domain_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in utterance_lower:
                    # 키워드 길이에 따라 가중치 부여
                    weight = len(keyword) / 10.0
                    score += weight
            
            if score > 0:
                scores[domain] = score
        
        return scores
    
    def get_related_intents(self, domain: str) -> List[str]:
        """도메인과 관련된 intent들을 반환합니다."""
        return self.domain_intent_mapping.get(domain, [])
    
    def enhance_intent_classification(self, utterance: str, original_intent: str) -> Tuple[str, float]:
        """
        도메인 정보를 활용하여 intent 분류를 개선합니다.
        
        Args:
            utterance: 사용자 발화
            original_intent: 원래 분류된 intent
            
        Returns:
            Tuple[str, float]: (개선된 intent, 신뢰도)
        """
        # 도메인 추론
        domain, domain_confidence, domain_info = self.infer_domain(utterance)
        
        # 도메인 신뢰도가 낮으면 원래 intent 유지
        if domain_confidence < 0.3:
            return original_intent, 0.5
        
        # 도메인과 관련된 intent들
        related_intents = self.get_related_intents(domain)
        
        # 원래 intent가 도메인과 관련이 있으면 신뢰도 증가
        if original_intent in related_intents:
            return original_intent, min(0.9, 0.5 + domain_confidence)
        
        # 원래 intent가 도메인과 관련이 없으면 유사도 기반 재분류 시도
        if original_intent == "unknown" or original_intent not in related_intents:
            # 도메인 관련 intent들 중에서 유사도 기반 선택
            best_intent = None
            best_similarity = 0.0
            
            for intent in related_intents:
                similarity = similarity_classifier.classify_by_similarity(utterance)[1]
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_intent = intent
            
            if best_intent and best_similarity > 0.6:
                return best_intent, best_similarity * domain_confidence
        
        return original_intent, 0.5
    
    def get_domain_context(self, domain: str) -> Dict:
        """도메인별 컨텍스트 정보를 반환합니다."""
        context_templates = {
            "ai": {
                "audience": "AI 전문가, 기술 연구자, 투자자",
                "tone": "전문적이고 기술적",
                "focus": "기술적 혁신성과 실용성"
            },
            "government": {
                "audience": "정부 관계자, 정책 입안자, 공무원",
                "tone": "공식적이고 신뢰할 수 있는",
                "focus": "공공 가치와 정책 효과성"
            },
            "private": {
                "audience": "투자자, 기업 임원, 비즈니스 파트너",
                "tone": "비즈니스 중심적이고 설득력 있는",
                "focus": "수익성과 시장 잠재력"
            },
            "education": {
                "audience": "학생, 교육자, 학습자",
                "tone": "교육적이고 이해하기 쉬운",
                "focus": "학습 효과와 교육 가치"
            },
            "healthcare": {
                "audience": "의료진, 환자, 의료기관",
                "tone": "전문적이고 신뢰할 수 있는",
                "focus": "의료 효과성과 안전성"
            },
            "finance": {
                "audience": "금융 전문가, 투자자, 고객",
                "tone": "전문적이고 신뢰할 수 있는",
                "focus": "금융 안정성과 수익성"
            },
            "environment": {
                "audience": "환경 전문가, 정책 입안자, 일반 시민",
                "tone": "환경 친화적이고 지속가능한",
                "focus": "환경 보호와 지속가능성"
            },
            "technology": {
                "audience": "기술 전문가, 개발자, 일반 사용자",
                "tone": "혁신적이고 접근하기 쉬운",
                "focus": "기술적 혁신과 사용자 경험"
            }
        }
        
        return context_templates.get(domain, {
            "audience": "일반 사용자",
            "tone": "중립적",
            "focus": "일반적인 목적"
        })

# 전역 인스턴스 생성
domain_inference = DomainInference() 