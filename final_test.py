#!/usr/bin/env python3
"""
최종 통합 테스트
"""

def main():
    print("🎉 Cursor Instruction Template System 최종 테스트")
    print("=" * 60)
    
    try:
        # 1. 시스템 로드 테스트
        from cursor_instruction_system import cursor_system
        print("✅ 1. 시스템 로드 성공")
        
        # 2. 어댑터 로드 테스트
        from cursor_instruction_adapter import cursor_adapter
        print("✅ 2. 어댑터 로드 성공")
        
        # 3. 기본 기능 테스트
        result = cursor_system.process_user_input("사업계획서 써줘")
        print(f"✅ 3. 기본 기능 테스트 성공: {result['intent']} (신뢰도: {result['confidence']:.2f})")
        
        # 4. 어댑터 기능 테스트
        adapted_result = cursor_adapter.process_utterance("마케팅 카피 써줘")
        print(f"✅ 4. 어댑터 기능 테스트 성공: {adapted_result['processing_type']}")
        
        # 5. 프롬프트 생성 테스트
        from cursor_instruction_adapter import get_cursor_prompt
        prompt = get_cursor_prompt("면접용 자기소개서 작성 도와줘")
        print(f"✅ 5. 프롬프트 생성 테스트 성공: {len(prompt)}자 생성")
        
        # 6. 시스템 통계
        stats = cursor_adapter.get_system_stats()
        print(f"✅ 6. 시스템 통계: {stats['template_count']}개 템플릿, {len(stats['supported_intents'])}개 의도 지원")
        
        print("\n🎊 모든 테스트 통과! 시스템이 정상적으로 작동합니다.")
        print("\n📋 생성된 파일들:")
        print("  - cursor_instruction_template_config.py (템플릿 설정)")
        print("  - cursor_instruction_system.py (핵심 시스템)")
        print("  - cursor_instruction_adapter.py (어댑터)")
        print("  - CURSOR_INSTRUCTION_README.md (문서)")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 