#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
개선된 fallback 시스템 테스트
"""

from classify_intent import classify_intent
from keyword_classifier import keyword_classifier
from template_loader import get_template
from fallback_manager import FallbackManager

def test_fallback_keyword_classification():
    """fallback 키워드 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "expected_intent": "business_plan",
            "description": "프롬프트 키워드"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "expected_intent": "business_plan",
            "description": "정부 지원사업 키워드"
        },
        {
            "utterance": "예비창업자 지원 프로그램 안내해줘",
            "expected_intent": "business_plan",
            "description": "예비창업 키워드"
        },
        {
            "utterance": "사업계획서를 작성해줘",
            "expected_intent": "business_plan",
            "description": "사업계획서 키워드"
        },
        {
            "utterance": "제안서를 만들어줘",
            "expected_intent": "business_plan",
            "description": "제안서 키워드"
        },
        {
            "utterance": "일반적인 요청을 도와줘",
            "expected_intent": "general_request",
            "description": "일반 요청 키워드"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "expected_intent": "unknown",
            "description": "일반적인 대화"
        }
    ]
    
    print("🧪 Fallback 키워드 분류 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 Intent: {test_case['expected_intent']}")
        
        # fallback 키워드 기반 분류
        intent, confidence = keyword_classifier.classify_fallback_keywords(test_case['utterance'])
        print(f"✅ Fallback 분류 결과: {intent} (신뢰도: {confidence:.3f})")
        
        # fallback 제안 확인
        suggestions = keyword_classifier.get_fallback_suggestions(test_case['utterance'])
        if suggestions:
            print(f"🔍 Fallback 제안: {suggestions}")
        
        if intent == test_case['expected_intent']:
            print("🎉 정확히 분류됨!")
        else:
            print(f"⚠️ 예상과 다름: {intent}")
        
        print("-" * 60)
        print()

def test_enhanced_intent_classification():
    """향상된 의도 분류 시스템을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "description": "fallback 키워드 테스트"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "description": "정부 지원사업 키워드 테스트"
        },
        {
            "utterance": "예비창업자 지원 프로그램 안내해줘",
            "description": "예비창업 키워드 테스트"
        },
        {
            "utterance": "일반적인 요청을 도와줘",
            "description": "일반 요청 키워드 테스트"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "description": "일반적인 대화 테스트"
        }
    ]
    
    print("🧪 향상된 의도 분류 시스템 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # 향상된 분류 시스템
        intent = classify_intent(test_case['utterance'])
        print(f"✅ 최종 분류 결과: {intent}")
        
        # fallback 키워드 분류 결과 확인
        fallback_intent, fallback_confidence = keyword_classifier.classify_fallback_keywords(test_case['utterance'])
        print(f"🔍 Fallback 분류: {fallback_intent} (신뢰도: {fallback_confidence:.3f})")
        
        print("-" * 60)
        print()

def test_template_loading_with_fallback():
    """fallback을 포함한 템플릿 로딩을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "intent": "unknown",
            "description": "unknown intent 템플릿 매칭"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "intent": "unknown",
            "description": "정부 지원사업 템플릿 매칭"
        },
        {
            "utterance": "일반적인 요청을 도와줘",
            "intent": "unknown",
            "description": "일반 요청 템플릿 매칭"
        }
    ]
    
    print("🧪 Fallback 템플릿 로딩 테스트 시작\n")
    
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

def test_fallback_manager():
    """FallbackManager를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "intent": "unknown",
            "domain": "technology",
            "audience": "developers",
            "description": "프롬프트 생성 요청"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "intent": "unknown",
            "domain": "government",
            "audience": "business",
            "description": "정부 지원사업 요청"
        },
        {
            "utterance": "일반적인 요청을 도와줘",
            "intent": "unknown",
            "domain": "general",
            "audience": "general",
            "description": "일반 요청"
        }
    ]
    
    print("🧪 FallbackManager 테스트 시작\n")
    
    fallback_manager = FallbackManager()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 Intent: {test_case['intent']}")
        print(f"🏢 Domain: {test_case['domain']}")
        print(f"👥 Audience: {test_case['audience']}")
        
        # 도움 메시지 생성
        helpful_message = fallback_manager.generate_helpful_message(test_case['utterance'])
        print(f"💡 도움 메시지: {helpful_message}")
        
        # 프롬프트 검증 테스트
        test_prompts = [
            "정상적인 프롬프트입니다.",
            "{placeholder}가 포함된 프롬프트",
            "{slot}와 {variable}이 있는 프롬프트",
            "# 단일 제목",
            "너무 짧음",
            ""
        ]
        
        print("🔍 프롬프트 검증 테스트:")
        for prompt in test_prompts:
            validated = fallback_manager._validate_and_fix_prompt(prompt)
            print(f"  원본: '{prompt}' → 검증: '{validated}'")
        
        print("-" * 60)
        print()

def test_error_handling():
    """오류 처리를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "description": "fallback 키워드 제안 테스트"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "description": "정부 지원사업 키워드 제안 테스트"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "description": "일반적인 대화 제안 테스트"
        }
    ]
    
    print("🧪 오류 처리 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # fallback 제안 확인
        suggestions = keyword_classifier.get_fallback_suggestions(test_case['utterance'])
        print(f"🔍 Fallback 제안: {suggestions}")
        
        # 도움 메시지 생성
        fallback_manager = FallbackManager()
        helpful_message = fallback_manager.generate_helpful_message(test_case['utterance'])
        print(f"💡 도움 메시지: {helpful_message}")
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("🚀 개선된 Fallback 시스템 테스트\n")
    
    # 1. Fallback 키워드 분류 테스트
    test_fallback_keyword_classification()
    
    # 2. 향상된 의도 분류 시스템 테스트
    test_enhanced_intent_classification()
    
    # 3. Fallback 템플릿 로딩 테스트
    test_template_loading_with_fallback()
    
    # 4. FallbackManager 테스트
    test_fallback_manager()
    
    # 5. 오류 처리 테스트
    test_error_handling()
    
    print("✅ 모든 테스트 완료!") 