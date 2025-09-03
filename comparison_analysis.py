# comparison_analysis.py

"""
새로운 cursor_instruction_generator.py와 기존 Cursor Instruction Template System을 비교 분석
"""

import logging
from typing import Dict, List, Any
from cursor_instruction_generator import generate_instruction, get_system_stats
from cursor_instruction_system import cursor_system

# 로깅 설정
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def compare_systems():
    """두 시스템을 비교 분석합니다."""
    
    print("🔍 Cursor Instruction System 비교 분석")
    print("=" * 60)
    
    # 1. 시스템 통계 비교
    print("\n📊 시스템 통계 비교")
    print("-" * 40)
    
    # 새로운 시스템 통계
    new_stats = get_system_stats()
    print(f"🆕 새로운 시스템: {new_stats['system_name']} v{new_stats['version']}")
    print(f"   지원 의도: {len(new_stats['supported_intents'])}개")
    print(f"   주요 기능: {', '.join(new_stats['features'])}")
    
    # 기존 시스템 통계
    old_stats = {
        "system_name": "Cursor Instruction Template System",
        "version": "1.0.0",
        "supported_intents": list(cursor_system.templates.keys()),
        "features": ["키워드 매칭", "LLM 추론", "신뢰도 기반 처리", "템플릿 우선순위"]
    }
    print(f"🔄 기존 시스템: {old_stats['system_name']} v{old_stats['version']}")
    print(f"   지원 의도: {len(old_stats['supported_intents'])}개")
    print(f"   주요 기능: {', '.join(old_stats['features'])}")
    
    # 2. 테스트 케이스 비교
    test_cases = [
        "사업계획서 써줘",
        "마케팅 카피 만들어줘",
        "자기소개서 작성 도와줘", 
        "회의 요약해줘",
        "코드 실행해봐",
        "고객 응대 메시지",
        "협업 제안 이메일",
        "제안서 작성",
        "투자자에게 보낼 IR 자료",
        "이 아이디어를 특허로 출원",
        "정책 제안서 만들어줘",
        "정부지원사업 신청서 작성",
        "그냥 써줘",
        "이거 어떻게 생각해?"
    ]
    
    print(f"\n🧪 테스트 케이스 비교 ({len(test_cases)}개)")
    print("-" * 40)
    
    results_comparison = []
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i:2d}. 입력: {test_input}")
        
        # 새로운 시스템 결과
        try:
            new_result = generate_instruction(test_input)
            new_intent = new_result['intent']
            new_confidence = new_result['confidence']
            new_clarification = new_result['requires_clarification']
        except Exception as e:
            new_intent = "ERROR"
            new_confidence = 0.0
            new_clarification = False
            logger.error(f"새로운 시스템 오류: {e}")
        
        # 기존 시스템 결과
        try:
            old_result = cursor_system.process_user_input(test_input)
            old_intent = old_result['intent']
            old_confidence = old_result['confidence']
            old_clarification = old_result['requires_clarification']
        except Exception as e:
            old_intent = "ERROR"
            old_confidence = 0.0
            old_clarification = False
            logger.error(f"기존 시스템 오류: {e}")
        
        # 결과 비교
        intent_match = new_intent == old_intent
        confidence_diff = abs(new_confidence - old_confidence)
        
        print(f"    🆕 새로운: {new_intent} (신뢰도: {new_confidence:.2f}, 명확화: {new_clarification})")
        print(f"    🔄 기존:   {old_intent} (신뢰도: {old_confidence:.2f}, 명확화: {old_clarification})")
        
        if intent_match:
            print(f"    ✅ 의도 일치")
        else:
            print(f"    ❌ 의도 불일치")
        
        if confidence_diff < 0.1:
            print(f"    ✅ 신뢰도 유사")
        else:
            print(f"    ⚠️  신뢰도 차이: {confidence_diff:.2f}")
        
        results_comparison.append({
            "input": test_input,
            "new_intent": new_intent,
            "old_intent": old_intent,
            "new_confidence": new_confidence,
            "old_confidence": old_confidence,
            "intent_match": intent_match,
            "confidence_diff": confidence_diff
        })
    
    # 3. 통계 요약
    print(f"\n📈 비교 결과 요약")
    print("-" * 40)
    
    total_tests = len(results_comparison)
    intent_matches = sum(1 for r in results_comparison if r['intent_match'])
    high_confidence_new = sum(1 for r in results_comparison if r['new_confidence'] >= 0.8)
    high_confidence_old = sum(1 for r in results_comparison if r['old_confidence'] >= 0.8)
    avg_confidence_diff = sum(r['confidence_diff'] for r in results_comparison) / total_tests
    
    print(f"총 테스트: {total_tests}개")
    print(f"의도 일치: {intent_matches}개 ({intent_matches/total_tests*100:.1f}%)")
    print(f"높은 신뢰도 (≥0.8):")
    print(f"  - 새로운 시스템: {high_confidence_new}개 ({high_confidence_new/total_tests*100:.1f}%)")
    print(f"  - 기존 시스템: {high_confidence_old}개 ({high_confidence_old/total_tests*100:.1f}%)")
    print(f"평균 신뢰도 차이: {avg_confidence_diff:.3f}")
    
    # 4. 장단점 분석
    print(f"\n💡 시스템별 장단점 분석")
    print("-" * 40)
    
    print("🆕 새로운 시스템 (cursor_instruction_generator.py):")
    print("  ✅ 장점:")
    print("    - 간단하고 직관적인 구조")
    print("    - 명확한 3단계 처리 (명시적 → 추론 → 명확화)")
    print("    - 구조화된 템플릿 (섹션별 구성)")
    print("    - 빠른 처리 속도")
    print("  ❌ 단점:")
    print("    - 제한된 키워드 매칭")
    print("    - 단순한 LLM 추론 (실제 API 미연결)")
    print("    - 신뢰도 계산 로직 부재")
    print("    - 확장성 제한")
    
    print("\n🔄 기존 시스템 (cursor_instruction_system.py):")
    print("  ✅ 장점:")
    print("    - 정교한 신뢰도 계산")
    print("    - 다단계 분류 시스템")
    print("    - 템플릿 우선순위 지원")
    print("    - 확장 가능한 구조")
    print("    - 상세한 로깅 및 디버깅")
    print("  ❌ 단점:")
    print("    - 복잡한 구조")
    print("    - 높은 리소스 사용량")
    print("    - 설정 복잡성")
    print("    - 학습 곡선")
    
    # 5. 권장사항
    print(f"\n🎯 권장사항")
    print("-" * 40)
    
    print("1. 하이브리드 접근법:")
    print("   - 새로운 시스템의 간단함 + 기존 시스템의 정교함")
    print("   - 명시적 의도는 새로운 시스템 사용")
    print("   - 모호한 의도는 기존 시스템 사용")
    
    print("\n2. 개선 방향:")
    print("   - 새로운 시스템에 신뢰도 계산 추가")
    print("   - 기존 시스템의 복잡성 단순화")
    print("   - 공통 인터페이스 표준화")
    
    print("\n3. 사용 시나리오:")
    print("   - 빠른 프로토타이핑: 새로운 시스템")
    print("   - 프로덕션 환경: 기존 시스템")
    print("   - 학습/교육: 새로운 시스템")

