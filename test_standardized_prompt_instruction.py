#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📋 [Prompt Instruction Format] 테스트
새로운 표준화된 프롬프트 지시사항 형식이 올바르게 작동하는지 테스트합니다.
"""

from prompt_generator import (
    process_user_request,
    generate_standardized_prompt_instruction,
    extract_intent_and_purpose
)

def test_standardized_prompt_instruction():
    """
    표준화된 프롬프트 지시사항 생성 기능을 테스트합니다.
    """
    print("📋 [Prompt Instruction Format] 테스트")
    print("=" * 80)

    # 테스트 케이스들
    test_cases = [
        {
            "input": "IR 자료 초안 좀 만들어줘",
            "description": "명확한 IR 문서 요청",
            "expected_intent": "investor_IR_document"
        },
        {
            "input": "사업계획서 써줘",
            "description": "명확한 사업계획서 요청",
            "expected_intent": "business_plan"
        },
        {
            "input": "마케팅 카피 써줘",
            "description": "명확한 마케팅 카피 요청",
            "expected_intent": "marketing_copy"
        },
        {
            "input": "그냥 써줘",
            "description": "모호한 콘텐츠 작성 요청",
            "expected_intent": "content_creation"
        },
        {
            "input": "나도 할까?",
            "description": "모호한 의사결정 요청",
            "expected_intent": "decision_making"
        },
        {
            "input": "형, 이거 요즘 대세야?",
            "description": "모호한 트렌드 검증 요청",
            "expected_intent": "trend_verification"
        },
        {
            "input": "그냥 사람 감성 자극하는 거 써줘",
            "description": "모호한 마케팅 카피 요청",
            "expected_intent": "marketing_copy"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 테스트 {i}: {test_case['description']}")
        print(f"입력: {test_case['input']}")
        print("-" * 60)

        try:
            # process_user_request 호출
            result = process_user_request(test_case['input'])
            
            # 결과 확인
            intent = result["intent"]
            prompt_instruction = result["prompt_instruction"]
            confidence_score = result["confidence_score"]
            method = result["method"]
            
            print(f"✅ 의도 분류: {intent}")
            print(f"✅ 신뢰도: {confidence_score:.2f}")
            print(f"✅ 처리 방법: {method}")
            print(f"✅ 예상 의도: {test_case['expected_intent']}")
            
            # 의도 일치 여부 확인
            if intent == test_case['expected_intent']:
                print("🎯 의도 분류 정확!")
            else:
                print(f"⚠️  의도 분류 불일치: 예상={test_case['expected_intent']}, 실제={intent}")
            
            print("\n📋 생성된 프롬프트 지시사항:")
            print(prompt_instruction)
            
            # 프롬프트 지시사항 형식 검증
            if "📋 [Prompt Instruction Format]" in prompt_instruction:
                print("✅ 올바른 형식 확인")
            else:
                print("❌ 형식 오류")
                
            if "User utterance:" in prompt_instruction:
                print("✅ User utterance 포함")
            else:
                print("❌ User utterance 누락")
                
            if "Intent:" in prompt_instruction:
                print("✅ Intent 포함")
            else:
                print("❌ Intent 누락")
                
            if "Reconstructed Purpose:" in prompt_instruction:
                print("✅ Reconstructed Purpose 포함")
            else:
                print("❌ Reconstructed Purpose 누락")
                
            if "Instruction:" in prompt_instruction:
                print("✅ Instruction 포함")
            else:
                print("❌ Instruction 누락")
                
            if "Output must be in Korean" in prompt_instruction:
                print("✅ 한국어 출력 요구사항 포함")
            else:
                print("❌ 한국어 출력 요구사항 누락")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_context_aware_prompt_instruction():
    """
    맥락 인식 프롬프트 지시사항 생성 기능을 테스트합니다.
    """
    print("\n\n🎯 맥락 인식 프롬프트 지시사항 테스트")
    print("=" * 80)

    # 맥락이 있는 테스트 케이스들
    test_cases = [
        {
            "input": "초안부터 시작하고 싶어요",
            "chat_history": [
                {"role": "user", "content": "투자자들에게 제출할 자료가 필요해요"},
                {"role": "assistant", "content": "어떤 종류의 투자자 자료인가요?"},
                {"role": "user", "content": "IR 자료를 준비하고 있어요"},
                {"role": "assistant", "content": "IR 자료 작성을 도와드리겠습니다."}
            ],
            "description": "IR 맥락에서의 초안 요청",
            "expected_intent": "investor_IR_document"
        },
        {
            "input": "계획서가 필요해요",
            "chat_history": [
                {"role": "user", "content": "창업을 준비하고 있어요"},
                {"role": "assistant", "content": "어떤 분야의 창업인가요?"},
                {"role": "user", "content": "IT 스타트업을 계획하고 있어요"},
                {"role": "assistant", "content": "IT 스타트업 창업을 축하드립니다."}
            ],
            "description": "창업 맥락에서의 계획서 요청",
            "expected_intent": "business_plan"
        },
        {
            "input": "고객들에게 어필할 카피가 필요해요",
            "chat_history": [
                {"role": "user", "content": "새로운 제품을 출시하려고 해요"},
                {"role": "assistant", "content": "어떤 제품인가요?"},
                {"role": "user", "content": "커피 브랜드입니다"},
                {"role": "assistant", "content": "커피 브랜드 마케팅을 도와드리겠습니다."}
            ],
            "description": "제품 출시 맥락에서의 마케팅 카피 요청",
            "expected_intent": "marketing_copy"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 맥락 테스트 {i}: {test_case['description']}")
        print(f"입력: {test_case['input']}")
        print(f"맥락: {len(test_case['chat_history'])}개 메시지")
        print("-" * 60)

        try:
            # process_user_request 호출 (맥락 포함)
            result = process_user_request(test_case['input'], test_case['chat_history'])
            
            # 결과 확인
            intent = result["intent"]
            prompt_instruction = result["prompt_instruction"]
            confidence_score = result["confidence_score"]
            method = result["method"]
            context_used = result.get("context_used", False)
            
            print(f"✅ 의도 분류: {intent}")
            print(f"✅ 신뢰도: {confidence_score:.2f}")
            print(f"✅ 처리 방법: {method}")
            print(f"✅ 맥락 사용: {context_used}")
            print(f"✅ 예상 의도: {test_case['expected_intent']}")
            
            # 의도 일치 여부 확인
            if intent == test_case['expected_intent']:
                print("🎯 의도 분류 정확!")
            else:
                print(f"⚠️  의도 분류 불일치: 예상={test_case['expected_intent']}, 실제={intent}")
            
            print("\n📋 생성된 프롬프트 지시사항:")
            print(prompt_instruction)
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_direct_function_call():
    """
    generate_standardized_prompt_instruction 함수를 직접 호출하여 테스트합니다.
    """
    print("\n\n🔧 직접 함수 호출 테스트")
    print("=" * 80)

    # 직접 함수 호출 테스트
    test_input = "IR 자료 초안 좀 만들어줘"
    
    try:
        # 의도 분석
        intent_analysis = extract_intent_and_purpose(test_input)
        
        # 표준화된 프롬프트 지시사항 생성
        prompt_instruction = generate_standardized_prompt_instruction(test_input, intent_analysis)
        
        print(f"입력: {test_input}")
        print(f"의도 분석: {intent_analysis['intent']}")
        print("\n📋 생성된 프롬프트 지시사항:")
        print(prompt_instruction)
        
        # 형식 검증
        required_elements = [
            "📋 [Prompt Instruction Format]",
            "User utterance:",
            "Intent:",
            "Reconstructed Purpose:",
            "Instruction:",
            "Output must be in Korean"
        ]
        
        print("\n🔍 형식 검증:")
        for element in required_elements:
            if element in prompt_instruction:
                print(f"✅ {element}")
            else:
                print(f"❌ {element}")
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 모든 테스트 실행
    test_standardized_prompt_instruction()
    test_context_aware_prompt_instruction()
    test_direct_function_call()
    
    print("\n\n🎉 모든 테스트 완료!") 