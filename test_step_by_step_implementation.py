#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step-by-Step Implementation 테스트
사용자의 요구사항에 따른 4단계 구현이 올바르게 작동하는지 테스트합니다.

Step 1: Intent Detection - 명확한 목적이 있는 경우 의도를 명시적으로 분류
Step 2: Template Matching - 분류된 의도와 가장 적합한 템플릿 매칭
Step 3: Purpose Inference - 목적이 모호한 경우 LLM 기반 추론
Step 4: Fallback Handling - 템플릿 매칭이 없는 경우 기본 지시사항
"""

from prompt_generator import (
    process_user_request,
    generate_standardized_prompt_instruction,
    generate_fallback_instruction,
    extract_intent_and_purpose
)

def test_step_by_step_implementation():
    """
    Step-by-Step 구현을 테스트합니다.
    """
    print("🎯 Step-by-Step Implementation 테스트")
    print("=" * 80)

    # 테스트 케이스들
    test_cases = [
        {
            "input": "IR 자료 초안 좀 만들어줘",
            "description": "Step 1 & 2: 명확한 목적 - IR 문서 작성",
            "expected_step": "Step 2: Template Matching",
            "expected_intent": "investor_IR_document"
        },
        {
            "input": "사업계획서 써줘",
            "description": "Step 1 & 2: 명확한 목적 - 사업계획서 작성",
            "expected_step": "Step 2: Template Matching",
            "expected_intent": "business_plan"
        },
        {
            "input": "마케팅 카피 써줘",
            "description": "Step 1 & 2: 명확한 목적 - 마케팅 카피 작성",
            "expected_step": "Step 2: Template Matching",
            "expected_intent": "marketing_copy"
        },
        {
            "input": "그냥 써줘",
            "description": "Step 4: 모호한 목적 - Fallback Handling",
            "expected_step": "Step 4: Fallback Handling",
            "expected_intent": "general_inquiry"
        },
        {
            "input": "이거 어떻게 생각해?",
            "description": "Step 4: 모호한 목적 - Fallback Handling",
            "expected_step": "Step 4: Fallback Handling",
            "expected_intent": "general_inquiry"
        },
        {
            "input": "돈이 될까?",
            "description": "Step 4: 모호한 목적 - Fallback Handling",
            "expected_step": "Step 4: Fallback Handling",
            "expected_intent": "general_inquiry"
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
            step = result.get("step", "Unknown")
            
            print(f"✅ 실행된 단계: {step}")
            print(f"✅ 의도 분류: {intent}")
            print(f"✅ 신뢰도: {confidence_score:.2f}")
            print(f"✅ 처리 방법: {method}")
            print(f"✅ 예상 단계: {test_case['expected_step']}")
            print(f"✅ 예상 의도: {test_case['expected_intent']}")
            
            # 단계 일치 여부 확인
            if step == test_case['expected_step']:
                print("🎯 단계 실행 정확!")
            else:
                print(f"⚠️  단계 불일치: 예상={test_case['expected_step']}, 실제={step}")
            
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
                
            if "Output must be in Korean" in prompt_instruction:
                print("✅ 한국어 출력 요구사항 포함")
            else:
                print("❌ 한국어 출력 요구사항 누락")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_context_aware_purpose_inference():
    """
    Step 3: Purpose Inference - 맥락 인식 목적 추론을 테스트합니다.
    """
    print("\n\n🎯 Step 3: Purpose Inference 테스트")
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
            "description": "IR 맥락에서의 초안 요청 - Step 3 실행 예상",
            "expected_step": "Step 3: Purpose Inference",
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
            "description": "창업 맥락에서의 계획서 요청 - Step 3 실행 예상",
            "expected_step": "Step 3: Purpose Inference",
            "expected_intent": "business_plan"
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
            step = result.get("step", "Unknown")
            context_used = result.get("context_used", False)
            
            print(f"✅ 실행된 단계: {step}")
            print(f"✅ 의도 분류: {intent}")
            print(f"✅ 신뢰도: {confidence_score:.2f}")
            print(f"✅ 처리 방법: {method}")
            print(f"✅ 맥락 사용: {context_used}")
            print(f"✅ 예상 단계: {test_case['expected_step']}")
            print(f"✅ 예상 의도: {test_case['expected_intent']}")
            
            # 단계 일치 여부 확인
            if step == test_case['expected_step']:
                print("🎯 단계 실행 정확!")
            else:
                print(f"⚠️  단계 불일치: 예상={test_case['expected_step']}, 실제={step}")
            
            # 의도 일치 여부 확인
            if intent == test_case['expected_intent']:
                print("🎯 의도 분류 정확!")
            else:
                print(f"⚠️  의도 분류 불일치: 예상={test_case['expected_intent']}, 실제={intent}")
            
            print("\n📋 생성된 프롬프트 지시사항:")
            print(prompt_instruction)
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_fallback_instruction():
    """
    Step 4: Fallback Handling - 기본 지시사항 생성을 테스트합니다.
    """
    print("\n\n🔧 Step 4: Fallback Handling 테스트")
    print("=" * 80)

    # Fallback 테스트 케이스들
    test_cases = [
        {
            "input": "그냥 써줘",
            "description": "모호한 요청"
        },
        {
            "input": "이거 어떻게 생각해?",
            "description": "의견 요청"
        },
        {
            "input": "돈이 될까?",
            "description": "수익성 질문"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Fallback 테스트 {i}: {test_case['description']}")
        print(f"입력: {test_case['input']}")
        print("-" * 60)

        try:
            # 의도 분석
            intent_analysis = extract_intent_and_purpose(test_case['input'])
            
            # Fallback 지시사항 생성
            fallback_instruction = generate_fallback_instruction(test_case['input'], intent_analysis)
            
            print(f"의도 분석: {intent_analysis['intent']}")
            print("\n📋 생성된 Fallback 지시사항:")
            print(fallback_instruction)
            
            # 형식 검증
            required_elements = [
                "📋 [Prompt Instruction Format]",
                "User utterance:",
                "Intent: general_inquiry",
                "Reconstructed Purpose:",
                "Instruction:",
                "Output must be in Korean",
                "추가 지침:"
            ]
            
            print("\n🔍 Fallback 형식 검증:")
            for element in required_elements:
                if element in fallback_instruction:
                    print(f"✅ {element}")
                else:
                    print(f"❌ {element}")
                    
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_step_summary():
    """
    각 단계별 요약을 제공합니다.
    """
    print("\n\n📊 Step-by-Step 구현 요약")
    print("=" * 80)
    
    steps = [
        {
            "step": "Step 1: Intent Detection",
            "description": "명확한 목적이 있는 경우 의도를 명시적으로 분류",
            "example": "IR 자료 초안 좀 만들어줘 → investor_IR_document",
            "method": "classify_intent() + extract_intent_and_purpose()"
        },
        {
            "step": "Step 2: Template Matching", 
            "description": "분류된 의도와 가장 적합한 미리 정의된 프롬프트 템플릿 매칭",
            "example": "신뢰도 >= 0.7 → 구조화된 템플릿 적용",
            "method": "generate_standardized_prompt_instruction()"
        },
        {
            "step": "Step 3: Purpose Inference",
            "description": "목적이 모호한 경우 이전 대화 맥락을 사용하여 LLM 기반 추론",
            "example": "신뢰도 < 0.7 + 채팅 히스토리 있음 → LLM 기반 추론",
            "method": "advanced_intent_reconstruction()"
        },
        {
            "step": "Step 4: Fallback Handling",
            "description": "템플릿 매칭이 없는 경우 기본 지시사항으로 LLM에 전달",
            "example": "신뢰도 < 0.7 + 채팅 히스토리 없음 → 기본 fallback",
            "method": "generate_fallback_instruction()"
        }
    ]
    
    for i, step_info in enumerate(steps, 1):
        print(f"\n{i}. {step_info['step']}")
        print(f"   📝 {step_info['description']}")
        print(f"   💡 예시: {step_info['example']}")
        print(f"   🔧 방법: {step_info['method']}")

if __name__ == "__main__":
    # 모든 테스트 실행
    test_step_by_step_implementation()
    test_context_aware_purpose_inference()
    test_fallback_instruction()
    test_step_summary()
    
    print("\n\n🎉 Step-by-Step 구현 테스트 완료!")
    print("\n📋 요약:")
    print("✅ Step 1: Intent Detection - 명확한 목적 분류")
    print("✅ Step 2: Template Matching - 구조화된 템플릿 적용") 
    print("✅ Step 3: Purpose Inference - LLM 기반 맥락 추론")
    print("✅ Step 4: Fallback Handling - 기본 지시사항 생성")
    print("✅ 모든 출력은 한국어로 생성")
    print("✅ 명확한 목적 = 구조화된 템플릿 적용")
    print("✅ 암묵적 목적 = LLM 추론 + 명확화 안내") 