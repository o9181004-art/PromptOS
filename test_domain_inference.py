#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
도메인 추론 시스템 테스트
"""

from classify_intent import classify_intent
from domain_inference import domain_inference
from fallback_manager import fallback_manager

def test_domain_inference():
    """도메인 추론을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS에 대한 제안서를 작성해줘",
            "expected_domain": "technology",
            "description": "신조어 포함"
        },
        {
            "utterance": "ChatGPT를 활용한 교육 자료를 만들어줘",
            "expected_domain": "ai",
            "description": "AI 관련 신조어"
        },
        {
            "utterance": "스마트시티 정책 분석 보고서를 작성해줘",
            "expected_domain": "government",
            "description": "정부 관련 키워드"
        },
        {
            "utterance": "핀테크 스타트업 투자 제안서를 작성해줘",
            "expected_domain": "finance",
            "description": "금융 관련 신조어"
        },
        {
            "utterance": "바이오 기술 연구과제 신청서를 작성해줘",
            "expected_domain": "healthcare",
            "description": "의료 관련 키워드"
        },
        {
            "utterance": "메타버스 플랫폼 마케팅 콘텐츠를 작성해줘",
            "expected_domain": "technology",
            "description": "기술 관련 신조어"
        },
        {
            "utterance": "기후변화 대응 정책 브리프를 작성해줘",
            "expected_domain": "environment",
            "description": "환경 관련 키워드"
        },
        {
            "utterance": "온라인 교육 플랫폼 개발 제안서를 작성해줘",
            "expected_domain": "education",
            "description": "교육 관련 키워드"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "expected_domain": "general",
            "description": "일반적인 대화"
        }
    ]
    
    print("🧪 도메인 추론 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 도메인: {test_case['expected_domain']}")
        
        # 도메인 추론
        domain, confidence, domain_info = domain_inference.infer_domain(test_case['utterance'])
        print(f"✅ 추론된 도메인: {domain} (신뢰도: {confidence:.3f})")
        
        if domain == test_case['expected_domain']:
            print("🎉 정확히 추론됨!")
        else:
            print(f"⚠️ 예상과 다름: {domain}")
        
        # 도메인 컨텍스트 정보
        context = domain_inference.get_domain_context(domain)
        print(f"📋 도메인 컨텍스트: {context}")
        
        print("-" * 60)
        print()

def test_enhanced_intent_classification():
    """향상된 intent 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS 기술 소개서를 작성해줘",
            "description": "신조어가 포함된 요청"
        },
        {
            "utterance": "ChatGPT 활용 가이드를 만들어줘",
            "description": "AI 관련 신조어"
        },
        {
            "utterance": "스마트시티 정책 제안서를 작성해줘",
            "description": "정부 관련 키워드"
        },
        {
            "utterance": "핀테크 투자 피칭을 작성해줘",
            "description": "금융 관련 신조어"
        }
    ]
    
    print("🧪 향상된 Intent 분류 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # Intent 분류 (도메인 정보 포함)
        intent = classify_intent(test_case['utterance'])
        print(f"🎯 분류된 Intent: {intent}")
        
        # 도메인 추론
        domain, confidence, domain_info = domain_inference.infer_domain(test_case['utterance'])
        print(f"🏢 추론된 도메인: {domain} (신뢰도: {confidence:.3f})")
        
        # 관련 intent 확인
        related_intents = domain_inference.get_related_intents(domain)
        print(f"🔗 도메인 관련 Intent들: {related_intents}")
        
        if intent in related_intents:
            print("✅ 도메인과 일치하는 Intent로 분류됨!")
        else:
            print("⚠️ 도메인과 다른 Intent로 분류됨")
        
        print("-" * 60)
        print()

def test_enhanced_fallback_generation():
    """향상된 fallback 생성을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS 플랫폼 소개서를 작성해줘",
            "description": "신조어가 포함된 요청"
        },
        {
            "utterance": "ChatGPT 활용 교육 자료를 만들어줘",
            "description": "AI 관련 신조어"
        },
        {
            "utterance": "스마트시티 정책 분석을 해줘",
            "description": "정부 관련 키워드"
        }
    ]
    
    print("🧪 향상된 Fallback 생성 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # Intent 분류
        intent = classify_intent(test_case['utterance'])
        print(f"🎯 분류된 Intent: {intent}")
        
        # 도메인 추론
        domain, confidence, domain_info = domain_inference.infer_domain(test_case['utterance'])
        print(f"🏢 추론된 도메인: {domain} (신뢰도: {confidence:.3f})")
        
        # 향상된 fallback 생성
        try:
            enhanced_prompt = fallback_manager.generate_prompt_with_llm(
                test_case['utterance'], intent, domain
            )
            print(f"✅ 향상된 프롬프트 생성 성공 (길이: {len(enhanced_prompt)} 문자)")
            print(f"📄 프롬프트 미리보기: {enhanced_prompt[:200]}...")
        except Exception as e:
            print(f"❌ 프롬프트 생성 실패: {e}")
        
        print("-" * 60)
        print()

def test_neologism_detection():
    """신조어 감지를 테스트합니다."""
    
    test_terms = [
        "프롬프트OS",
        "ChatGPT", 
        "스마트시티",
        "메타버스",
        "핀테크",
        "바이오",
        "존재하지않는신조어"
    ]
    
    print("🧪 신조어 감지 테스트 시작\n")
    
    for term in test_terms:
        print(f"🔍 검사 중: {term}")
        
        # 신조어 검사
        neologism_info = domain_inference._check_neologism(term)
        
        if neologism_info:
            print(f"✅ 신조어 발견!")
            print(f"   설명: {neologism_info['description']}")
            print(f"   도메인: {neologism_info['domain']}")
            print(f"   관련 Intent: {neologism_info['related_intents']}")
        else:
            print(f"❌ 신조어가 아님")
        
        print("-" * 40)
        print()

if __name__ == "__main__":
    print("🚀 도메인 추론 시스템 테스트\n")
    
    # 1. 도메인 추론 테스트
    test_domain_inference()
    
    # 2. 향상된 intent 분류 테스트
    test_enhanced_intent_classification()
    
    # 3. 향상된 fallback 생성 테스트
    test_enhanced_fallback_generation()
    
    # 4. 신조어 감지 테스트
    test_neologism_detection()
    
    print("✅ 모든 테스트 완료!") 