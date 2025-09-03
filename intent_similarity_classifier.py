#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
유사도 기반 Intent 분류 시스템
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional
import json
import os

class IntentSimilarityClassifier:
    """
    유사도 기반 Intent 분류기
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        초기화
        
        Args:
            model_name: 사용할 sentence transformer 모델명
        """
        self.model = SentenceTransformer(model_name)
        self.intent_embeddings = {}
        self.intent_examples = {}
        self.similarity_threshold = 0.75
        
        # Intent 예시 정의
        self._define_intent_examples()
        self._compute_intent_embeddings()
    
    def _define_intent_examples(self):
        """각 intent에 대한 예시 문장들을 정의합니다."""
        self.intent_examples = {
            "summary": [
                "문서를 요약해줘",
                "긴 텍스트를 간단히 정리해줘",
                "핵심 내용만 추출해줘",
                "요약본을 만들어줘",
                "간결하게 정리해줘",
                "주요 포인트만 뽑아줘"
            ],
            "self_intro": [
                "자기소개서를 작성해줘",
                "이력서를 만들어줘",
                "개인 소개글을 써줘",
                "지원 동기를 설명해줘",
                "자기소개를 해줘",
                "개인 프로필을 작성해줘"
            ],
            "customer_reply": [
                "고객 응대 메시지를 작성해줘",
                "불만 처리 사과문을 써줘",
                "클레임 대응문을 만들어줘",
                "고객 서비스 답변을 작성해줘",
                "사과문을 써줘",
                "고객 문의에 답변해줘"
            ],
            "grant_proposal": [
                "정부지원사업 제안서를 작성해줘",
                "연구과제 신청서를 만들어줘",
                "기금 신청서를 써줘",
                "사업 제안서를 작성해줘",
                "지원서를 만들어줘",
                "과제 신청서를 써줘"
            ],
            "startup_pitch": [
                "스타트업 투자유치 피칭을 작성해줘",
                "비즈니스 모델 설명을 만들어줘",
                "피칭덱을 작성해줘",
                "투자 제안서를 써줘",
                "스타트업 소개를 만들어줘",
                "비즈니스 피칭을 작성해줘"
            ],
            "policy_brief": [
                "정책 분석 보고서를 작성해줘",
                "정책 제안서를 만들어줘",
                "정책 브리프를 써줘",
                "정책 보고서를 작성해줘",
                "정책 연구 결과를 정리해줘",
                "정책 분석을 해줘"
            ],
            "marketing_copy": [
                "마케팅 콘텐츠를 작성해줘",
                "광고 문구를 만들어줘",
                "홍보 자료를 써줘",
                "브랜딩 문구를 작성해줘",
                "제품 소개를 만들어줘",
                "마케팅 문구를 써줘"
            ],
            "education_content": [
                "교육 자료를 작성해줘",
                "강의 내용을 만들어줘",
                "학습 가이드를 써줘",
                "설명서를 작성해줘",
                "튜토리얼을 만들어줘",
                "교육 콘텐츠를 써줘"
            ]
        }
    
    def _compute_intent_embeddings(self):
        """각 intent의 예시 문장들을 임베딩하여 저장합니다."""
        for intent, examples in self.intent_examples.items():
            # 각 intent의 모든 예시 문장을 임베딩
            embeddings = self.model.encode(examples)
            # 평균 임베딩을 계산하여 intent의 대표 벡터로 사용
            self.intent_embeddings[intent] = np.mean(embeddings, axis=0)
    
    def classify_by_similarity(self, utterance: str) -> Tuple[str, float]:
        """
        유사도 기반으로 intent를 분류합니다.
        
        Args:
            utterance: 분류할 사용자 발화
            
        Returns:
            Tuple[str, float]: (분류된 intent, 유사도 점수)
        """
        # 입력 문장 임베딩
        utterance_embedding = self.model.encode([utterance])[0]
        
        # 각 intent와의 유사도 계산
        similarities = {}
        for intent, intent_embedding in self.intent_embeddings.items():
            similarity = cosine_similarity(
                [utterance_embedding], 
                [intent_embedding]
            )[0][0]
            similarities[intent] = similarity
        
        # 가장 높은 유사도를 가진 intent 찾기
        best_intent = max(similarities.items(), key=lambda x: x[1])
        
        # 임계값 이상인 경우에만 해당 intent 반환
        if best_intent[1] >= self.similarity_threshold:
            return best_intent
        else:
            return "unknown", best_intent[1]
    
    def get_similar_intents(self, utterance: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        입력 문장과 유사한 intent들을 상위 k개 반환합니다.
        
        Args:
            utterance: 분류할 사용자 발화
            top_k: 반환할 상위 intent 개수
            
        Returns:
            List[Tuple[str, float]]: (intent, 유사도 점수) 리스트
        """
        # 입력 문장 임베딩
        utterance_embedding = self.model.encode([utterance])[0]
        
        # 각 intent와의 유사도 계산
        similarities = []
        for intent, intent_embedding in self.intent_embeddings.items():
            similarity = cosine_similarity(
                [utterance_embedding], 
                [intent_embedding]
            )[0][0]
            similarities.append((intent, similarity))
        
        # 유사도 순으로 정렬하여 상위 k개 반환
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def set_similarity_threshold(self, threshold: float):
        """유사도 임계값을 설정합니다."""
        self.similarity_threshold = threshold
    
    def add_intent_example(self, intent: str, example: str):
        """새로운 intent 예시를 추가합니다."""
        if intent not in self.intent_examples:
            self.intent_examples[intent] = []
        
        self.intent_examples[intent].append(example)
        
        # 임베딩 재계산
        embeddings = self.model.encode(self.intent_examples[intent])
        self.intent_embeddings[intent] = np.mean(embeddings, axis=0)

# 전역 인스턴스 생성
similarity_classifier = IntentSimilarityClassifier() 