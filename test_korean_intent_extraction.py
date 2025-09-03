#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Korean Intent & Purpose Extraction System Test
새로운 한글 중심 의도 및 목적 추출 시스템을 테스트합니다.
"""

from prompt_generator import extract_intent_and_purpose, process_user_request

def test_korean_intent_extraction():
    """
    한글 중심 Intent & Purpose Extraction 시스템을 테스트합니다.
    """
    print("🚀 한글 중심 Intent & Purpose Extraction 시스템 테스트")
    print("=" * 70)
    
    # 테스트 케이스들 - 짧고 모호한 한글 입력들
    test_cases = [
        "내 친구가 이걸 한다고 하는데, 나도 할까?",
        "이 방법이 가능할까?",
        "조언해주세요",
        "친구가 하는 것과 비교하면?",
        "이게 맞나?",
        "어떻게 해야 할지 모르겠어",
        "가능할까?",
        "도움이 필요해",
        "다른 방법은?",
        "확인해주세요",
        "걱정이에요",
        "불확실해",
        "시도해볼까?",
        "어떻게 할까?",
        "제안해주세요"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_input}")
        print("-" * 60)
        
        # Intent & Purpose Extraction 테스트
        intent_analysis = extract_intent_and_purpose(test_input)
        print(f"🎯 감지된 의도: {intent_analysis['intent']}")
        print(f"🎯 한글 분류: {intent_analysis['korean_classification']}")
        print(f"🎯 설명: {intent_analysis['description']}")
        print(f"📄 시스템 프롬프트:")
        print(intent_analysis['system_prompt'])
        
        # 전체 시스템 테스트
        try:
            result = process_user_request(test_input)
            print(f"📊 전체 시스템 결과:")
            print(f"  - 템플릿 의도: {result['intent']}")
            print(f"  - Intent & Purpose 의도: {result['intent_analysis']['intent']}")
            print(f"  - 한글 분류: {result['intent_analysis']['korean_classification']}")
            print(f"  - 최종 프롬프트 길이: {len(result['prompt'])}")
            
            # 어떤 시스템이 사용되었는지 확인
            if result['intent'] == 'etc' or result['intent_analysis']['intent'] != 'general_inquiry':
                print("✅ Intent & Purpose 기반 프롬프트가 사용되었습니다!")
            else:
                print("ℹ️ 기존 템플릿 기반 프롬프트가 사용되었습니다.")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_specific_korean_patterns():
    """
    특정 한글 패턴들을 테스트합니다.
    """
    print("\n🔍 특정 한글 패턴 테스트")
    print("=" * 50)
    
    pattern_tests = {
        "decision_making": [
            "할까?",
            "해야 할까?",
            "어떻게?",
            "시도해볼까?",
            "어떻게 할까?"
        ],
        "feasibility_judgment": [
            "가능할까?",
            "실현 가능할까?",
            "될까?"
        ],
        "advice_seeking": [
            "조언해주세요",
            "도움이 필요해",
            "제안해주세요",
            "가이드해주세요"
        ],
        "comparison_request": [
            "친구가 하는 것과 비교하면?",
            "다른 방법은?",
            "비교해주세요"
        ],
        "validation_seeking": [
            "맞나?",
            "올바른가?",
            "확인해주세요",
            "검증해주세요"
        ],
        "doubt_expression": [
            "모르겠어",
            "불확실해",
            "의심스러워",
            "걱정이에요"
        ]
    }
    
    for intent_type, test_inputs in pattern_tests.items():
        print(f"\n📌 {intent_type} 패턴:")
        for test_input in test_inputs:
            intent_analysis = extract_intent_and_purpose(test_input)
            print(f"  - '{test_input}' → {intent_analysis['intent']} ({intent_analysis['korean_classification']})")
            if intent_analysis['intent'] == intent_type:
                print(f"    ✅ 정확히 매칭됨")
            else:
                print(f"    ❌ 매칭 실패 (예상: {intent_type}, 실제: {intent_analysis['intent']})")

def test_mixed_language_inputs():
    """
    혼합 언어 입력을 테스트합니다.
    """
    print("\n🌐 혼합 언어 입력 테스트")
    print("=" * 40)
    
    mixed_test_cases = [
        "내 friend가 이걸 한다고 하는데, 나도 할까?",
        "이 방법이 possible할까?",
        "advice가 필요해",
        "친구 vs 나",
        "이게 right인가?",
        "don't know what to do",
        "help me please",
        "compare these options",
        "confirm this for me",
        "I'm worried about this"
    ]
    
    for i, test_input in enumerate(mixed_test_cases, 1):
        print(f"\n📝 혼합 언어 테스트 {i}: {test_input}")
        intent_analysis = extract_intent_and_purpose(test_input)
        print(f"  → 의도: {intent_analysis['intent']}")
        print(f"  → 한글 분류: {intent_analysis['korean_classification']}")
        print(f"  → 설명: {intent_analysis['description']}")

if __name__ == "__main__":
    test_korean_intent_extraction()
    test_specific_korean_patterns()
    test_mixed_language_inputs()
    print("\n🎉 한글 중심 Intent & Purpose Extraction 시스템 테스트 완료!") 