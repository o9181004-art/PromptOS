#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
개선된 Fallback 프롬프트 템플릿 테스트 스크립트
"""

from fallback_manager import fallback_manager

def test_fallback_prompt():
    """개선된 fallback 프롬프트 템플릿을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "AI 기반 제안서를 정부에 제출할거야",
            "intent": "grant_proposal",
            "description": "정부지원 제안서 요청"
        },
        {
            "utterance": "스타트업 투자유치를 위한 피칭덱을 만들어야 해",
            "intent": "startup_pitch",
            "description": "스타트업 피칭 요청"
        },
        {
            "utterance": "환경 정책에 대한 분석 보고서를 작성해야 해",
            "intent": "policy_brief",
            "description": "정책 브리프 요청"
        },
        {
            "utterance": "새로운 제품을 위한 마케팅 콘텐츠를 만들어야 해",
            "intent": "marketing_copy",
            "description": "마케팅 콘텐츠 요청"
        },
        {
            "utterance": "학생들을 위한 AI 교육 자료를 만들어야 해",
            "intent": "education_content",
            "description": "교육 콘텐츠 요청"
        },
        {
            "utterance": "창의적인 아이디어를 구체화하고 싶어",
            "intent": "unknown",
            "description": "알 수 없는 의도 요청"
        }
    ]
    
    print("🧪 개선된 Fallback 프롬프트 템플릿 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 Intent: {test_case['intent']}")
        print("🔄 프롬프트 생성 중...")
        
        # Fallback 프롬프트 생성
        generated_prompt = fallback_manager.generate_prompt_with_llm(
            test_case['utterance'], 
            test_case['intent']
        )
        
        print(f"✅ 생성된 프롬프트:")
        print("-" * 50)
        print(generated_prompt)
        print("-" * 50)
        print()
    
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    test_fallback_prompt() 