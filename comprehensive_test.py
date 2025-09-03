#!/usr/bin/env python3
"""
포괄적인 Cursor Instruction System 테스트
"""

from cursor_instruction_system import cursor_system

def test_comprehensive():
    """포괄적인 테스트"""
    print("🚀 Cursor Instruction System 포괄 테스트")
    print("=" * 60)
    
    test_cases = [
        ("사업계획서 써줘", "명시적 의도 - 사업계획서"),
        ("IR 자료 초안 좀 만들어줘", "명시적 의도 - IR 문서"),
        ("마케팅 카피 써줘", "명시적 의도 - 마케팅 카피"),
        ("면접용 자기소개서 작성 도와줘", "명시적 의도 - 자기소개서"),
        ("회의 요약해줘", "명시적 의도 - 회의 요약"),
        ("코드 실행해봐", "명시적 의도 - 코드 실행"),
        ("그냥 써줘", "모호한 의도"),
        ("이거 어떻게 생각해?", "모호한 의도"),
        ("투자자에게 보낼 자료", "유사 의도 - IR 관련"),
        ("고객 응대 메시지", "명시적 의도 - 고객 응대"),
        ("협업 제안 이메일", "명시적 의도 - 협업 이메일"),
        ("제안서 작성", "명시적 의도 - 제안서")
    ]
    
    results = []
    
    for test_input, description in test_cases:
        print(f"\n🧪 테스트: {description}")
        print(f"📝 입력: {test_input}")
        print("-" * 40)
        
        result = cursor_system.process_user_input(test_input)
        
        print(f"🎯 의도: {result['intent']}")
        print(f"📊 신뢰도: {result['confidence']:.2f}")
        print(f"🔧 분류 방법: {result['classification_method']}")
        print(f"❓ 명확화 필요: {result['requires_clarification']}")
        
        if result['followup_questions']:
            print("💬 후속 질문:")
            for i, question in enumerate(result['followup_questions'], 1):
                print(f"  {i}. {question}")
        
        results.append({
            'input': test_input,
            'description': description,
            'intent': result['intent'],
            'confidence': result['confidence'],
            'method': result['classification_method'],
            'requires_clarification': result['requires_clarification']
        })
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    high_confidence = [r for r in results if r['confidence'] >= 0.8]
    medium_confidence = [r for r in results if 0.5 <= r['confidence'] < 0.8]
    low_confidence = [r for r in results if r['confidence'] < 0.5]
    
    print(f"✅ 높은 신뢰도 (≥0.8): {len(high_confidence)}개")
    for r in high_confidence:
        print(f"  - {r['input']} → {r['intent']} ({r['confidence']:.2f})")
    
    print(f"⚠️ 중간 신뢰도 (0.5-0.8): {len(medium_confidence)}개")
    for r in medium_confidence:
        print(f"  - {r['input']} → {r['intent']} ({r['confidence']:.2f})")
    
    print(f"❓ 낮은 신뢰도 (<0.5): {len(low_confidence)}개")
    for r in low_confidence:
        print(f"  - {r['input']} → {r['intent']} ({r['confidence']:.2f})")
    
    # 분류 방법별 통계
    methods = {}
    for r in results:
        method = r['method']
        methods[method] = methods.get(method, 0) + 1
    
    print(f"\n🔧 분류 방법별 통계:")
    for method, count in methods.items():
        print(f"  - {method}: {count}개")
    
    print(f"\n✅ 테스트 완료! 총 {len(results)}개 케이스 테스트됨")

if __name__ == "__main__":
    test_comprehensive() 