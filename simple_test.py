#!/usr/bin/env python3
"""
간단한 Cursor Instruction System 테스트
"""

try:
    from cursor_instruction_system import cursor_system
    print("✅ 시스템 로드 성공")
    
    # 테스트 입력
    test_input = "사업계획서 써줘"
    print(f"🧪 테스트 입력: {test_input}")
    
    # 처리
    result = cursor_system.process_user_input(test_input)
    
    # 결과 출력
    print(f"🎯 의도: {result['intent']}")
    print(f"📊 신뢰도: {result['confidence']:.2f}")
    print(f"🔧 분류 방법: {result['classification_method']}")
    print(f"❓ 명확화 필요: {result['requires_clarification']}")
    
    if result['followup_questions']:
        print("💬 후속 질문:")
        for i, question in enumerate(result['followup_questions'], 1):
            print(f"  {i}. {question}")
    
    print("✅ 테스트 완료")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc() 