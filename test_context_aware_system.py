#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Context-Aware Prompt Reconstruction System Test
새로운 맥락 인식 프롬프트 재구성 시스템을 테스트합니다.
"""

from prompt_generator import extract_intent_and_purpose, process_user_request, format_chat_history

def test_context_aware_system():
    """
    Context-Aware Prompt Reconstruction 시스템을 테스트합니다.
    """
    print("🎯 Context-Aware Prompt Reconstruction 시스템 테스트")
    print("=" * 70)
    
    # 테스트 케이스들 - 모호하고 유머러스한 입력들
    test_cases = [
        {
            "input": "형, 이거 요즘 대세야?",
            "chat_history": [
                {"role": "user", "content": "AI 기술에 투자하려고 하는데 어떤 분야가 좋을까요?"},
                {"role": "assistant", "content": "AI 기술 투자 분야로는 머신러닝, 자연어처리, 컴퓨터 비전 등이 있습니다."},
                {"role": "user", "content": "그럼 챗GPT 같은 기술은 어떤가요?"}
            ]
        },
        {
            "input": "나도 할까?",
            "chat_history": [
                {"role": "user", "content": "친구가 창업을 시작했다고 하는데"},
                {"role": "assistant", "content": "창업에 대한 관심이 있으시군요. 어떤 분야의 창업인가요?"},
                {"role": "user", "content": "IT 스타트업이라고 해요"}
            ]
        },
        {
            "input": "이거 괜찮아?",
            "chat_history": [
                {"role": "user", "content": "사업계획서를 작성했는데"},
                {"role": "assistant", "content": "사업계획서 작성 완료를 축하드립니다. 어떤 내용을 포함했나요?"},
                {"role": "user", "content": "시장 분석과 수익 모델을 포함했어요"}
            ]
        },
        {
            "input": "형, 대박이야!",
            "chat_history": [
                {"role": "user", "content": "투자 제안서를 제출했는데"},
                {"role": "assistant", "content": "투자 제안서 제출을 축하드립니다. 어떤 반응을 받으셨나요?"},
                {"role": "user", "content": "투자자들이 관심을 보이고 있어요"}
            ]
        },
        {
            "input": "이거 요즘 트렌드야?",
            "chat_history": [
                {"role": "user", "content": "블록체인 기술에 대해 알아보고 있는데"},
                {"role": "assistant", "content": "블록체인은 분산원장 기술로 다양한 분야에서 활용되고 있습니다."},
                {"role": "user", "content": "NFT도 블록체인 기술인가요?"}
            ]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_case['input']}")
        print("-" * 60)
        
        # Context-Aware Intent & Purpose Extraction 테스트
        intent_analysis = extract_intent_and_purpose(test_case['input'], test_case['chat_history'])
        print(f"🎯 감지된 의도: {intent_analysis['intent']}")
        print(f"🎯 한글 분류: {intent_analysis['korean_classification']}")
        print(f"🎯 설명: {intent_analysis['description']}")
        print(f"🎯 맥락 인식: {intent_analysis['is_context_aware']}")
        print(f"📄 시스템 프롬프트:")
        print(intent_analysis['system_prompt'])
        
        # 전체 시스템 테스트
        try:
            result = process_user_request(test_case['input'], test_case['chat_history'])
            print(f"📊 전체 시스템 결과:")
            print(f"  - 템플릿 의도: {result['intent']}")
            print(f"  - Intent & Purpose 의도: {result['intent_analysis']['intent']}")
            print(f"  - 한글 분류: {result['intent_analysis']['korean_classification']}")
            print(f"  - 맥락 인식: {result['intent_analysis']['is_context_aware']}")
            print(f"  - 최종 프롬프트 길이: {len(result['prompt'])}")
            
            # 어떤 시스템이 사용되었는지 확인
            if result['intent_analysis']['is_context_aware']:
                print("✅ Context-Aware 프롬프트가 사용되었습니다!")
            elif result['intent'] == 'etc' or result['intent_analysis']['intent'] != 'general_inquiry':
                print("✅ Intent & Purpose 기반 프롬프트가 사용되었습니다!")
            else:
                print("ℹ️ 기존 템플릿 기반 프롬프트가 사용되었습니다.")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_chat_history_formatting():
    """
    채팅 히스토리 포맷팅을 테스트합니다.
    """
    print("\n📋 채팅 히스토리 포맷팅 테스트")
    print("=" * 50)
    
    # 다양한 형태의 채팅 히스토리 테스트
    test_histories = [
        # 빈 히스토리
        [],
        
        # 딕셔너리 형태
        [
            {"role": "user", "content": "안녕하세요"},
            {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"},
            {"role": "user", "content": "사업계획서 작성에 대해 문의하고 싶어요"}
        ],
        
        # 문자열 형태
        [
            "사업계획서를 작성하고 싶어요",
            "어떤 분야의 사업계획서인가요?",
            "IT 스타트업 분야입니다"
        ],
        
        # 혼합 형태
        [
            {"role": "user", "content": "투자 제안서를 작성해야 해요"},
            "어떤 투자자에게 제안하시나요?",
            {"role": "assistant", "content": "투자자 유형에 따라 제안서 내용이 달라질 수 있습니다."}
        ]
    ]
    
    for i, history in enumerate(test_histories, 1):
        print(f"\n📝 히스토리 {i}:")
        formatted = format_chat_history(history)
        print(formatted)

def test_vague_pattern_detection():
    """
    모호한 패턴 감지를 테스트합니다.
    """
    print("\n🔍 모호한 패턴 감지 테스트")
    print("=" * 40)
    
    vague_inputs = [
        "형, 이거 요즘 대세야?",
        "나도 할까?",
        "이거 괜찮아?",
        "형, 대박이야!",
        "이거 요즘 트렌드야?",
        "bro, this is cool",
        "should i do it?",
        "is this ok?",
        "wow, awesome!",
        "trending now?"
    ]
    
    for i, test_input in enumerate(vague_inputs, 1):
        print(f"\n📝 테스트 {i}: {test_input}")
        intent_analysis = extract_intent_and_purpose(test_input)
        print(f"  → 의도: {intent_analysis['intent']}")
        print(f"  → 한글 분류: {intent_analysis['korean_classification']}")
        print(f"  → 맥락 인식: {intent_analysis['is_context_aware']}")

def test_context_aware_vs_standard():
    """
    맥락 인식 vs 표준 프롬프트를 비교 테스트합니다.
    """
    print("\n🔄 맥락 인식 vs 표준 프롬프트 비교 테스트")
    print("=" * 60)
    
    test_input = "형, 이거 요즘 대세야?"
    chat_history = [
        {"role": "user", "content": "AI 기술에 투자하려고 하는데"},
        {"role": "assistant", "content": "AI 기술 투자는 좋은 선택입니다."},
        {"role": "user", "content": "어떤 분야가 유망할까요?"}
    ]
    
    print(f"📝 테스트 입력: {test_input}")
    print(f"📋 채팅 히스토리: {len(chat_history)}개 메시지")
    
    # 맥락 인식 프롬프트
    print(f"\n🎯 맥락 인식 프롬프트:")
    context_aware = extract_intent_and_purpose(test_input, chat_history)
    print(f"  - 의도: {context_aware['intent']}")
    print(f"  - 분류: {context_aware['korean_classification']}")
    print(f"  - 맥락 인식: {context_aware['is_context_aware']}")
    print(f"  - 프롬프트 길이: {len(context_aware['system_prompt'])}")
    
    # 표준 프롬프트
    print(f"\n📄 표준 프롬프트:")
    standard = extract_intent_and_purpose(test_input, None)
    print(f"  - 의도: {standard['intent']}")
    print(f"  - 분류: {standard['korean_classification']}")
    print(f"  - 맥락 인식: {standard['is_context_aware']}")
    print(f"  - 프롬프트 길이: {len(standard['system_prompt'])}")
    
    # 차이점 분석
    print(f"\n📊 차이점 분석:")
    if context_aware['is_context_aware'] and not standard['is_context_aware']:
        print("  ✅ 맥락 인식 시스템이 정상적으로 작동합니다!")
        print("  📈 프롬프트 길이 증가: +{}자".format(len(context_aware['system_prompt']) - len(standard['system_prompt'])))
    else:
        print("  ❌ 맥락 인식 시스템에 문제가 있습니다.")

if __name__ == "__main__":
    test_context_aware_system()
    test_chat_history_formatting()
    test_vague_pattern_detection()
    test_context_aware_vs_standard()
    print("\n🎉 Context-Aware Prompt Reconstruction 시스템 테스트 완료!") 