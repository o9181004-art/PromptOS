"""
✅ Cursor Instruction Template System
목적 기반 프롬프트 템플릿 시스템의 통합 구현
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from cursor_instruction_template_config import (
    TEMPLATES_BY_INTENT, 
    IMPLICIT_PURPOSE_FALLBACK,
    CONFIDENCE_THRESHOLDS,
    TEMPLATE_PRIORITY,
    DEFAULT_CONFIG
)

# 로깅 설정
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class CursorInstructionSystem:
    """
    목적 기반 프롬프트 템플릿 시스템
    명시적 의도와 암묵적 의도를 구분하여 처리
    """
    
    def __init__(self):
        self.templates = TEMPLATES_BY_INTENT
        self.fallback_config = IMPLICIT_PURPOSE_FALLBACK
        self.confidence_thresholds = CONFIDENCE_THRESHOLDS
        self.template_priority = TEMPLATE_PRIORITY
        self.default_config = DEFAULT_CONFIG
        
        # 의도별 키워드 매핑
        self.intent_keywords = self._build_intent_keywords()
        
        logger.info(f"✅ Cursor Instruction System 초기화 완료")
        logger.info(f"📋 템플릿 개수: {len(self.templates)}")
        logger.info(f"🎯 지원 의도: {list(self.templates.keys())}")
    
    def _build_intent_keywords(self) -> Dict[str, List[str]]:
        """의도별 키워드 매핑 구축"""
        keywords = {
            "summary": ["요약", "정리", "핵심", "요점", "간단히"],
            "ir_draft": ["IR", "투자자", "투자", "펀딩", "자금조달"],
            "customer_reply": ["고객", "응대", "문의", "답변", "상담"],
            "collab_email": ["협업", "제안", "이메일", "파트너십", "함께"],
            "biz_plan": ["사업계획서", "비즈니스", "창업", "사업", "계획서"],
            "marketing_copy": ["마케팅", "카피", "홍보", "광고", "프로모션"],
            "self_intro": ["자기소개서", "소개", "이력서", "면접", "지원서"],
            "proposal": ["제안서", "제안", "기획서", "안건", "계획"],
            "meeting_summary": ["회의", "요약", "회의록", "논의", "결정"],
            "code_run": ["코드", "프로그램", "실행", "개발", "디버깅"]
        }
        return keywords
    
    def classify_intent(self, user_input: str) -> Tuple[str, float, str]:
        """
        사용자 입력의 의도를 분류하고 신뢰도를 계산
        
        Returns:
            Tuple[str, float, str]: (의도, 신뢰도, 분류 방법)
        """
        user_input = user_input.strip()
        
        # 1. 명시적 의도 매칭 (키워드 기반)
        explicit_intent, keyword_score = self._match_explicit_intent(user_input)
        if explicit_intent and keyword_score > self.confidence_thresholds["high_confidence"]:
            return explicit_intent, keyword_score, "explicit_keyword_matching"
        
        # 2. 템플릿 기반 유사도 매칭
        template_intent, similarity_score = self._match_template_similarity(user_input)
        if template_intent and similarity_score > self.confidence_thresholds["medium_confidence"]:
            return template_intent, similarity_score, "template_similarity"
        
        # 3. LLM 기반 추론 (낮은 신뢰도)
        llm_intent, llm_score = self._infer_intent_with_llm(user_input)
        if llm_intent and llm_score > self.confidence_thresholds["low_confidence"]:
            return llm_intent, llm_score, "llm_inference"
        
        # 4. Fallback
        return "general_inquiry", 0.3, "fallback"
    
    def _match_explicit_intent(self, user_input: str) -> Tuple[Optional[str], float]:
        """명시적 의도 키워드 매칭"""
        best_match = None
        best_score = 0.0
        
        for intent, keywords in self.intent_keywords.items():
            score = 0.0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in user_input:
                    score += 0.3  # 키워드 매칭 가중치 증가
                    matched_keywords.append(keyword)
            
            # 키워드 매칭 개수에 따른 보너스
            if len(matched_keywords) > 1:
                score += 0.2
            
            # 입력 길이에 따른 패널티 (제거)
            # if len(user_input) < 10:
            #     score -= 0.1
            
            if score > best_score:
                best_score = score
                best_match = intent
        
        logger.info(f"🔍 키워드 매칭 결과: {best_match} (점수: {best_score:.2f})")
        return best_match, min(best_score, 1.0)
    
    def _match_template_similarity(self, user_input: str) -> Tuple[Optional[str], float]:
        """템플릿 기반 유사도 매칭"""
        # 간단한 유사도 계산 (실제로는 더 정교한 알고리즘 사용)
        best_match = None
        best_score = 0.0
        
        for intent, template_info in self.templates.items():
            description = template_info["description"]
            title = template_info["title"]
            
            # 설명과 제목에서 키워드 매칭
            score = 0.0
            for word in user_input.split():
                if word in description:
                    score += 0.05
                if word in title:
                    score += 0.1
            
            if score > best_score:
                best_score = score
                best_match = intent
        
        return best_match, min(best_score, 1.0)
    
    def _infer_intent_with_llm(self, user_input: str) -> Tuple[Optional[str], float]:
        """LLM 기반 의도 추론 (시뮬레이션)"""
        # 실제로는 LLM API 호출
        # 여기서는 간단한 규칙 기반 추론
        if any(word in user_input for word in ["어떻게", "방법", "도와줘"]):
            return "general_inquiry", 0.5
        elif any(word in user_input for word in ["생각", "의견", "평가"]):
            return "review_request", 0.6
        else:
            return "general_inquiry", 0.4
    
    def generate_prompt(self, user_input: str, intent: str, confidence: float) -> str:
        """의도에 따른 프롬프트 생성"""
        
        # 높은 신뢰도: 명시적 템플릿 사용
        if confidence > self.confidence_thresholds["high_confidence"]:
            if intent in self.templates:
                template = self.templates[intent]["template"]
                return f"{template}\n\n사용자 요청: {user_input}"
        
        # 중간 신뢰도: 템플릿 + 추가 지시사항
        elif confidence > self.confidence_thresholds["medium_confidence"]:
            if intent in self.templates:
                template = self.templates[intent]["template"]
                return f"{template}\n\n사용자 요청: {user_input}\n\n추가적인 맥락이나 세부사항이 필요할 수 있습니다."
        
        # 낮은 신뢰도: Fallback 사용
        else:
            fallback_instruction = self.fallback_config["instruction"].format(user_input=user_input)
            return fallback_instruction
    
    def get_followup_questions(self, intent: str, confidence: float) -> List[str]:
        """신뢰도에 따른 후속 질문 생성"""
        if confidence < self.confidence_thresholds["medium_confidence"]:
            if intent in self.templates:
                template_info = self.templates[intent]
                return [
                    f"{template_info['title']}에 대해 더 구체적으로 알려주세요.",
                    "어떤 형식이나 스타일을 원하시나요?",
                    "특별히 포함하고 싶은 내용이 있으신가요?"
                ]
        
        return []
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """사용자 입력 처리의 메인 함수"""
        logger.info(f"🔍 사용자 입력 처리 시작: {user_input}")
        
        # 1. 의도 분류
        intent, confidence, method = self.classify_intent(user_input)
        
        # 2. 프롬프트 생성
        prompt = self.generate_prompt(user_input, intent, confidence)
        
        # 3. 후속 질문 생성
        followup_questions = self.get_followup_questions(intent, confidence)
        
        # 4. 결과 구성
        result = {
            "user_input": user_input,
            "intent": intent,
            "confidence": confidence,
            "classification_method": method,
            "prompt": prompt,
            "followup_questions": followup_questions,
            "template_info": self.templates.get(intent, {}),
            "requires_clarification": confidence < self.confidence_thresholds["medium_confidence"]
        }
        
        logger.info(f"✅ 처리 완료: intent={intent}, confidence={confidence:.2f}, method={method}")
        
        return result

# 시스템 인스턴스 생성
cursor_system = CursorInstructionSystem()

def get_cursor_instruction_system():
    """시스템 인스턴스 반환"""
    return cursor_system

# 테스트 함수
def test_cursor_system():
    """시스템 테스트"""
    test_cases = [
        "사업계획서 써줘",
        "IR 자료 초안 좀 만들어줘", 
        "마케팅 카피 써줘",
        "그냥 써줘",
        "이거 어떻게 생각해?",
        "면접용 자기소개서 작성 도와줘",
        "회의 요약해줘",
        "코드 실행해봐"
    ]
    
    print("🧪 Cursor Instruction System 테스트")
    print("=" * 60)
    
    for test_input in test_cases:
        result = cursor_system.process_user_input(test_input)
        
        print(f"\n📝 입력: {test_input}")
        print(f"🎯 의도: {result['intent']}")
        print(f"📊 신뢰도: {result['confidence']:.2f}")
        print(f"🔧 방법: {result['classification_method']}")
        print(f"❓ 명확화 필요: {result['requires_clarification']}")
        
        if result['followup_questions']:
            print(f"💬 후속 질문: {result['followup_questions'][:2]}")

if __name__ == "__main__":
    test_cursor_system() 