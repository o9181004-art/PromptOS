#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
템플릿 이름 매칭 시스템
"""

from typing import Dict, List, Optional, Tuple
import os
import re
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer
import numpy as np

class TemplateMatcher:
    """
    템플릿 이름 매칭 시스템
    """
    
    def __init__(self):
        """초기화"""
        # 템플릿 디렉토리 경로
        self.templates_dir = "templates"
        
        # 사용 가능한 템플릿 목록
        self.available_templates = self._load_available_templates()
        print(f"총 로드된 템플릿 수: {len(self.available_templates)}")
        
        # 템플릿 이름별 설명 매핑
        self.template_descriptions = {
            "summary.txt": "문서 요약 및 핵심 내용 추출",
            "summary_meeting.txt": "회의록 요약 및 핵심 사항 정리",
            "self_intro.txt": "자기소개서 및 개인 소개",
            "self_intro_engineer.txt": "엔지니어 자기소개서",
            "customer_reply.txt": "고객 응대 및 불만 처리",
            "customer_reply_apology.txt": "고객 사과문 및 클레임 대응",
            "grant_proposal/ai/ai.txt": "AI 관련 정부지원사업 제안서",
            "grant_proposal/ai/government.txt": "정부 AI 정책 관련 제안서",
            "grant_proposal/ai/private.txt": "민간 AI 사업 제안서",
            "proposal/climate.txt": "기후변화 관련 제안서",
            "code_run.txt": "코드 실행 및 개발 관련",
            "unknown.txt": "일반적인 용도"
        }
        
        # SentenceTransformer 모델 로드
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.template_embeddings = self._compute_template_embeddings()
        except Exception as e:
            print(f"⚠️ SentenceTransformer 로드 실패: {e}")
            self.embedding_model = None
            self.template_embeddings = {}
    
    def _load_available_templates(self) -> List[str]:
        """사용 가능한 템플릿 목록을 로드합니다."""
        templates = []
        
        if os.path.exists(self.templates_dir):
            for root, dirs, files in os.walk(self.templates_dir):
                for file in files:
                    if file.endswith('.txt'):
                        # 상대 경로로 저장
                        rel_path = os.path.relpath(os.path.join(root, file), self.templates_dir)
                        templates.append(rel_path)
        
        return templates
    
    def _compute_template_embeddings(self) -> Dict[str, np.ndarray]:
        """템플릿 이름들의 임베딩을 계산합니다."""
        embeddings = {}
        
        for template in self.available_templates:
            # 템플릿 이름과 설명을 결합
            description = self.template_descriptions.get(template, "")
            text = f"{template} {description}"
            
            try:
                embedding = self.embedding_model.encode(text)
                embeddings[template] = embedding
            except Exception as e:
                print(f"⚠️ 템플릿 '{template}' 임베딩 계산 실패: {e}")
        
        return embeddings
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """코사인 유사도를 계산합니다."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def fuzzy_match(self, query: str, template_name: str) -> float:
        """퍼지 매칭 점수를 계산합니다."""
        return SequenceMatcher(None, query.lower(), template_name.lower()).ratio()
    
    def match_template_by_name(self, utterance: str, threshold: float = 0.6) -> Optional[str]:
        """
        발화를 기반으로 템플릿 이름을 매칭합니다.
        
        Args:
            utterance: 사용자 발화
            threshold: 매칭 임계값
            
        Returns:
            Optional[str]: 매칭된 템플릿 이름
        """
        if not self.available_templates:
            return None
        
        best_match = None
        best_score = 0.0
        
        # 1. 퍼지 매칭 시도
        for template in self.available_templates:
            # 템플릿 이름에서 확장자 제거
            template_name = os.path.splitext(template)[0]
            
            # 퍼지 매칭 점수 계산
            fuzzy_score = self.fuzzy_match(utterance, template_name)
            
            # 템플릿 설명과도 매칭 시도
            description = self.template_descriptions.get(template, "")
            desc_score = self.fuzzy_match(utterance, description)
            
            # 최고 점수 선택
            score = max(fuzzy_score, desc_score)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = template
        
        # 2. 임베딩 기반 유사도 매칭 (SentenceTransformer 사용 가능한 경우)
        if self.embedding_model and self.template_embeddings:
            try:
                utterance_embedding = self.embedding_model.encode(utterance)
                
                for template, template_embedding in self.template_embeddings.items():
                    similarity = self.cosine_similarity(utterance_embedding, template_embedding)
                    
                    if similarity > best_score and similarity >= threshold:
                        best_score = similarity
                        best_match = template
            except Exception as e:
                print(f"⚠️ 임베딩 기반 매칭 실패: {e}")
        
        return best_match
    
    def get_similar_templates(self, utterance: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        발화와 유사한 템플릿들을 반환합니다.
        
        Args:
            utterance: 사용자 발화
            top_k: 반환할 상위 템플릿 수
            
        Returns:
            List[Tuple[str, float]]: (템플릿 이름, 유사도 점수) 리스트
        """
        if not self.available_templates:
            return []
        
        template_scores = []
        
        # 모든 템플릿에 대해 점수 계산
        for template in self.available_templates:
            template_name = os.path.splitext(template)[0]
            description = self.template_descriptions.get(template, "")
            
            # 퍼지 매칭 점수
            fuzzy_score = self.fuzzy_match(utterance, template_name)
            desc_score = self.fuzzy_match(utterance, description)
            fuzzy_best = max(fuzzy_score, desc_score)
            
            # 임베딩 기반 유사도 (가능한 경우)
            embedding_score = 0.0
            if self.embedding_model and template in self.template_embeddings:
                try:
                    utterance_embedding = self.embedding_model.encode(utterance)
                    template_embedding = self.template_embeddings[template]
                    embedding_score = self.cosine_similarity(utterance_embedding, template_embedding)
                except Exception:
                    pass
            
            # 최종 점수 (퍼지 매칭과 임베딩 점수의 가중 평균)
            final_score = (fuzzy_best * 0.6) + (embedding_score * 0.4)
            template_scores.append((template, final_score))
        
        # 점수순으로 정렬하고 상위 k개 반환
        template_scores.sort(key=lambda x: x[1], reverse=True)
        return template_scores[:top_k]
    
    def get_template_info(self, template_name: str) -> Dict:
        """
        템플릿 정보를 반환합니다.
        
        Args:
            template_name: 템플릿 이름
            
        Returns:
            Dict: 템플릿 정보
        """
        description = self.template_descriptions.get(template_name, "설명 없음")
        
        return {
            "name": template_name,
            "description": description,
            "path": os.path.join(self.templates_dir, template_name),
            "exists": os.path.exists(os.path.join(self.templates_dir, template_name))
        }
    
    def add_template_description(self, template_name: str, description: str):
        """
        템플릿 설명을 추가합니다.
        
        Args:
            template_name: 템플릿 이름
            description: 설명
        """
        self.template_descriptions[template_name] = description
        
        # 임베딩 재계산 (가능한 경우)
        if self.embedding_model:
            try:
                text = f"{template_name} {description}"
                embedding = self.embedding_model.encode(text)
                self.template_embeddings[template_name] = embedding
            except Exception as e:
                print(f"⚠️ 템플릿 '{template_name}' 임베딩 추가 실패: {e}")
    
    def refresh_templates(self):
        """템플릿 목록을 새로고침합니다."""
        self.available_templates = self._load_available_templates()
        print(f"총 로드된 템플릿 수: {len(self.available_templates)}")
        
        if self.embedding_model:
            self.template_embeddings = self._compute_template_embeddings()

# 전역 인스턴스 생성
template_matcher = TemplateMatcher() 