#!/usr/bin/env python3
"""
Cursor Instruction System 테스트 스크립트
"""

from cursor_instruction_system import cursor_system

def test_single_input(user_input: str):
    """단일 입력 테스트"""
    print(f"\n🧪 테스트 입력: {user_input}")
    print("-" * 50)
    
    result = cursor_system.process_user_input(user_input)
    
    print(f"🎯 의도: {result['intent']}")
    print(f"📊 신뢰도: {result['confidence']:.2f}")
    print(f"🔧 분류 방법: {result['classification_method']}")
    print(f"❓ 명확화 필요: {result['requires_clarification']}")
    
    if result['followup_questions']:
        print(f"💬 후속 질문:")
        for i, question in enumerate(result['followup_questions'], 1):
            print(f"  {i}. {question}")

def main():
    """메인 테스트 함수"""
    print("🚀 Cursor Instruction System 테스트")
    print("=" * 60)
    
    test_cases = [
        "사업계획서 써줘",
        "IR 자료 초안 좀 만들어줘",
        "마케팅 카피 써줘",
        "면접용 자기소개서 작성 도와줘",
        "회의 요약해줘",
        "코드 실행해봐",
        "그냥 써줘",
        "이거 어떻게 생각해?"
    ]
    
    for test_input in test_cases:
        test_single_input(test_input)
        print()

if __name__ == "__main__":
    main() 