def test_specific_cases():
    """특정 케이스에 대한 상세 테스트"""
    
    print("\n🔬 특정 케이스 상세 테스트")
    print("=" * 60)
    
    # 모호한 케이스 테스트
    ambiguous_cases = [
        "그냥 써줘",
        "이거 어떻게 생각해?",
        "도와줘",
        "뭔가 만들어줘"
    ]
    
    for case in ambiguous_cases:
        print(f"\n📝 모호한 입력: {case}")
        
        # 새로운 시스템
        new_result = generate_instruction(case)
        print(f"🆕 새로운 시스템:")
        print(f"   의도: {new_result['intent']}")
        print(f"   신뢰도: {new_result['confidence']}")
        print(f"   명확화 필요: {new_result['requires_clarification']}")
        if new_result['requires_clarification']:
            print(f"   지시사항: {new_result['instruction'][:2]}...")
        
        # 기존 시스템
        old_result = cursor_system.process_user_input(case)
        print(f"🔄 기존 시스템:")
        print(f"   의도: {old_result['intent']}")
        print(f"   신뢰도: {old_result['confidence']}")
        print(f"   명확화 필요: {old_result['requires_clarification']}")
        if old_result['followup_questions']:
            print(f"   후속 질문: {old_result['followup_questions'][:2]}...")

if __name__ == "__main__":
    compare_systems()
    test_specific_cases() 