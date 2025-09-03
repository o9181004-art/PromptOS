#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[📌 REFINED CURSOR INSTRUCTION] 테스트
개선된 맥락 인식 의도 분류 시스템을 종합적으로 테스트합니다.
"""

from prompt_generator import (
    process_user_request, 
    evaluate_intent_confidence,
    advanced_intent_reconstruction,
    generate_enhanced_fallback_prompt,
    evaluate_reconstructed_confidence
)

def test_refined_cursor_instruction():
    """
    개선된 Cursor Instruction 시스템을 테스트합니다.
    """
    print("🎯 [📌 REFINED CURSOR INSTRUCTION] 개선된 맥락 인식 시스템 테스트")
    print("=" * 80)
    
    # 테스트 케이스들 - 다양한 모호하고 맥락 의존적인 입력들
    test_cases = [
        {
            "input": "그냥 사람 감성 자극하는 거 써줘",
            "chat_history": [
                {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
                {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"},
                {"role": "assistant", "content": "커피 브랜드 마케팅 카피를 작성해드리겠습니다."},
                {"role": "user", "content": "감성적으로 어필하고 싶어요"}
            ],
            "expected_intent": "marketing_copy",
            "description": "마케팅 맥락에서 감성적 마케팅 카피 요청"
        },
        {
            "input": "형, 이거 요즘 대세야?",
            "chat_history": [
                {"role": "user", "content": "AI 기술에 투자하려고 하는데"},
                {"role": "assistant", "content": "AI 기술 투자는 좋은 선택입니다."},
                {"role": "user", "content": "어떤 분야가 유망할까요?"},
                {"role": "assistant", "content": "머신러닝, 자연어처리, 컴퓨터 비전 등이 유망합니다."},
                {"role": "user", "content": "특정 AI 기술을 조사하고 있어요"}
            ],
            "expected_intent": "trend_verification",
            "description": "AI 투자 맥락에서 트렌드 검증 요청"
        },
        {
            "input": "나도 할까?",
            "chat_history": [
                {"role": "user", "content": "친구가 창업을 시작했다고 하는데"},
                {"role": "assistant", "content": "창업에 대한 관심이 있으시군요."},
                {"role": "user", "content": "IT 스타트업이라고 해요"},
                {"role": "assistant", "content": "IT 스타트업은 현재 많은 관심을 받고 있습니다."},
                {"role": "user", "content": "나도 비슷한 아이디어가 있어요"}
            ],
            "expected_intent": "decision_making",
            "description": "창업 맥락에서 행동 여부 판단 요청"
        },
        {
            "input": "이거 괜찮아?",
            "chat_history": [
                {"role": "user", "content": "사업계획서를 작성했는데"},
                {"role": "assistant", "content": "사업계획서 작성 완료를 축하드립니다."},
                {"role": "user", "content": "시장 분석과 수익 모델을 포함했어요"},
                {"role": "assistant", "content": "좋은 구성입니다. 더 구체적인 내용이 있나요?"},
                {"role": "user", "content": "투자자들에게 제출하려고 해요"}
            ],
            "expected_intent": "validation_seeking",
            "description": "사업계획서 맥락에서 검증 요청"
        },
        {
            "input": "형, 대박이야!",
            "chat_history": [
                {"role": "user", "content": "투자 제안서를 제출했는데"},
                {"role": "assistant", "content": "투자 제안서 제출을 축하드립니다."},
                {"role": "user", "content": "투자자들이 관심을 보이고 있어요"},
                {"role": "assistant", "content": "정말 좋은 소식이네요! 어떤 반응이었나요?"},
                {"role": "user", "content": "2차 미팅을 제안받았어요"}
            ],
            "expected_intent": "casual_opinion",
            "description": "투자 성공 맥락에서 기쁨 표현"
        },
        {
            "input": "그냥 써줘",
            "chat_history": [
                {"role": "user", "content": "블로그 포스트를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 주제의 블로그 포스트인가요?"},
                {"role": "user", "content": "기술 트렌드에 대한 글이에요"},
                {"role": "assistant", "content": "구체적인 기술 분야나 트렌드가 있나요?"},
                {"role": "user", "content": "AI와 머신러닝 관련이에요"}
            ],
            "expected_intent": "content_creation",
            "description": "블로그 포스트 맥락에서 콘텐츠 작성 요청"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_case['input']}")
        print(f"📋 설명: {test_case['description']}")
        print("-" * 70)
        
        # 전체 시스템 테스트
        try:
            result = process_user_request(test_case['input'], test_case['chat_history'])
            
            print(f"🎯 처리 방법: {result.get('method', 'unknown')}")
            print(f"🎯 템플릿 의도: {result['intent']}")
            print(f"🎯 Intent & Purpose 의도: {result['intent_analysis']['intent']}")
            print(f"🎯 신뢰도 점수: {result.get('confidence_score', 0.0):.3f}")
            print(f"🎯 한글 분류: {result['intent_analysis']['korean_classification']}")
            print(f"🎯 맥락 인식: {result['intent_analysis']['is_context_aware']}")
            print(f"🎯 맥락 사용: {result.get('context_used', False)}")
            
            # 사용자 메시지가 있는 경우
            if 'user_message' in result:
                print(f"🎯 사용자 메시지: {result['user_message']}")
            
            # 고급 분석 결과가 있는 경우
            if 'advanced_analysis' in result:
                print(f"🎯 고급 의도 추론: {result['advanced_analysis']['intent']}")
                print(f"🎯 고급 신뢰도: {result['advanced_analysis']['confidence']:.3f}")
                print(f"🎯 맥락 분석: {result['advanced_analysis'].get('context_analysis', {})}")
                print(f"🎯 한국어 응답: {result['advanced_analysis']['korean_response'][:100]}...")
            
            print(f"📊 최종 프롬프트 길이: {len(result['prompt'])}")
            
            # 예상 결과와 비교
            expected = test_case['expected_intent']
            actual = result.get('advanced_analysis', {}).get('intent', result['intent_analysis']['intent'])
            
            if actual == expected:
                print(f"✅ 정확한 의도 분류: {actual}")
            else:
                print(f"❌ 의도 분류 오류: 예상={expected}, 실제={actual}")
            
            # 신뢰도 평가
            confidence = result.get('confidence_score', 0.0)
            if confidence >= 0.7:
                print(f"✅ 높은 신뢰도: {confidence:.3f}")
            elif confidence >= 0.5:
                print(f"⚠️ 중간 신뢰도: {confidence:.3f}")
            else:
                print(f"❌ 낮은 신뢰도: {confidence:.3f}")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_enhanced_fallback_system():
    """
    향상된 fallback 시스템을 테스트합니다.
    """
    print("\n🔧 향상된 Fallback 시스템 테스트")
    print("=" * 60)
    
    # 채팅 히스토리가 없는 모호한 입력들
    test_cases = [
        {
            "input": "그냥 이거",
            "expected_purpose": "general",
            "description": "매우 모호한 입력"
        },
        {
            "input": "사업계획서 괜찮아?",
            "expected_purpose": "business",
            "description": "사업 관련 모호한 입력"
        },
        {
            "input": "마케팅 카피 써줘",
            "expected_purpose": "marketing",
            "description": "마케팅 관련 모호한 입력"
        },
        {
            "input": "이거 할까?",
            "expected_purpose": "decision",
            "description": "의사결정 관련 모호한 입력"
        },
        {
            "input": "요약해줘",
            "expected_purpose": "summary",
            "description": "요약 관련 모호한 입력"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Fallback 테스트 {i}: {test_case['input']}")
        print(f"📋 설명: {test_case['description']}")
        
        try:
            # Intent & Purpose 분석
            from prompt_generator import extract_intent_and_purpose
            intent_analysis = extract_intent_and_purpose(test_case['input'])
            
            # 향상된 fallback 프롬프트 생성
            fallback_prompt = generate_enhanced_fallback_prompt(test_case['input'], intent_analysis)
            
            print(f"🎯 분석된 의도: {intent_analysis['intent']}")
            print(f"🎯 한국어 분류: {intent_analysis['korean_classification']}")
            print(f"📊 Fallback 프롬프트 길이: {len(fallback_prompt)}")
            print(f"📄 Fallback 프롬프트 미리보기:")
            print(f"  {fallback_prompt[:200]}...")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_confidence_evaluation_improvements():
    """
    개선된 신뢰도 평가 시스템을 테스트합니다.
    """
    print("\n🔍 개선된 신뢰도 평가 시스템 테스트")
    print("=" * 60)
    
    test_cases = [
        {
            "template_intent": "business_plan",
            "intent_analysis": {"intent": "business_plan"},
            "user_input": "사업계획서를 작성해주세요",
            "expected_high": True,
            "description": "명확한 사업계획서 요청"
        },
        {
            "template_intent": "etc",
            "intent_analysis": {"intent": "general_inquiry"},
            "user_input": "그냥 이거",
            "expected_high": False,
            "description": "매우 모호한 입력"
        },
        {
            "template_intent": "marketing_copy",
            "intent_analysis": {"intent": "marketing_copy"},
            "user_input": "마케팅 카피를 작성해야 해요",
            "expected_high": True,
            "description": "명확한 마케팅 카피 요청"
        },
        {
            "template_intent": "etc",
            "intent_analysis": {"intent": "decision_making"},
            "user_input": "나도 할까?",
            "expected_high": False,
            "description": "모호한 의사결정 요청"
        },
        {
            "template_intent": "summary",
            "intent_analysis": {"intent": "summary"},
            "user_input": "이 문서를 요약해주세요.",
            "expected_high": True,
            "description": "명확한 요약 요청"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 신뢰도 테스트 {i}: {test_case['user_input']}")
        print(f"📋 설명: {test_case['description']}")
        
        confidence = evaluate_intent_confidence(
            test_case['template_intent'],
            test_case['intent_analysis'],
            test_case['user_input']
        )
        
        print(f"  → 신뢰도 점수: {confidence:.3f}")
        
        if test_case['expected_high']:
            if confidence >= 0.7:
                print("  ✅ 예상대로 높은 신뢰도")
            else:
                print("  ❌ 예상과 다르게 낮은 신뢰도")
        else:
            if confidence < 0.7:
                print("  ✅ 예상대로 낮은 신뢰도")
            else:
                print("  ❌ 예상과 다르게 높은 신뢰도")

def test_advanced_reconstruction_improvements():
    """
    개선된 고급 의도 재구성 시스템을 테스트합니다.
    """
    print("\n🔧 개선된 고급 의도 재구성 시스템 테스트")
    print("=" * 60)
    
    test_input = "그냥 사람 감성 자극하는 거 써줘"
    chat_history = [
        {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
        {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
        {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"},
        {"role": "assistant", "content": "커피 브랜드 마케팅 카피를 작성해드리겠습니다."},
        {"role": "user", "content": "감성적으로 어필하고 싶어요"}
    ]
    
    print(f"📝 테스트 입력: {test_input}")
    print(f"📋 채팅 히스토리: {len(chat_history)}개 메시지")
    
    try:
        result = advanced_intent_reconstruction(test_input, chat_history)
        
        print(f"\n🎯 고급 분석 결과:")
        print(f"  - 의도: {result['intent']}")
        print(f"  - 톤: {result['conditions']['tone']}")
        print(f"  - 시제: {result['conditions']['tense']}")
        print(f"  - 대상: {result['conditions']['audience']}")
        print(f"  - 신뢰도: {result['confidence']:.3f}")
        print(f"  - 맥락 분석: {result.get('context_analysis', {})}")
        print(f"  - 한국어 응답 길이: {len(result['korean_response'])}")
        print(f"  - LLM 프롬프트 길이: {len(result['llm_prompt'])}")
        
        print(f"\n📄 한국어 응답 미리보기:")
        print(f"  {result['korean_response'][:200]}...")
        
        # 재구성 신뢰도 평가 테스트
        reconstructed_confidence = evaluate_reconstructed_confidence(
            test_input, chat_history, result
        )
        print(f"\n🔍 재구성 신뢰도 평가: {reconstructed_confidence:.3f}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_refined_cursor_instruction()
    test_enhanced_fallback_system()
    test_confidence_evaluation_improvements()
    test_advanced_reconstruction_improvements()
    print("\n🎉 [📌 REFINED CURSOR INSTRUCTION] 개선된 맥락 인식 시스템 테스트 완료!") 