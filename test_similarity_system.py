#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
유사도 기반 분류 및 템플릿 매핑 시스템 테스트
"""

from classify_intent import classify_intent
from template_loader import get_template
from intent_similarity_classifier import similarity_classifier
from template_mapper import template_mapper

def test_similarity_classification():
    """유사도 기반 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "문서를 요약해줘",
            "expected": "summary",
            "description": "명확한 요약 요청"
        },
        {
            "utterance": "자기소개서를 작성해줘",
            "expected": "self_intro",
            "description": "명확한 자기소개 요청"
        },
        {
            "utterance": "고객 응대 메시지를 작성해줘",
            "expected": "customer_reply",
            "description": "명확한 고객 응대 요청"
        },
        {
            "utterance": "정부지원사업 제안서를 작성해줘",
            "expected": "grant_proposal",
            "description": "명확한 제안서 요청"
        },
        {
            "utterance": "스타트업 투자유치 피칭을 작성해줘",
            "expected": "startup_pitch",
            "description": "명확한 피칭 요청"
        },
        {
            "utterance": "정책 분석 보고서를 작성해줘",
            "expected": "policy_brief",
            "description": "명확한 정책 분석 요청"
        },
        {
            "utterance": "마케팅 콘텐츠를 작성해줘",
            "expected": "marketing_copy",
            "description": "명확한 마케팅 요청"
        },
        {
            "utterance": "교육 자료를 작성해줘",
            "expected": "education_content",
            "description": "명확한 교육 자료 요청"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "expected": "unknown",
            "description": "일반적인 대화"
        },
        {
            "utterance": "안녕하세요",
            "expected": "unknown",
            "description": "인사말"
        }
    ]
    
    print("🧪 유사도 기반 분류 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 결과: {test_case['expected']}")
        
        # Intent 분류
        result = classify_intent(test_case['utterance'])
        
        print(f"✅ 실제 결과: {result}")
        
        if result == test_case['expected']:
            print("🎉 정확히 분류됨!")
        else:
            print(f"⚠️ 예상과 다름: {result}")
        
        print("-" * 60)
        print()

def test_template_mapping():
    """템플릿 매핑을 테스트합니다."""
    
    test_cases = [
        {
            "intent": "summary",
            "description": "요약 템플릿 매핑"
        },
        {
            "intent": "self_intro",
            "description": "자기소개 템플릿 매핑"
        },
        {
            "intent": "customer_reply",
            "description": "고객 응대 템플릿 매핑"
        },
        {
            "intent": "grant_proposal",
            "description": "제안서 템플릿 매핑"
        },
        {
            "intent": "startup_pitch",
            "description": "피칭 템플릿 매핑"
        },
        {
            "intent": "policy_brief",
            "description": "정책 분석 템플릿 매핑"
        },
        {
            "intent": "marketing_copy",
            "description": "마케팅 템플릿 매핑"
        },
        {
            "intent": "education_content",
            "description": "교육 자료 템플릿 매핑"
        }
    ]
    
    print("🧪 템플릿 매핑 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"🎯 Intent: {test_case['intent']}")
        
        # 템플릿 목록 가져오기
        templates = template_mapper.get_templates_for_intent(test_case['intent'])
        print(f"📋 매핑된 템플릿들: {templates}")
        
        # 최적 템플릿 선택
        best_template = template_mapper.get_best_template_for_intent(test_case['intent'])
        print(f"🏆 최적 템플릿: {best_template}")
        
        # 템플릿 로드 테스트
        template_content = get_template(test_case['intent'], utterance=f"{test_case['intent']} 관련 요청")
        if template_content:
            print(f"✅ 템플릿 로드 성공 (길이: {len(template_content)} 문자)")
        else:
            print("❌ 템플릿 로드 실패")
        
        print("-" * 60)
        print()

def test_similarity_fallback():
    """유사도 기반 fallback을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "문서를 간단히 정리해줘",
            "description": "요약과 유사한 요청"
        },
        {
            "utterance": "개인 프로필을 작성해줘",
            "description": "자기소개와 유사한 요청"
        },
        {
            "utterance": "사과문을 써줘",
            "description": "고객 응대와 유사한 요청"
        },
        {
            "utterance": "코드 실행 방법을 알려줘",
            "description": "코드 관련 요청"
        }
    ]
    
    print("🧪 유사도 기반 Fallback 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # Intent 분류
        intent = classify_intent(test_case['utterance'])
        print(f"🎯 분류된 Intent: {intent}")
        
        # 템플릿 로드 (unknown인 경우 유사도 기반 fallback)
        template_content = get_template(intent, utterance=test_case['utterance'])
        
        if template_content:
            print(f"✅ 템플릿 로드 성공 (길이: {len(template_content)} 문자)")
            # 템플릿 내용 미리보기
            preview = template_content[:100] + "..." if len(template_content) > 100 else template_content
            print(f"📄 템플릿 미리보기: {preview}")
        else:
            print("❌ 템플릿 로드 실패")
        
        print("-" * 60)
        print()

def test_similar_intents():
    """유사한 intent 찾기를 테스트합니다."""
    
    test_utterances = [
        "문서를 요약해줘",
        "자기소개서를 작성해줘",
        "고객 응대 메시지를 작성해줘",
        "정부지원사업 제안서를 작성해줘"
    ]
    
    print("🧪 유사한 Intent 찾기 테스트 시작\n")
    
    for utterance in test_utterances:
        print(f"💬 입력: {utterance}")
        
        # 유사한 intent들 찾기
        similar_intents = similarity_classifier.get_similar_intents(utterance, top_k=3)
        
        print("🔍 유사한 Intent들:")
        for i, (intent, similarity) in enumerate(similar_intents, 1):
            print(f"  {i}. {intent} (유사도: {similarity:.3f})")
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("🚀 유사도 기반 분류 및 템플릿 매핑 시스템 테스트\n")
    
    # 1. 유사도 기반 분류 테스트
    test_similarity_classification()
    
    # 2. 템플릿 매핑 테스트
    test_template_mapping()
    
    # 3. 유사도 기반 fallback 테스트
    test_similarity_fallback()
    
    # 4. 유사한 intent 찾기 테스트
    test_similar_intents()
    
    print("✅ 모든 테스트 완료!") 