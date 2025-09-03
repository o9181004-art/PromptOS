#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
키워드 기반 분류 및 템플릿 매칭 시스템 테스트
"""

from classify_intent import classify_intent
from keyword_classifier import keyword_classifier
from template_matcher import template_matcher
from template_loader import get_template

def test_keyword_classification():
    """키워드 기반 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "사업계획서를 작성해줘",
            "expected_intent": "grant_proposal",
            "description": "정부지원사업 키워드"
        },
        {
            "utterance": "자기소개서를 작성해줘",
            "expected_intent": "self_intro",
            "description": "자기소개 키워드"
        },
        {
            "utterance": "고객 응대 메시지를 작성해줘",
            "expected_intent": "customer_reply",
            "description": "고객 응대 키워드"
        },
        {
            "utterance": "문서를 요약해줘",
            "expected_intent": "summary",
            "description": "요약 키워드"
        },
        {
            "utterance": "스타트업 피칭을 작성해줘",
            "expected_intent": "startup_pitch",
            "description": "피칭 키워드"
        },
        {
            "utterance": "정책 분석을 해줘",
            "expected_intent": "policy_brief",
            "description": "정책 키워드"
        },
        {
            "utterance": "마케팅 콘텐츠를 작성해줘",
            "expected_intent": "marketing_copy",
            "description": "마케팅 키워드"
        },
        {
            "utterance": "교육 자료를 만들어줘",
            "expected_intent": "education_content",
            "description": "교육 키워드"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "expected_intent": "unknown",
            "description": "일반적인 대화"
        }
    ]
    
    print("🧪 키워드 기반 분류 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 Intent: {test_case['expected_intent']}")
        
        # 키워드 기반 분류
        intent, confidence = keyword_classifier.classify_by_keywords(test_case['utterance'])
        print(f"✅ 키워드 분류 결과: {intent} (신뢰도: {confidence:.3f})")
        
        # 매칭된 키워드 확인
        matched_keywords = keyword_classifier.get_matched_keywords(test_case['utterance'])
        if matched_keywords:
            print(f"🔍 매칭된 키워드: {matched_keywords}")
        
        if intent == test_case['expected_intent']:
            print("🎉 정확히 분류됨!")
        else:
            print(f"⚠️ 예상과 다름: {intent}")
        
        print("-" * 60)
        print()

def test_template_matching():
    """템플릿 이름 매칭을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "요약 템플릿을 사용해줘",
            "expected_template": "summary.txt",
            "description": "요약 템플릿 매칭"
        },
        {
            "utterance": "자기소개서 템플릿이 필요해",
            "expected_template": "self_intro.txt",
            "description": "자기소개 템플릿 매칭"
        },
        {
            "utterance": "고객 응대 템플릿을 찾아줘",
            "expected_template": "customer_reply.txt",
            "description": "고객 응대 템플릿 매칭"
        },
        {
            "utterance": "회의록 요약 템플릿",
            "expected_template": "summary_meeting.txt",
            "description": "회의록 요약 템플릿 매칭"
        },
        {
            "utterance": "엔지니어 자기소개서",
            "expected_template": "self_intro_engineer.txt",
            "description": "엔지니어 자기소개 템플릿 매칭"
        },
        {
            "utterance": "AI 관련 제안서",
            "expected_template": "grant_proposal/ai/ai.txt",
            "description": "AI 제안서 템플릿 매칭"
        }
    ]
    
    print("🧪 템플릿 이름 매칭 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 템플릿: {test_case['expected_template']}")
        
        # 템플릿 이름 매칭
        matched_template = template_matcher.match_template_by_name(test_case['utterance'], threshold=0.6)
        print(f"✅ 매칭된 템플릿: {matched_template}")
        
        if matched_template == test_case['expected_template']:
            print("🎉 정확히 매칭됨!")
        else:
            print(f"⚠️ 예상과 다름: {matched_template}")
        
        # 유사한 템플릿들 확인
        similar_templates = template_matcher.get_similar_templates(test_case['utterance'], top_k=3)
        if similar_templates:
            print(f"🔍 유사한 템플릿들:")
            for template, score in similar_templates:
                print(f"  - {template} (유사도: {score:.3f})")
        
        print("-" * 60)
        print()

def test_enhanced_classification():
    """향상된 분류 시스템을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "사업계획서를 작성해줘",
            "description": "키워드 기반 분류 테스트"
        },
        {
            "utterance": "프롬프트OS 기술 소개서를 작성해줘",
            "description": "고유명사 기반 분류 테스트"
        },
        {
            "utterance": "ChatGPT 활용 가이드를 만들어줘",
            "description": "AI 관련 고유명사 테스트"
        },
        {
            "utterance": "스마트시티 정책 분석을 해줘",
            "description": "정부 정책 고유명사 테스트"
        },
        {
            "utterance": "창의적인 아이디어를 구체화하고 싶어",
            "description": "일반적인 요청 테스트"
        }
    ]
    
    print("🧪 향상된 분류 시스템 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # 향상된 분류 시스템
        intent = classify_intent(test_case['utterance'])
        print(f"✅ 최종 분류 결과: {intent}")
        
        # 키워드 분류 결과 확인
        keyword_intent, keyword_confidence = keyword_classifier.classify_by_keywords(test_case['utterance'])
        print(f"🔍 키워드 분류: {keyword_intent} (신뢰도: {keyword_confidence:.3f})")
        
        # 템플릿 매칭 시도
        if intent == "unknown":
            matched_template = template_matcher.match_template_by_name(test_case['utterance'], threshold=0.6)
            if matched_template:
                print(f"📋 템플릿 매칭: {matched_template}")
            else:
                print("📋 템플릿 매칭: 실패")
        
        print("-" * 60)
        print()

def test_template_loading():
    """템플릿 로딩을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "사업계획서를 작성해줘",
            "intent": "grant_proposal",
            "description": "정부지원사업 템플릿"
        },
        {
            "utterance": "자기소개서를 작성해줘",
            "intent": "self_intro",
            "description": "자기소개 템플릿"
        },
        {
            "utterance": "요약 템플릿을 사용해줘",
            "intent": "unknown",
            "description": "unknown intent 템플릿 매칭"
        }
    ]
    
    print("🧪 템플릿 로딩 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 Intent: {test_case['intent']}")
        
        # 템플릿 로딩
        template_content = get_template(test_case['intent'], utterance=test_case['utterance'])
        
        if template_content:
            print(f"✅ 템플릿 로딩 성공 (길이: {len(template_content)} 문자)")
            print(f"📄 템플릿 미리보기: {template_content[:200]}...")
        else:
            print("❌ 템플릿 로딩 실패")
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("🚀 키워드 기반 분류 및 템플릿 매칭 시스템 테스트\n")
    
    # 1. 키워드 기반 분류 테스트
    test_keyword_classification()
    
    # 2. 템플릿 이름 매칭 테스트
    test_template_matching()
    
    # 3. 향상된 분류 시스템 테스트
    test_enhanced_classification()
    
    # 4. 템플릿 로딩 테스트
    test_template_loading()
    
    print("✅ 모든 테스트 완료!") 