#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
새로운 Intent 분류 기능 테스트 스크립트
"""

from classify_intent import classify_intent

def test_intent_classification():
    """새로운 intent 분류 기능을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "이 긴 보고서를 간결하게 요약해줘",
            "expected": "summary",
            "description": "요약 의도 테스트"
        },
        {
            "utterance": "이력서를 작성해야 해. AI 개발자 지원을 위한 자기소개서를 써야 해",
            "expected": "self_intro",
            "description": "자기소개 의도 테스트"
        },
        {
            "utterance": "고객 클레임에 대한 응대문을 작성해야 해. 불만 처리 사과문을 써야 해",
            "expected": "customer_reply",
            "description": "고객 응대 의도 테스트"
        },
        {
            "utterance": "정부지원사업에 제안서를 작성해야 해. AI 기반 솔루션을 제안할 거야",
            "expected": "grant_proposal",
            "description": "정부지원 제안서 의도 테스트"
        },
        {
            "utterance": "투자유치를 위한 피칭덱을 만들어야 해. 스타트업 비즈니스 모델을 설명해야 해",
            "expected": "startup_pitch",
            "description": "스타트업 피칭 의도 테스트"
        },
        {
            "utterance": "환경 정책에 대한 분석 보고서를 작성해야 해. 정책 제안도 포함해야 해",
            "expected": "policy_brief",
            "description": "정책 브리프 의도 테스트"
        },
        {
            "utterance": "제품 광고 문구를 작성해야 해. 마케팅 홍보 자료를 만들어야 해",
            "expected": "marketing_copy",
            "description": "마케팅 콘텐츠 의도 테스트"
        },
        {
            "utterance": "AI 강의 자료를 작성해야 해. 교육용 튜토리얼을 만들어야 해",
            "expected": "education_content",
            "description": "교육 콘텐츠 의도 테스트"
        },
        {
            "utterance": "오늘 날씨가 좋네요",
            "expected": "unknown",
            "description": "알 수 없는 의도 테스트"
        }
    ]
    
    print("🧪 새로운 Intent 분류 기능 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 결과: {test_case['expected']}")
        
        # Intent 분류 실행
        result = classify_intent(test_case['utterance'])
        
        print(f"✅ 실제 결과: {result}")
        
        # 결과 검증
        if result == test_case['expected']:
            print("🎉 테스트 통과!")
        else:
            print("❌ 테스트 실패!")
        
        print("-" * 60)
        print()
    
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    test_intent_classification() 