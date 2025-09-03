#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cursor Instruction: Context-Aware Intent Classification System Test
새로운 맥락 인식 의도 분류 시스템을 테스트합니다.
"""

from prompt_generator import extract_intent_and_purpose, process_user_request, classify_intent_with_context

def test_cursor_instruction_system():
    """
    Cursor Instruction 기반 Context-Aware Intent Classification 시스템을 테스트합니다.
    """
    print("🎯 Cursor Instruction: Context-Aware Intent Classification 시스템 테스트")
    print("=" * 80)
    
    # 테스트 케이스들 - 모호하고 비격식적인 입력들
    test_cases = [
        {
            "input": "그냥 사람 감성 자극하는 거 써줘",
            "chat_history": [
                {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
                {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"}
            ],
            "expected_intent": "marketing_copy"
        },
        {
            "input": "형, 이거 요즘 대세야?",
            "chat_history": [
                {"role": "user", "content": "AI 기술에 투자하려고 하는데"},
                {"role": "assistant", "content": "AI 기술 투자는 좋은 선택입니다."},
                {"role": "user", "content": "어떤 분야가 유망할까요?"}
            ],
            "expected_intent": "trend_verification"
        },
        {
            "input": "나도 할까?",
            "chat_history": [
                {"role": "user", "content": "친구가 창업을 시작했다고 하는데"},
                {"role": "assistant", "content": "창업에 대한 관심이 있으시군요."},
                {"role": "user", "content": "IT 스타트업이라고 해요"}
            ],
            "expected_intent": "decision_making"
        },
        {
            "input": "이거 괜찮아?",
            "chat_history": [
                {"role": "user", "content": "사업계획서를 작성했는데"},
                {"role": "assistant", "content": "사업계획서 작성 완료를 축하드립니다."},
                {"role": "user", "content": "시장 분석과 수익 모델을 포함했어요"}
            ],
            "expected_intent": "validation_seeking"
        },
        {
            "input": "형, 대박이야!",
            "chat_history": [
                {"role": "user", "content": "투자 제안서를 제출했는데"},
                {"role": "assistant", "content": "투자 제안서 제출을 축하드립니다."},
                {"role": "user", "content": "투자자들이 관심을 보이고 있어요"}
            ],
            "expected_intent": "casual_opinion"
        },
        {
            "input": "그냥 써줘",
            "chat_history": [
                {"role": "user", "content": "블로그 포스트를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 주제의 블로그 포스트인가요?"},
                {"role": "user", "content": "기술 트렌드에 대한 글이에요"}
            ],
            "expected_intent": "content_creation"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_case['input']}")
        print("-" * 70)
        
        # Context-Aware Intent Classification 테스트
        intent_analysis = extract_intent_and_purpose(test_case['input'], test_case['chat_history'])
        print(f"🎯 감지된 의도: {intent_analysis['intent']}")
        print(f"🎯 한글 분류: {intent_analysis['korean_classification']}")
        print(f"🎯 설명: {intent_analysis['description']}")
        print(f"🎯 맥락 인식: {intent_analysis['is_context_aware']}")
        
        # 예상 의도와 비교
        expected = test_case['expected_intent']
        actual = intent_analysis['intent']
        if actual == expected:
            print(f"✅ 정확한 의도 분류: {actual}")
        else:
            print(f"❌ 의도 분류 오류: 예상={expected}, 실제={actual}")
        
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

def test_context_aware_classification():
    """
    맥락 인식 분류 함수를 직접 테스트합니다.
    """
    print("\n🔍 Context-Aware Classification 함수 테스트")
    print("=" * 60)
    
    # 의도 매핑 정의
    intent_mapping = {
        "marketing_copy": {
            "keywords": ["마케팅", "광고", "홍보", "브랜딩"],
            "context_keywords": ["감성", "자극", "사람", "고객"],
            "korean_classification": "마케팅 카피 작성 요청",
            "description": "감성적이고 설득력 있는 마케팅 카피 작성 요청"
        },
        "content_creation": {
            "keywords": ["콘텐츠", "글", "작성"],
            "context_keywords": ["그냥", "써줘"],
            "korean_classification": "콘텐츠 작성 요청",
            "description": "일반적인 콘텐츠나 글 작성 요청"
        }
    }
    
    # 테스트 케이스
    test_cases = [
        {
            "input": "그냥 사람 감성 자극하는 거 써줘",
            "chat_history": [
                {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
                {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"}
            ]
        },
        {
            "input": "그냥 써줘",
            "chat_history": [
                {"role": "user", "content": "블로그 포스트를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 주제의 블로그 포스트인가요?"},
                {"role": "user", "content": "기술 트렌드에 대한 글이에요"}
            ]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 {i}: {test_case['input']}")
        
        intent, classification, description = classify_intent_with_context(
            test_case['input'], test_case['chat_history'], intent_mapping
        )
        
        print(f"  → 의도: {intent}")
        print(f"  → 분류: {classification}")
        print(f"  → 설명: {description}")

def test_ambiguous_pattern_detection():
    """
    모호한 패턴 감지를 테스트합니다.
    """
    print("\n🔍 모호한 패턴 감지 테스트")
    print("=" * 50)
    
    ambiguous_inputs = [
        "그냥 사람 감성 자극하는 거 써줘",
        "형, 이거 요즘 대세야?",
        "나도 할까?",
        "이거 괜찮아?",
        "형, 대박이야!",
        "그냥 써줘",
        "just write something",
        "people emotion stimulate",
        "this is cool",
        "should i do it?"
    ]
    
    for i, test_input in enumerate(ambiguous_inputs, 1):
        print(f"\n📝 테스트 {i}: {test_input}")
        intent_analysis = extract_intent_and_purpose(test_input)
        print(f"  → 의도: {intent_analysis['intent']}")
        print(f"  → 한글 분류: {intent_analysis['korean_classification']}")
        print(f"  → 맥락 인식: {intent_analysis['is_context_aware']}")

def test_marketing_context_detection():
    """
    마케팅 맥락 감지를 특별히 테스트합니다.
    """
    print("\n📢 마케팅 맥락 감지 테스트")
    print("=" * 50)
    
    marketing_test_cases = [
        {
            "input": "그냥 사람 감성 자극하는 거 써줘",
            "chat_history": [
                {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
                {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
                {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"}
            ]
        },
        {
            "input": "감성적으로 써줘",
            "chat_history": [
                {"role": "user", "content": "광고 문구를 작성해야 해요"},
                {"role": "assistant", "content": "어떤 제품의 광고 문구인가요?"},
                {"role": "user", "content": "화장품 브랜드 홍보용이에요"}
            ]
        },
        {
            "input": "사람 마음에 와닿게",
            "chat_history": [
                {"role": "user", "content": "브랜딩 메시지를 만들고 싶어요"},
                {"role": "assistant", "content": "어떤 브랜드의 메시지인가요?"},
                {"role": "user", "content": "스타트업 브랜딩용이에요"}
            ]
        }
    ]
    
    for i, test_case in enumerate(marketing_test_cases, 1):
        print(f"\n📝 마케팅 테스트 {i}: {test_case['input']}")
        intent_analysis = extract_intent_and_purpose(test_case['input'], test_case['chat_history'])
        print(f"  → 의도: {intent_analysis['intent']}")
        print(f"  → 분류: {intent_analysis['korean_classification']}")
        print(f"  → 맥락 인식: {intent_analysis['is_context_aware']}")
        
        if intent_analysis['intent'] == 'marketing_copy':
            print("  ✅ 마케팅 카피 의도로 정확히 분류됨!")
        else:
            print("  ❌ 마케팅 카피 의도 분류 실패")

def test_context_vs_keyword_classification():
    """
    맥락 기반 vs 키워드 기반 분류를 비교 테스트합니다.
    """
    print("\n🔄 맥락 기반 vs 키워드 기반 분류 비교 테스트")
    print("=" * 70)
    
    test_input = "그냥 사람 감성 자극하는 거 써줘"
    chat_history = [
        {"role": "user", "content": "마케팅 카피를 작성해야 하는데"},
        {"role": "assistant", "content": "어떤 제품이나 서비스의 마케팅 카피인가요?"},
        {"role": "user", "content": "새로운 커피 브랜드 홍보용이에요"}
    ]
    
    print(f"📝 테스트 입력: {test_input}")
    print(f"📋 채팅 히스토리: {len(chat_history)}개 메시지")
    
    # 맥락 기반 분류 (채팅 히스토리 포함)
    print(f"\n🎯 맥락 기반 분류:")
    context_aware = extract_intent_and_purpose(test_input, chat_history)
    print(f"  - 의도: {context_aware['intent']}")
    print(f"  - 분류: {context_aware['korean_classification']}")
    print(f"  - 맥락 인식: {context_aware['is_context_aware']}")
    print(f"  - 프롬프트 길이: {len(context_aware['system_prompt'])}")
    
    # 키워드 기반 분류 (채팅 히스토리 없음)
    print(f"\n📄 키워드 기반 분류:")
    keyword_based = extract_intent_and_purpose(test_input, None)
    print(f"  - 의도: {keyword_based['intent']}")
    print(f"  - 분류: {keyword_based['korean_classification']}")
    print(f"  - 맥락 인식: {keyword_based['is_context_aware']}")
    print(f"  - 프롬프트 길이: {len(keyword_based['system_prompt'])}")
    
    # 차이점 분석
    print(f"\n📊 차이점 분석:")
    if context_aware['is_context_aware'] and not keyword_based['is_context_aware']:
        print("  ✅ 맥락 기반 분류가 정상적으로 작동합니다!")
        print("  📈 프롬프트 길이 증가: +{}자".format(len(context_aware['system_prompt']) - len(keyword_based['system_prompt'])))
        
        if context_aware['intent'] == 'marketing_copy' and keyword_based['intent'] != 'marketing_copy':
            print("  🎯 맥락 기반 분류가 더 정확한 의도 감지!")
        else:
            print("  ℹ️ 두 분류 방식의 결과가 동일함")
    else:
        print("  ❌ 맥락 기반 분류에 문제가 있습니다.")

if __name__ == "__main__":
    test_cursor_instruction_system()
    test_context_aware_classification()
    test_ambiguous_pattern_detection()
    test_marketing_context_detection()
    test_context_vs_keyword_classification()
    print("\n🎉 Cursor Instruction: Context-Aware Intent Classification 시스템 테스트 완료!") 