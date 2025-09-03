#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
슬롯 추출 기능 테스트 스크립트
"""

from prompt_builder import extract_slots_with_llm, prompt_missing_values
from classify_intent import classify_intent

def test_slot_extraction():
    """슬롯 추출 기능을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "AI 개발자로 취업하고 싶어서 자기소개서를 써야 해. 파이썬과 머신러닝에 능숙하고, 스타트업에서 3년간 일한 경험이 있어. 앞으로는 AI 솔루션을 개발하는 것이 목표야.",
            "intent": "self_intro",
            "expected_slots": ["motivation", "strengths", "experience", "goals"]
        },
        {
            "utterance": "고객이 제품 품질에 불만을 가지고 있어. 정중하게 사과하고 해결책을 제시해야 해.",
            "intent": "customer_reply", 
            "expected_slots": ["situation", "tone", "urgency"]
        },
        {
            "utterance": "이 긴 보고서를 간결하게 요약해서 상사에게 전달해야 해.",
            "intent": "summary",
            "expected_slots": ["content", "tone", "audience"]
        }
    ]
    
    print("🧪 슬롯 추출 기능 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['utterance']}")
        print(f"🎯 Intent: {test_case['intent']}")
        
        # LLM 슬롯 추출 테스트
        extracted_slots = extract_slots_with_llm(
            test_case['utterance'], 
            test_case['intent'], 
            test_case['expected_slots']
        )
        
        print(f"🤖 추출된 슬롯: {extracted_slots}")
        print("-" * 50)
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    test_slot_extraction() 