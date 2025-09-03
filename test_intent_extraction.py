#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Intent & Purpose Extraction System Test
새로운 의도 및 목적 추출 시스템을 테스트합니다.
"""

from prompt_generator import extract_intent_and_purpose, process_user_request

def test_intent_extraction():
    """
    Intent & Purpose Extraction 시스템을 테스트합니다.
    """
    print("🚀 Intent & Purpose Extraction 시스템 테스트")
    print("=" * 60)
    
    # 테스트 케이스들 - 모호하고 비형식적인 입력들
    test_cases = [
        "My friend is doing this thing... should I try it too?",
        "내 친구가 이걸 한다고 하는데, 나도 할까?",
        "I don't know what to do...",
        "어떻게 해야 할지 모르겠어",
        "Is this the right approach?",
        "이 방법이 맞나?",
        "Can you help me decide?",
        "결정하는데 도움을 주세요",
        "What's the difference between these options?",
        "이 옵션들 사이의 차이점이 뭔가요?",
        "I'm worried about making the wrong choice",
        "잘못된 선택을 할까봐 걱정이에요",
        "Should I follow my friend's advice?",
        "친구 조언을 따라야 할까?",
        "I'm not sure if this is the right time",
        "지금이 적절한 시기인지 확신이 안 서요"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_input}")
        print("-" * 50)
        
        # Intent & Purpose Extraction 테스트
        intent_analysis = extract_intent_and_purpose(test_input)
        print(f"🎯 감지된 의도: {intent_analysis['intent']}")
        print(f"🎯 재구성된 목적: {intent_analysis['purpose']}")
        print(f"🎯 톤 가이드: {intent_analysis['tone']}")
        print(f"📄 시스템 프롬프트:")
        print(intent_analysis['system_prompt'])
        
        # 전체 시스템 테스트
        try:
            result = process_user_request(test_input)
            print(f"📊 전체 시스템 결과:")
            print(f"  - 템플릿 의도: {result['intent']}")
            print(f"  - Intent & Purpose 의도: {result['intent_analysis']['intent']}")
            print(f"  - 최종 프롬프트 길이: {len(result['prompt'])}")
            
            # 어떤 시스템이 사용되었는지 확인
            if result['intent'] == 'etc' or result['intent_analysis']['intent'] != 'general_inquiry':
                print("✅ Intent & Purpose 기반 프롬프트가 사용되었습니다!")
            else:
                print("ℹ️ 기존 템플릿 기반 프롬프트가 사용되었습니다.")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_specific_patterns():
    """
    특정 패턴들을 테스트합니다.
    """
    print("\n🔍 특정 패턴 테스트")
    print("=" * 40)
    
    pattern_tests = {
        "decision_making": [
            "should i do it?",
            "할까?",
            "해야 할까?",
            "어떻게 해야 할까?"
        ],
        "doubt_expression": [
            "모르겠어",
            "don't know",
            "불확실해",
            "uncertain"
        ],
        "comparison_request": [
            "친구가 하는 것과 비교하면?",
            "friend vs me",
            "다른 방법은?",
            "other options"
        ],
        "validation_seeking": [
            "맞나?",
            "right?",
            "올바른가?",
            "correct?"
        ],
        "advice_request": [
            "조언해주세요",
            "advice needed",
            "도움이 필요해",
            "help me"
        ]
    }
    
    for intent_type, test_inputs in pattern_tests.items():
        print(f"\n📌 {intent_type} 패턴:")
        for test_input in test_inputs:
            intent_analysis = extract_intent_and_purpose(test_input)
            print(f"  - '{test_input}' → {intent_analysis['intent']}")
            if intent_analysis['intent'] == intent_type:
                print(f"    ✅ 정확히 매칭됨")
            else:
                print(f"    ❌ 매칭 실패 (예상: {intent_type}, 실제: {intent_analysis['intent']})")

if __name__ == "__main__":
    test_intent_extraction()
    test_specific_patterns()
    print("\n🎉 Intent & Purpose Extraction 시스템 테스트 완료!") 