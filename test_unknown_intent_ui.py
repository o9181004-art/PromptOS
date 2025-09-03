#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unknown Intent UI 테스트 스크립트
"""

from classify_intent import classify_intent

def test_unknown_intent():
    """Unknown intent 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "오늘 날씨가 좋네요",
            "description": "일반적인 대화"
        },
        {
            "utterance": "안녕하세요",
            "description": "인사말"
        },
        {
            "utterance": "무엇을 도와드릴까요?",
            "description": "질문"
        },
        {
            "utterance": "창의적인 아이디어를 구체화하고 싶어",
            "description": "모호한 요청"
        }
    ]
    
    print("🧪 Unknown Intent UI 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # Intent 분류
        result = classify_intent(test_case['utterance'])
        
        print(f"🎯 분류 결과: {result}")
        
        if result == "unknown":
            print("✅ Unknown intent로 올바르게 분류됨")
        else:
            print(f"⚠️ 예상과 다름: {result}")
        
        print("-" * 50)
        print()
    
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    test_unknown_intent() 