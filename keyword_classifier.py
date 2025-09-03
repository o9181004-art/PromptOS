#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
키워드 기반 의도 분류 시스템
"""

from typing import Dict, List, Optional, Tuple
import re

class KeywordClassifier:
    """
    키워드 기반 의도 분류 시스템
    """
    
    def __init__(self):
        """초기화"""
        # 키워드 사전 (키워드 → 의도 매핑)
        self.keyword_intent_mapping = {
            # 요약 관련 키워드
            "summary": [
                "요약", "정리", "핵심", "개요", "줄거리", "요점", "개념", "설명",
                "분석", "검토", "평가", "리뷰", "요약해", "정리해", "핵심만", "간단히"
            ],
            
            # 자기소개 관련 키워드
            "self_intro": [
                "자기소개", "이력서", "경력", "소개", "프로필", "약력", "경험",
                "지원", "입사", "취업", "면접", "자소서", "자기소개서", "이력",
                "나를", "저를", "본인을", "개인을", "경력서", "이력서"
            ],
            
            # 고객 응대 관련 키워드
            "customer_reply": [
                "고객", "응대", "불만", "클레임", "사과", "해결", "처리", "대응",
                "서비스", "문의", "상담", "답변", "회신", "안내", "도움", "지원",
                "문제", "이슈", "해결책", "방안", "대책", "조치", "조치사항"
            ],
            
            # 정부지원사업 관련 키워드
            "grant_proposal": [
                "정부지원", "지원사업", "사업계획서", "제안서", "신청서", "기금",
                "연구과제", "연구개발", "R&D", "과제", "프로젝트", "사업화",
                "기술개발", "혁신", "창업", "벤처", "스타트업", "투자", "지원금",
                "보조금", "융자", "대출", "사업계획", "비즈니스플랜", "사업제안"
            ],
            
            # 스타트업 피칭 관련 키워드
            "startup_pitch": [
                "피칭", "투자유치", "투자제안", "비즈니스모델", "수익모델", "시장",
                "경쟁사", "차별화", "혁신", "창업", "스타트업", "벤처", "기업",
                "사업", "서비스", "제품", "플랫폼", "앱", "솔루션", "기술",
                "아이디어", "비즈니스", "사업계획", "전략", "마케팅", "판매"
            ],
            
            # 정책 브리프 관련 키워드
            "policy_brief": [
                "정책", "정책분석", "정책제안", "정책연구", "정책브리프", "정책보고서",
                "법안", "법령", "규정", "제도", "시스템", "체계", "방안", "대책",
                "해결책", "방법", "접근", "전략", "계획", "로드맵", "가이드라인",
                "표준", "기준", "원칙", "지침", "매뉴얼", "가이드"
            ],
            
            # 마케팅 콘텐츠 관련 키워드
            "marketing_copy": [
                "마케팅", "홍보", "광고", "브랜딩", "브랜드", "마케팅콘텐츠",
                "홍보자료", "광고문구", "카피", "슬로건", "캠페인", "프로모션",
                "이벤트", "세일", "할인", "쿠폰", "리워드", "포인트", "적립",
                "고객", "타겟", "시장", "경쟁", "차별화", "포지셔닝", "메시지"
            ],
            
            # 교육 콘텐츠 관련 키워드
            "education_content": [
                "교육", "학습", "강의", "수업", "튜토리얼", "가이드", "매뉴얼",
                "설명서", "교재", "학습자료", "교육자료", "강의자료", "수업자료",
                "커리큘럼", "과정", "프로그램", "워크샵", "세미나", "컨퍼런스",
                "학회", "연구", "조사", "분석", "리서치", "데이터", "통계"
            ],
            
            # 비즈니스 계획 관련 키워드 (fallback용)
            "business_plan": [
                "프롬프트", "사업계획서", "제안서", "정부", "예비창업", "신청", 
                "지원사업", "계획", "사업", "기획", "소개", "홍보", "비즈니스",
                "창업", "벤처", "스타트업", "투자", "지원금", "보조금", "융자",
                "대출", "사업계획", "비즈니스플랜", "사업제안", "기술개발",
                "혁신", "사업화", "R&D", "연구개발", "과제", "프로젝트"
            ]
        }
        
        # 키워드 가중치 (더 구체적인 키워드에 높은 가중치)
        self.keyword_weights = {
            "사업계획서": 10.0,
            "제안서": 9.0,
            "자기소개서": 9.0,
            "이력서": 8.0,
            "피칭": 8.0,
            "투자유치": 8.0,
            "정책분석": 8.0,
            "마케팅": 7.0,
            "홍보": 7.0,
            "교육": 6.0,
            "요약": 5.0,
            "고객": 5.0,
            # fallback 키워드들
            "프롬프트": 6.0,
            "정부": 7.0,
            "예비창업": 8.0,
            "신청": 6.0,
            "지원사업": 8.0,
            "계획": 5.0,
            "사업": 6.0,
            "기획": 6.0,
            "소개": 5.0,
            "홍보": 7.0
        }
    
    def classify_by_keywords(self, utterance: str) -> Tuple[str, float]:
        """
        키워드 기반으로 의도를 분류합니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            Tuple[str, float]: (분류된 의도, 신뢰도)
        """
        utterance_lower = utterance.lower()
        intent_scores = {}
        
        # 각 의도별로 키워드 매칭 점수 계산
        for intent, keywords in self.keyword_intent_mapping.items():
            score = 0
            
            for keyword in keywords:
                if keyword.lower() in utterance_lower:
                    # 키워드 가중치 적용
                    weight = self.keyword_weights.get(keyword, len(keyword) / 10.0)
                    score += weight
            
            if score > 0:
                intent_scores[intent] = score
        
        # 가장 높은 점수의 의도 선택
        if not intent_scores:
            return "unknown", 0.0
        
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # 신뢰도 계산 (점수가 3.0 이상일 때만 유효)
        confidence = min(best_intent[1] / 10.0, 1.0) if best_intent[1] > 3.0 else 0.0
        
        return best_intent[0], confidence
    
    def get_matched_keywords(self, utterance: str) -> Dict[str, List[str]]:
        """
        발화에서 매칭된 키워드들을 의도별로 반환합니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            Dict[str, List[str]]: 의도별 매칭된 키워드 리스트
        """
        utterance_lower = utterance.lower()
        matched_keywords = {}
        
        for intent, keywords in self.keyword_intent_mapping.items():
            matched = []
            for keyword in keywords:
                if keyword.lower() in utterance_lower:
                    matched.append(keyword)
            
            if matched:
                matched_keywords[intent] = matched
        
        return matched_keywords
    
    def add_keyword(self, intent: str, keyword: str, weight: float = None):
        """
        새로운 키워드를 사전에 추가합니다.
        
        Args:
            intent: 의도
            keyword: 키워드
            weight: 가중치 (선택사항)
        """
        if intent not in self.keyword_intent_mapping:
            self.keyword_intent_mapping[intent] = []
        
        if keyword not in self.keyword_intent_mapping[intent]:
            self.keyword_intent_mapping[intent].append(keyword)
        
        if weight is not None:
            self.keyword_weights[keyword] = weight
    
    def get_keyword_suggestions(self, partial_keyword: str) -> List[str]:
        """
        부분 키워드에 대한 제안을 반환합니다.
        
        Args:
            partial_keyword: 부분 키워드
            
        Returns:
            List[str]: 제안 키워드 리스트
        """
        suggestions = []
        partial_lower = partial_keyword.lower()
        
        for intent, keywords in self.keyword_intent_mapping.items():
            for keyword in keywords:
                if partial_lower in keyword.lower():
                    suggestions.append(keyword)
        
        return list(set(suggestions))  # 중복 제거
    
    def classify_fallback_keywords(self, utterance: str) -> Tuple[str, float]:
        """
        fallback 키워드 기반으로 의도를 분류합니다.
        LLM이 "unknown"을 반환했을 때 사용됩니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            Tuple[str, float]: (분류된 의도, 신뢰도)
        """
        utterance_lower = utterance.lower()
        
        # fallback 키워드들
        fallback_keywords = {
            "business_plan": [
                "프롬프트", "사업계획서", "제안서", "정부", "예비창업", "신청", 
                "지원사업", "계획", "사업", "기획", "소개", "홍보", "비즈니스",
                "창업", "벤처", "스타트업", "투자", "지원금", "보조금", "융자",
                "대출", "사업계획", "비즈니스플랜", "사업제안", "기술개발",
                "혁신", "사업화", "R&D", "연구개발", "과제", "프로젝트"
            ],
            "general_request": [
                "만들어", "작성해", "해줘", "도와", "생성", "제작", "구성",
                "개발", "설계", "계획", "안내", "가이드", "매뉴얼", "설명서"
            ]
        }
        
        intent_scores = {}
        
        for intent, keywords in fallback_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in utterance_lower:
                    weight = self.keyword_weights.get(keyword, len(keyword) / 10.0)
                    score += weight
            
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return "unknown", 0.0
        
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        confidence = min(best_intent[1] / 10.0, 1.0) if best_intent[1] > 2.0 else 0.0
        
        return best_intent[0], confidence
    
    def get_fallback_suggestions(self, utterance: str) -> List[str]:
        """
        fallback 키워드 제안을 반환합니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            List[str]: 제안 키워드 리스트
        """
        suggestions = []
        utterance_lower = utterance.lower()
        
        # 일반적인 비즈니스 관련 키워드들
        business_keywords = [
            "사업계획서", "지원서", "제안서", "정부지원", "창업", "투자",
            "마케팅", "홍보", "자기소개서", "이력서", "요약", "분석"
        ]
        
        for keyword in business_keywords:
            if keyword.lower() in utterance_lower:
                suggestions.append(keyword)
        
        return suggestions

# 전역 인스턴스 생성
keyword_classifier = KeywordClassifier() 