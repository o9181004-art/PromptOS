"""
✅ Cursor Instruction System Adapter
기존 PromptOS 시스템과 새로운 Cursor Instruction System을 연결하는 어댑터
"""

import logging
from typing import Dict, Any, Optional
from cursor_instruction_system import cursor_system

logger = logging.getLogger(__name__)

class CursorInstructionAdapter:
    """
    기존 PromptOS 시스템과 Cursor Instruction System 간의 어댑터
    """
    
    def __init__(self):
        self.cursor_system = cursor_system
        logger.info("✅ Cursor Instruction Adapter 초기화 완료")
    
    def process_utterance(self, utterance: str, chat_history: Optional[list] = None) -> Dict[str, Any]:
        """
        기존 PromptOS 시스템과 호환되는 인터페이스
        
        Args:
            utterance: 사용자 발화
            chat_history: 채팅 히스토리 (선택사항)
            
        Returns:
            Dict[str, Any]: 처리 결과
        """
        try:
            # Cursor Instruction System으로 처리
            result = self.cursor_system.process_user_input(utterance)
            
            # 기존 시스템과 호환되는 형태로 변환
            adapted_result = self._adapt_result(result, chat_history)
            
            logger.info(f"✅ 어댑터 처리 완료: {utterance} → {result['intent']}")
            return adapted_result
            
        except Exception as e:
            logger.error(f"❌ 어댑터 처리 오류: {e}")
            return self._create_fallback_result(utterance, str(e))
    
    def _adapt_result(self, cursor_result: Dict[str, Any], chat_history: Optional[list]) -> Dict[str, Any]:
        """Cursor 결과를 기존 시스템 형식으로 변환"""
        
        # 기본 구조
        adapted = {
            "utterance": cursor_result["user_input"],
            "intent": cursor_result["intent"],
            "confidence": cursor_result["confidence"],
            "classification_method": cursor_result["classification_method"],
            "prompt": cursor_result["prompt"],
            "requires_clarification": cursor_result["requires_clarification"],
            "followup_questions": cursor_result["followup_questions"],
            "template_info": cursor_result["template_info"],
            "system": "cursor_instruction",
            "chat_history": chat_history or []
        }
        
        # 신뢰도에 따른 처리 방식 결정
        if cursor_result["confidence"] >= 0.8:
            adapted["processing_type"] = "high_confidence_template"
            adapted["should_use_template"] = True
        elif cursor_result["confidence"] >= 0.5:
            adapted["processing_type"] = "medium_confidence_with_fallback"
            adapted["should_use_template"] = True
        else:
            adapted["processing_type"] = "low_confidence_fallback"
            adapted["should_use_template"] = False
        
        return adapted
    
    def _create_fallback_result(self, utterance: str, error_message: str) -> Dict[str, Any]:
        """오류 발생 시 fallback 결과 생성"""
        return {
            "utterance": utterance,
            "intent": "general_inquiry",
            "confidence": 0.1,
            "classification_method": "error_fallback",
            "prompt": f"사용자의 요청을 이해하지 못했습니다: {utterance}\n\n오류: {error_message}\n\n친근하고 도움이 되는 방식으로 응답해주세요.",
            "requires_clarification": True,
            "followup_questions": [
                "어떤 종류의 도움이 필요하신가요?",
                "더 구체적으로 설명해주실 수 있나요?"
            ],
            "template_info": {},
            "system": "cursor_instruction_fallback",
            "chat_history": [],
            "processing_type": "error_fallback",
            "should_use_template": False
        }
    
    def get_supported_intents(self) -> list:
        """지원하는 의도 목록 반환"""
        return list(self.cursor_system.templates.keys())
    
    def get_template_info(self, intent: str) -> Optional[Dict[str, Any]]:
        """특정 의도의 템플릿 정보 반환"""
        return self.cursor_system.templates.get(intent)
    
    def validate_intent(self, intent: str) -> bool:
        """의도가 유효한지 검증"""
        return intent in self.cursor_system.templates
    
    def get_system_stats(self) -> Dict[str, Any]:
        """시스템 통계 정보 반환"""
        return {
            "system_name": "Cursor Instruction System",
            "template_count": len(self.cursor_system.templates),
            "supported_intents": self.get_supported_intents(),
            "confidence_thresholds": self.cursor_system.confidence_thresholds,
            "version": "1.0.0"
        }

# 전역 어댑터 인스턴스
cursor_adapter = CursorInstructionAdapter()

def get_cursor_adapter():
    """어댑터 인스턴스 반환"""
    return cursor_adapter

# 기존 시스템과의 호환성을 위한 함수들
def process_with_cursor_system(utterance: str, chat_history: Optional[list] = None) -> Dict[str, Any]:
    """기존 시스템에서 호출할 수 있는 함수"""
    return cursor_adapter.process_utterance(utterance, chat_history)

def get_cursor_prompt(utterance: str) -> str:
    """프롬프트만 반환하는 간단한 함수"""
    result = cursor_adapter.process_utterance(utterance)
    return result["prompt"]

# 테스트 함수
def test_adapter():
    """어댑터 테스트"""
    print("🧪 Cursor Instruction Adapter 테스트")
    print("=" * 50)
    
    test_cases = [
        "사업계획서 써줘",
        "마케팅 카피 써줘",
        "그냥 써줘",
        "면접용 자기소개서 작성 도와줘"
    ]
    
    for test_input in test_cases:
        print(f"\n📝 입력: {test_input}")
        
        result = cursor_adapter.process_utterance(test_input)
        
        print(f"🎯 의도: {result['intent']}")
        print(f"📊 신뢰도: {result['confidence']:.2f}")
        print(f"🔧 처리 방식: {result['processing_type']}")
        print(f"📋 템플릿 사용: {result['should_use_template']}")
        print(f"❓ 명확화 필요: {result['requires_clarification']}")
        
        if result['followup_questions']:
            print(f"💬 후속 질문: {len(result['followup_questions'])}개")
    
    # 시스템 통계
    stats = cursor_adapter.get_system_stats()
    print(f"\n📊 시스템 통계:")
    print(f"  - 시스템: {stats['system_name']}")
    print(f"  - 템플릿 개수: {stats['template_count']}")
    print(f"  - 지원 의도: {len(stats['supported_intents'])}개")
    
    print("\n✅ 어댑터 테스트 완료")

if __name__ == "__main__":
    test_adapter() 