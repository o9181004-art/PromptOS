#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
심각한 문제 해결 테스트
"""

from classify_intent import classify_intent
from template_loader import get_template
from prompt_builder import extract_placeholders, fill_template

def test_critical_user_inputs():
    """실제 사용자 입력으로 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "예비창업자 패키지 사업계획서를 작성할거야. 아이템은 프롬프트OS야.",
            "description": "문제가 된 사용자 입력"
        },
        {
            "utterance": "사업계획서를 작성해줘",
            "description": "기본 사업계획서 요청"
        },
        {
            "utterance": "자기소개서를 작성해줘",
            "description": "자기소개서 요청"
        },
        {
            "utterance": "문서를 요약해줘",
            "description": "요약 요청"
        },
        {
            "utterance": "고객 응대 메시지를 작성해줘",
            "description": "고객 응대 요청"
        }
    ]
    
    print("🚨 심각한 문제 해결 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # 1. 의도 분류
        intent = classify_intent(test_case['utterance'])
        print(f"✅ 분류된 의도: {intent}")
        
        # 2. 템플릿 로딩
        template_text = get_template(intent, utterance=test_case['utterance'])
        print(f"📄 템플릿 로딩: {'성공' if template_text else '실패'}")
        
        if template_text:
            print(f"📏 템플릿 길이: {len(template_text)} 문자")
            print(f"📄 템플릿 미리보기: {template_text[:100]}...")
            
            # 3. 플레이스홀더 추출
            placeholders = extract_placeholders(template_text)
            print(f"🔧 플레이스홀더: {placeholders}")
            
            # 4. 기본 값으로 템플릿 채우기
            values = {
                "user_utterance": test_case['utterance'],
                "intent": intent,
                "domain": "general",
                "tone": "professional",
                "audience": "general",
                "tense": "현재시제"
            }
            
            # 누락된 플레이스홀더에 기본값 추가
            for placeholder in placeholders:
                if placeholder not in values:
                    values[placeholder] = "N/A"
            
            # 5. 템플릿 채우기
            try:
                final_prompt = fill_template(template_text, values)
                print(f"✅ 최종 프롬프트 생성: {'성공' if final_prompt else '실패'}")
                if final_prompt:
                    print(f"📏 프롬프트 길이: {len(final_prompt)} 문자")
                    print(f"📄 프롬프트 미리보기: {final_prompt[:200]}...")
            except Exception as e:
                print(f"❌ 템플릿 채우기 실패: {e}")
        else:
            print("❌ 템플릿을 찾을 수 없음")
        
        print("-" * 80)
        print()

def test_fallback_system():
    """Fallback 시스템을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트를 만들어줘",
            "intent": "business_plan",
            "description": "fallback 키워드 분류"
        },
        {
            "utterance": "정부 지원사업 신청서를 작성해줘",
            "intent": "business_plan", 
            "description": "정부 지원사업 키워드"
        },
        {
            "utterance": "일반적인 요청을 도와줘",
            "intent": "general_request",
            "description": "일반 요청"
        }
    ]
    
    print("🔄 Fallback 시스템 테스트\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 Intent: {test_case['intent']}")
        
        # 템플릿 로딩 테스트
        template_text = get_template(test_case['intent'], utterance=test_case['utterance'])
        
        if template_text:
            print(f"✅ 템플릿 로딩 성공 (길이: {len(template_text)} 문자)")
            
            # 플레이스홀더 추출
            placeholders = extract_placeholders(template_text)
            print(f"🔧 플레이스홀더: {placeholders}")
            
            # 기본 값으로 채우기
            values = {
                "user_utterance": test_case['utterance'],
                "intent": test_case['intent'],
                "domain": "general",
                "tone": "professional", 
                "audience": "general"
            }
            
            # 누락된 값에 기본값 추가
            for placeholder in placeholders:
                if placeholder not in values:
                    values[placeholder] = "N/A"
            
            # 템플릿 채우기
            try:
                final_prompt = fill_template(template_text, values)
                print(f"✅ 최종 프롬프트 생성 성공")
                print(f"📄 프롬프트 미리보기: {final_prompt[:150]}...")
            except Exception as e:
                print(f"❌ 템플릿 채우기 실패: {e}")
        else:
            print("❌ 템플릿 로딩 실패")
        
        print("-" * 60)
        print()

def test_template_availability():
    """사용 가능한 템플릿들을 확인합니다."""
    
    print("📁 템플릿 가용성 확인\n")
    
    # 주요 intent들에 대한 템플릿 확인
    intents = [
        "summary", "self_intro", "customer_reply", "grant_proposal",
        "startup_pitch", "policy_brief", "marketing_copy", "education_content",
        "business_plan", "general_request", "unknown"
    ]
    
    for intent in intents:
        template_text = get_template(intent)
        if template_text:
            print(f"✅ {intent}: 템플릿 있음 (길이: {len(template_text)} 문자)")
        else:
            print(f"❌ {intent}: 템플릿 없음")
    
    print("-" * 60)
    print()

if __name__ == "__main__":
    print("🚨 심각한 문제 해결 테스트 시작\n")
    
    # 1. 템플릿 가용성 확인
    test_template_availability()
    
    # 2. 실제 사용자 입력 테스트
    test_critical_user_inputs()
    
    # 3. Fallback 시스템 테스트
    test_fallback_system()
    
    print("✅ 모든 테스트 완료!") 