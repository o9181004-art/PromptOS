# hybrid_cursor_system.py

"""
하이브리드 Cursor Instruction System
새로운 시스템의 간단함과 기존 시스템의 정교함을 결합
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from cursor_instruction_generator import generate_instruction, classify_intent_llm
from cursor_instruction_system import cursor_system

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridCursorSystem:
    """
    하이브리드 Cursor Instruction System
    명시적 의도는 새로운 시스템, 모호한 의도는 기존 시스템 사용
    """
    
    def __init__(self):
        self.new_system = generate_instruction
        self.old_system = cursor_system
        self.confidence_threshold = 0.6  # 하이브리드 전환 임계값
        
        logger.info("✅ 하이브리드 Cursor System 초기화 완료")
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        하이브리드 방식으로 사용자 입력을 처리합니다.
        
        Args:
            user_input: 사용자 입력
            
        Returns:
            Dict[str, Any]: 처리 결과
        """
        logger.info(f"🔍 하이브리드 처리 시작: {user_input}")
        
        # 1단계: 새로운 시스템으로 빠른 처리 시도
        new_result = self.new_system(user_input)
        
        # 명시적 의도가 감지된 경우 (높은 신뢰도)
        if new_result['confidence'] >= self.confidence_threshold and new_result['intent'] != 'unknown':
            logger.info(f"✅ 새로운 시스템 사용: {new_result['intent']} (신뢰도: {new_result['confidence']})")
            return self._adapt_new_result(new_result, user_input)
        
        # 2단계: 기존 시스템으로 정교한 처리
        logger.info("🔄 기존 시스템으로 전환")
        old_result = self.old_system.process_user_input(user_input)
        
        # 기존 시스템의 신뢰도가 더 높은 경우
        if old_result['confidence'] > new_result['confidence']:
            logger.info(f"✅ 기존 시스템 사용: {old_result['intent']} (신뢰도: {old_result['confidence']})")
            return self._adapt_old_result(old_result, user_input)
        
        # 3단계: 결과 비교 및 최적 선택
        logger.info("⚖️ 결과 비교 및 최적 선택")
        return self._select_best_result(new_result, old_result, user_input)
    
    def _adapt_new_result(self, new_result: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """새로운 시스템 결과를 표준 형식으로 변환"""
        return {
            "user_input": user_input,
            "intent": new_result['intent'],
            "confidence": new_result['confidence'],
            "classification_method": "hybrid_new_system",
            "prompt": "\n".join(new_result['instruction']),
            "followup_questions": [],
            "template_info": new_result.get('template_info', {}),
            "requires_clarification": new_result['requires_clarification'],
            "system_used": "new_system",
            "reconstructed_purpose": new_result.get('reconstructed_purpose', '')
        }
    
    def _adapt_old_result(self, old_result: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """기존 시스템 결과를 표준 형식으로 변환"""
        return {
            "user_input": user_input,
            "intent": old_result['intent'],
            "confidence": old_result['confidence'],
            "classification_method": "hybrid_old_system",
            "prompt": old_result['prompt'],
            "followup_questions": old_result['followup_questions'],
            "template_info": old_result.get('template_info', {}),
            "requires_clarification": old_result['requires_clarification'],
            "system_used": "old_system",
            "reconstructed_purpose": old_result.get('reconstructed_purpose', '')
        }
    
    def _select_best_result(self, new_result: Dict[str, Any], old_result: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """두 시스템의 결과를 비교하여 최적의 결과 선택"""
        
        # 신뢰도 기반 선택
        if new_result['confidence'] > old_result['confidence']:
            logger.info("🏆 새로운 시스템 결과 선택 (높은 신뢰도)")
            return self._adapt_new_result(new_result, user_input)
        elif old_result['confidence'] > new_result['confidence']:
            logger.info("🏆 기존 시스템 결과 선택 (높은 신뢰도)")
            return self._adapt_old_result(old_result, user_input)
        
        # 신뢰도가 동일한 경우, 의도 일치 여부 확인
        if new_result['intent'] == old_result['intent']:
            logger.info("🏆 의도 일치 - 새로운 시스템 결과 선택 (간단함)")
            return self._adapt_new_result(new_result, user_input)
        
        # 의도가 다른 경우, 더 구체적인 의도 선택
        if new_result['intent'] != 'unknown' and old_result['intent'] == 'general_inquiry':
            logger.info("🏆 새로운 시스템 결과 선택 (더 구체적)")
            return self._adapt_new_result(new_result, user_input)
        elif old_result['intent'] != 'general_inquiry' and new_result['intent'] == 'unknown':
            logger.info("🏆 기존 시스템 결과 선택 (더 구체적)")
            return self._adapt_old_result(old_result, user_input)
        
        # 기본값: 기존 시스템 선택
        logger.info("🏆 기본값 - 기존 시스템 결과 선택")
        return self._adapt_old_result(old_result, user_input)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """하이브리드 시스템 통계 반환"""
        return {
            "system_name": "Hybrid Cursor Instruction System",
            "version": "1.0.0",
            "components": {
                "new_system": "cursor_instruction_generator.py",
                "old_system": "cursor_instruction_system.py"
            },
            "features": [
                "자동 시스템 선택",
                "신뢰도 기반 최적화",
                "결과 비교 및 선택",
                "표준화된 출력 형식"
            ],
            "confidence_threshold": self.confidence_threshold
        }

# 하이브리드 시스템 인스턴스
hybrid_system = HybridCursorSystem()

def test_hybrid_system():
    """하이브리드 시스템 테스트"""
    
    test_cases = [
        # 명시적 의도 (새로운 시스템 사용 예상)
        "사업계획서 써줘",
        "마케팅 카피 만들어줘",
        "자기소개서 작성 도와줘",
        "투자자에게 보낼 IR 자료",
        
        # 모호한 의도 (기존 시스템 사용 예상)
        "그냥 써줘",
        "이거 어떻게 생각해?",
        "도와줘",
        
        # 경계 케이스
        "회의 요약해줘",
        "코드 실행해봐",
        "고객 응대 메시지"
    ]
    
    print("🧪 하이브리드 Cursor System 테스트")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i:2d}. 입력: {test_input}")
        
        result = hybrid_system.process_user_input(test_input)
        
        print(f"    🎯 의도: {result['intent']}")
        print(f"    📊 신뢰도: {result['confidence']:.2f}")
        print(f"    🔧 사용 시스템: {result['system_used']}")
        print(f"    📋 분류 방법: {result['classification_method']}")
        print(f"    ❓ 명확화 필요: {result['requires_clarification']}")
        
        if result['followup_questions']:
            print(f"    ❓ 후속 질문: {len(result['followup_questions'])}개")

def compare_all_systems():
    """모든 시스템 비교"""
    
    test_cases = [
        "사업계획서 써줘",
        "마케팅 카피 만들어줘",
        "그냥 써줘"
    ]
    
    print("🔍 모든 시스템 비교")
    print("=" * 60)
    
    for test_input in test_cases:
        print(f"\n📝 입력: {test_input}")
        
        # 새로운 시스템
        new_result = generate_instruction(test_input)
        print(f"🆕 새로운: {new_result['intent']} ({new_result['confidence']:.2f})")
        
        # 기존 시스템
        old_result = cursor_system.process_user_input(test_input)
        print(f"🔄 기존:   {old_result['intent']} ({old_result['confidence']:.2f})")
        
        # 하이브리드 시스템
        hybrid_result = hybrid_system.process_user_input(test_input)
        print(f"⚡ 하이브리드: {hybrid_result['intent']} ({hybrid_result['confidence']:.2f}) - {hybrid_result['system_used']}")

if __name__ == "__main__":
    test_hybrid_system()
    print("\n" + "=" * 60)
    compare_all_systems() 