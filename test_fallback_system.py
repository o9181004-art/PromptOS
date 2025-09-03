#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PromptOS Fallback System Test
목적 지향적 fallback 시스템을 직접 테스트합니다.
"""

from prompt_generator import fallback_prompt_from_topic, process_user_request

def test_fallback_system():
    """
    새로운 fallback 시스템을 테스트합니다.
    """
    print("🚀 PromptOS 목적 지향적 Fallback 시스템 테스트")
    print("=" * 60)
    
    # 테스트 케이스들 - 의도 분류가 실패할 수 있는 모호한 입력들
    test_cases = [
        "I have a great idea. What should I do with it?",
        "startup funding needed",
        "마케팅 전략이 필요해",
        "기술 개발 방법을 알려줘",
        "투자 유치하고 싶어",
        "help me with my business",
        "어떻게 해야 할지 모르겠어",
        "좋은 아이디어가 있는데 어떻게 발전시켜야 할까?",
        "비즈니스 모델을 만들고 싶어",
        "앱 개발하고 싶은데 어떻게 시작해야 할까?",
        "브랜딩 전략이 필요해",
        "크라우드펀딩으로 자금을 모으고 싶어",
        "특허 출원하고 싶은데 어떻게 해야 할까?",
        "무작정 시작했는데 방향을 잡고 싶어",
        "혁신적인 아이디어가 있는데 상용화하고 싶어"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {test_input}")
        print("-" * 50)
        
        # 1. 직접 fallback 프롬프트 생성 테스트
        fallback_prompt = fallback_prompt_from_topic(test_input)
        print(f"🔍 Fallback 프롬프트 길이: {len(fallback_prompt)}")
        print(f"📄 Fallback 프롬프트 미리보기:")
        print(fallback_prompt[:200] + "..." if len(fallback_prompt) > 200 else fallback_prompt)
        
        # 2. 전체 시스템 테스트 (의도 분류 결과도 확인)
        try:
            result = process_user_request(test_input)
            print(f"🎯 의도 분류 결과: {result['intent']}")
            print(f"⚙️ 조건 추출: {result['conditions']}")
            print(f"📊 최종 프롬프트 길이: {len(result['prompt'])}")
            
            # fallback이 사용되었는지 확인
            if result['intent'] == 'etc':
                print("✅ Fallback 시스템이 정상 작동했습니다!")
            else:
                print("ℹ️ 의도 분류가 성공하여 기본 템플릿이 사용되었습니다.")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print()

def test_keyword_mapping():
    """
    키워드 매핑 테이블을 테스트합니다.
    """
    print("\n🔍 키워드 매핑 테이블 테스트")
    print("=" * 40)
    
    # 각 주제별 키워드 테스트
    test_keywords = {
        "startup": ["startup", "창업", "사업", "비즈니스", "business"],
        "idea": ["idea", "아이디어", "concept", "개념", "혁신"],
        "funding": ["funding", "투자", "investment", "자금", "money"],
        "proposal": ["proposal", "제안서", "기획서", "plan", "계획"],
        "marketing": ["marketing", "마케팅", "홍보", "promotion", "광고"],
        "technology": ["technology", "기술", "개발", "development", "프로그래밍"],
        "general_help": ["help", "도움", "어떻게", "how", "방법"]
    }
    
    for topic, keywords in test_keywords.items():
        print(f"\n📌 주제: {topic}")
        for keyword in keywords:
            fallback_prompt = fallback_prompt_from_topic(keyword)
            print(f"  - '{keyword}' → 길이: {len(fallback_prompt)}")
            if "사용자가" in fallback_prompt:
                print(f"    ✅ 정상 작동")
            else:
                print(f"    ❌ 오류")

if __name__ == "__main__":
    test_fallback_system()
    test_keyword_mapping()
    print("\n🎉 Fallback 시스템 테스트 완료!") 