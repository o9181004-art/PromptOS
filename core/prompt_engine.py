"""
PromptOS Core Engine
기존 프롬프트 생성 기능을 통합한 핵심 엔진
"""

import logging
from typing import Dict, Any, Optional
from prompt_generator import generate_prompt, extract_conditions
from llm_utils import classify_intent_llm
from fallback_manager import FallbackManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptEngine:
    """PromptOS 핵심 프롬프트 생성 엔진"""
    
    def __init__(self):
        self.fallback_manager = FallbackManager()
        logger.info("✅ PromptEngine 초기화 완료")
    
    def generate_prompt_from_input(self, user_input: str) -> Dict[str, Any]:
        """
        사용자 입력으로부터 프롬프트를 생성합니다.
        
        Args:
            user_input (str): 사용자 입력 텍스트
            
        Returns:
            Dict[str, Any]: {
                'success': bool,
                'prompt': str,
                'intent': str,
                'error': str (optional)
            }
        """
        try:
            logger.info(f"🔍 프롬프트 생성 시작: {user_input[:50]}...")
            
            # 1. 의도 분류
            intent = classify_intent_llm(user_input).strip().lower()
            logger.info(f"✅ 의도 분류: {intent}")
            
            if intent == "unknown":
                # Fallback 처리
                fallback_prompt = self.fallback_manager.generate_prompt_with_llm(user_input)
                return {
                    'success': True,
                    'prompt': fallback_prompt,
                    'intent': 'fallback',
                    'method': 'llm_fallback'
                }
            
            # 2. 조건 추출
            conditions = extract_conditions(user_input)
            logger.info(f"✅ 조건 추출: {conditions}")
            
            # 3. 프롬프트 생성
            generated_prompt = generate_prompt(intent, user_input)
            
            if generated_prompt:
                return {
                    'success': True,
                    'prompt': generated_prompt,
                    'intent': intent,
                    'conditions': conditions,
                    'method': 'template_based'
                }
            else:
                # 템플릿 기반 생성 실패 시 fallback
                fallback_prompt = self.fallback_manager.generate_prompt_with_llm(user_input, intent)
                return {
                    'success': True,
                    'prompt': fallback_prompt,
                    'intent': intent,
                    'method': 'llm_fallback'
                }
                
        except Exception as e:
            logger.error(f"❌ 프롬프트 생성 실패: {e}")
            return {
                'success': False,
                'error': str(e),
                'prompt': None,
                'intent': None
            }
    
    def clear_input(self) -> Dict[str, Any]:
        """입력 초기화"""
        return {
            'success': True,
            'message': '입력이 초기화되었습니다.'
        }

# 전역 인스턴스
prompt_engine = PromptEngine() 