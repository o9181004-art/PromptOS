#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FallbackManager 기능 테스트 스크립트
"""

from fallback_manager import fallback_manager

def test_fallback_manager():
    """FallbackManager의 기능을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "창의적인 마케팅 콘텐츠를 만들어줘",
            "intent": "marketing_content",
            "description": "존재하지 않는 intent로 템플릿 없음 상황 테스트"
        },
        {
            "utterance": "고객을 위한 정중한 이메일을 작성해줘",
            "intent": "email_writing", 
            "description": "이메일 작성 요청 테스트"
        },
        {
            "utterance": "학생들을 위한 간단한 설명이 필요해",
            "intent": "education_content",
            "description": "교육 콘텐츠 요청 테스트"
        },
        {
            "utterance": "AI 기반 제안서를 정부에 제출할거야",
            "intent": "unknown",
            "description": "unknown intent로 테스트"
        }
    ]
    
    print("🧪 FallbackManager 기능 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 사용자 발화: {test_case['utterance']}")
        print(f"🎯 Intent: {test_case['intent']}")
        print("🔄 LLM 프롬프트 생성 중...")
        
        # LLM 프롬프트 생성
        generated_prompt = fallback_manager.generate_prompt_with_llm(
            test_case['utterance'], 
            test_case['intent']
        )
        
        print(f"✅ 생성된 프롬프트:")
        print("-" * 50)
        print(generated_prompt)
        print("-" * 50)
        print("\n")
    
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    test_fallback_manager() 