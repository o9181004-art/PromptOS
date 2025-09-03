import os
import logging
from llm_api import call_llm_openrouter
import re # Added for advanced_intent_reconstruction
from purpose_based_template_system import get_purpose_based_template_system

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_intent(user_input: str) -> str:
    """
    사용자 입력을 기반으로 의도를 분류합니다.
    
    Args:
        user_input (str): 분류할 사용자 입력
        
    Returns:
        str: 분류된 의도 (business_plan, collaboration_email, customer_reply, summary, complaint, self_intro, etc)
    """
    prompt = f"""
다음 문장은 어떤 목적의 문장인가요? 아래 중 하나로 분류해주세요:
- business_plan
- collaboration_email
- customer_reply
- summary
- complaint
- self_intro
- etc

문장: "{user_input}"
"""
    try:
        response = call_llm_openrouter(prompt)
        response = response.lower().strip()
        
        # 유효한 의도 목록
        valid_intents = [
            "business_plan", "collaboration_email", "customer_reply", 
            "summary", "complaint", "self_intro", "etc"
        ]
        
        # 응답에서 유효한 의도 찾기
        for intent in valid_intents:
            if intent in response:
                return intent
        
        # 응답에서 의도가 명확하지 않은 경우 "etc" 반환
        return "etc"
        
    except Exception as e:
        logger.error(f"의도 분류 실패: {e}")
        return "etc"

def extract_intent_and_purpose(user_input: str, chat_history: list = None) -> dict:
    """
    🎯 [📌 REFINED CURSOR INSTRUCTION: Enhanced Context-Aware Intent Classification]
    
    If the user's intent is **not clearly classifiable**, refer to prior messages (chat history) 
    to infer their likely goal. Reclassify the intent based on inferred purpose 
    (e.g., if "Make an IR draft" is detected, override 'general_inquiry' with 'investor_IR_document').
    
    Use the inferred intent to select or construct the appropriate system prompt template.
    Avoid generic fallback templates unless absolutely necessary.
    Always match prompt tone, style, and structure to the purpose 
    (e.g., professional for investors, casual for friend advice).
    
    Args:
        user_input (str): The user's utterance
        chat_history (list): Optional chat history for context
        
    Returns:
        dict: Contains intent, purpose, and system prompt
    """
    user_input_lower = user_input.lower()
    
    # Check if input is ambiguous or informal
    ambiguous_patterns = [
        "그냥", "사람", "감성", "자극", "써줘", "이거", "요즘", "대세", "괜찮아", "대박", 
        "나도 할까", "형", "bro", "this", "trend", "cool", "awesome", "should i", 
        "is this ok", "wow", "just", "people", "emotion", "stimulate", "write"
    ]
    
    is_ambiguous_or_informal = any(pattern in user_input_lower for pattern in ambiguous_patterns)
    
    # Enhanced intent classification with context awareness and reclassification
    intent_mapping = {
        "marketing_copy": {
            "keywords": ["마케팅", "광고", "홍보", "브랜딩", "marketing", "advertising", "promotion", "branding"],
            "context_keywords": ["감성", "자극", "사람", "고객", "emotion", "stimulate", "people", "customer"],
            "korean_classification": "마케팅 카피 작성 요청",
            "description": "감성적이고 설득력 있는 마케팅 카피 작성 요청",
            "tone": "persuasive",
            "style": "emotional",
            "audience": "customer"
        },
        "content_creation": {
            "keywords": ["콘텐츠", "글", "작성", "content", "writing", "article", "post"],
            "context_keywords": ["그냥", "써줘", "just", "write"],
            "korean_classification": "콘텐츠 작성 요청",
            "description": "일반적인 콘텐츠나 글 작성 요청",
            "tone": "informative",
            "style": "engaging",
            "audience": "general"
        },
        "decision_making": {
            "keywords": ["할까", "해야 할까", "어떻게", "시도", "해볼까", "should i", "how", "try", "do it"],
            "context_keywords": ["판단", "결정", "judgment", "decision"],
            "korean_classification": "행동 여부 판단 요청",
            "description": "어떤 행동을 따라 할지에 대한 판단 요청",
            "tone": "analytical",
            "style": "balanced",
            "audience": "personal"
        },
        "feasibility_judgment": {
            "keywords": ["가능할까", "실현 가능", "feasible", "possible", "realistic"],
            "context_keywords": ["가능성", "실현", "possibility", "realization"],
            "korean_classification": "실현 가능성 판단",
            "description": "특정 행동이나 계획의 실현 가능성에 대한 판단 요청",
            "tone": "analytical",
            "style": "thorough",
            "audience": "expert"
        },
        "advice_seeking": {
            "keywords": ["조언", "도움", "가이드", "제안", "advice", "help", "guide", "suggestion"],
            "context_keywords": ["어떻게", "방법", "how", "method"],
            "korean_classification": "조언 요청",
            "description": "특정 상황에 대한 조언이나 가이드 요청",
            "tone": "supportive",
            "style": "practical",
            "audience": "personal"
        },
        "comparison_request": {
            "keywords": ["친구", "다른", "비교", "vs", "versus", "friend", "other", "compare"],
            "context_keywords": ["차이", "비교", "difference", "comparison"],
            "korean_classification": "비교 분석 요청",
            "description": "여러 옵션 간의 비교 분석 요청",
            "tone": "objective",
            "style": "comparative",
            "audience": "general"
        },
        "validation_seeking": {
            "keywords": ["맞나", "올바른", "확인", "검증", "right", "correct", "confirm", "validate"],
            "context_keywords": ["검토", "평가", "review", "evaluation"],
            "korean_classification": "검증 요청",
            "description": "현재 접근 방식이나 결정의 적절성 검증 요청",
            "tone": "thorough",
            "style": "evaluative",
            "audience": "expert"
        },
        "doubt_expression": {
            "keywords": ["모르겠어", "불확실", "의심", "걱정", "don't know", "uncertain", "doubt", "worry"],
            "context_keywords": ["불안", "걱정", "anxiety", "concern"],
            "korean_classification": "불확실성 표현",
            "description": "현재 상황이나 결정에 대한 불확실성이나 걱정 표현",
            "tone": "empathetic",
            "style": "reassuring",
            "audience": "personal"
        },
        "trend_verification": {
            "keywords": ["대세", "요즘", "트렌드", "trend", "popular", "hot", "viral"],
            "context_keywords": ["인기", "유행", "popularity", "fashion"],
            "korean_classification": "트렌드 검증 요청",
            "description": "현재 트렌드나 인기 있는 것에 대한 검증 요청",
            "tone": "informative",
            "style": "current",
            "audience": "general"
        },
        "casual_opinion": {
            "keywords": ["괜찮아", "대박", "좋아", "cool", "awesome", "great", "nice"],
            "context_keywords": ["의견", "평가", "opinion", "evaluation"],
            "korean_classification": "캐주얼 의견 요청",
            "description": "캐주얼한 의견이나 평가 요청",
            "tone": "casual",
            "style": "friendly",
            "audience": "personal"
        },
        "investor_IR_document": {
            "keywords": ["IR", "투자자", "투자", "investor", "investment", "초안", "draft"],
            "context_keywords": ["자료", "문서", "document", "material"],
            "korean_classification": "투자자 관계 문서 작성 요청",
            "description": "투자자를 위한 IR 문서 작성 요청",
            "tone": "professional",
            "style": "formal",
            "audience": "investor"
        },
        "business_plan": {
            "keywords": ["사업계획서", "비즈니스", "창업", "business plan", "startup", "company"],
            "context_keywords": ["계획", "전략", "plan", "strategy"],
            "korean_classification": "사업계획서 작성 요청",
            "description": "사업계획서 작성 요청",
            "tone": "professional",
            "style": "strategic",
            "audience": "investor"
        },
        "proposal": {
            "keywords": ["제안서", "제안", "proposal", "suggestion", "recommendation"],
            "context_keywords": ["안", "방안", "proposal", "solution"],
            "korean_classification": "제안서 작성 요청",
            "description": "제안서 작성 요청",
            "tone": "persuasive",
            "style": "structured",
            "audience": "client"
        }
    }
    
    # Context-aware intent classification with reclassification logic
    detected_intent = "general_inquiry"
    detected_classification = "일반적인 문의"
    detected_description = "일반적인 정보나 가이드 요청"
    detected_tone = "genuine"
    detected_style = "informative"
    detected_audience = "general"
    
    if is_ambiguous_or_informal and chat_history:
        # Use enhanced context-aware classification with reclassification
        detected_intent, detected_classification, detected_description, detected_tone, detected_style, detected_audience = classify_intent_with_context_enhanced(
            user_input, chat_history, intent_mapping
        )
    else:
        # Use keyword-based classification for clear inputs
        for intent, config in intent_mapping.items():
            if any(keyword in user_input_lower for keyword in config["keywords"]):
                detected_intent = intent
                detected_classification = config["korean_classification"]
                detected_description = config["description"]
                detected_tone = config.get("tone", "genuine")
                detected_style = config.get("style", "informative")
                detected_audience = config.get("audience", "general")
                break
    
    # Construct context-aware system prompt with purpose-driven template selection
    if is_ambiguous_or_informal and chat_history:
        # Enhanced context-aware prompt for ambiguous/informal inputs
        system_prompt = f"""사용자의 발화는 '{user_input}'입니다.
이 발화는 모호하거나 비격식적이므로, 이전 대화 기록을 분석하여 실제 의도와 주제 맥락을 추론하십시오.

이전 대화 맥락:
{format_chat_history(chat_history)}

추론된 의도: {detected_classification}
설명: {detected_description}
톤: {detected_tone}
스타일: {detected_style}
대상: {detected_audience}

분석 지침:
1. 키워드 매칭에만 의존하지 말고 대화 맥락을 종합적으로 분석
2. 사용자의 실제 목적과 주제를 대화 흐름에서 추론
3. 모호한 표현을 구체적이고 실용적인 요청으로 해석
4. 이전 대화에서 언급된 주제나 목적과 연결
5. 추론된 의도에 맞는 적절한 톤과 스타일 적용

출력 요구사항:
- 반드시 한글로 작성
- 추론된 목적에 맞는 구체적이고 실용적인 응답 구성
- 사용자의 실제 의도를 반영한 맞춤형 가이드 제공
- 맥락에 맞는 다음 단계나 구체적인 제안 포함
- {detected_tone} 톤과 {detected_style} 스타일로 {detected_audience} 대상에게 적합한 응답"""
    else:
        # Standard prompt for clear inputs
        system_prompt = f"""사용자의 발화는 "{user_input}"입니다.
이 발화는 '{detected_classification}'으로 분류됩니다.
이에 따라 다음 조건을 만족하는 한글 응답을 생성하십시오:

- 해당 상황에 대한 실질적이고 유용한 조언
- 가능한 장단점 및 고려 요소
- 사용자의 상황에 맞는 구체적인 다음 단계 제안
- {detected_tone} 톤과 {detected_style} 스타일로 {detected_audience} 대상에게 적합한 응답

모든 출력은 반드시 한글로 생성하십시오."""
    
    return {
        "intent": detected_intent,
        "korean_classification": detected_classification,
        "description": detected_description,
        "system_prompt": system_prompt,
        "is_context_aware": is_ambiguous_or_informal and chat_history is not None,
        "tone": detected_tone,
        "style": detected_style,
        "audience": detected_audience
    }

def classify_intent_with_context(user_input: str, chat_history: list, intent_mapping: dict) -> tuple:
    """
    대화 맥락을 기반으로 의도를 분류합니다.
    
    Args:
        user_input (str): 사용자 발화
        chat_history (list): 대화 히스토리
        intent_mapping (dict): 의도 매핑 딕셔너리
        
    Returns:
        tuple: (intent, classification, description)
    """
    user_input_lower = user_input.lower()
    
    # Combine current input with recent chat history for context analysis
    context_text = user_input_lower
    if chat_history:
        # Extract recent messages for context
        recent_messages = chat_history[-3:]  # Last 3 messages
        for message in recent_messages:
            if isinstance(message, dict):
                content = message.get('content', '').lower()
            else:
                content = str(message).lower()
            context_text += " " + content
    
    # Score each intent based on both keywords and context
    intent_scores = {}
    
    for intent, config in intent_mapping.items():
        score = 0
        
        # Direct keyword matching (higher weight)
        for keyword in config["keywords"]:
            if keyword in user_input_lower:
                score += 3
        
        # Context keyword matching (medium weight)
        for keyword in config.get("context_keywords", []):
            if keyword in context_text:
                score += 2
        
        # Context analysis for specific patterns
        if intent == "marketing_copy" and any(word in context_text for word in ["감성", "자극", "사람", "emotion", "stimulate", "people"]):
            score += 5  # High score for marketing context
        
        elif intent == "content_creation" and any(word in user_input_lower for word in ["그냥", "써줘", "just", "write"]):
            score += 4  # High score for writing requests
        
        elif intent == "trend_verification" and any(word in context_text for word in ["대세", "트렌드", "trend", "popular"]):
            score += 3
        
        elif intent == "casual_opinion" and any(word in user_input_lower for word in ["괜찮아", "대박", "cool", "awesome"]):
            score += 3
        
        intent_scores[intent] = score
    
    # Find the highest scoring intent
    if intent_scores:
        best_intent = max(intent_scores, key=intent_scores.get)
        if intent_scores[best_intent] > 0:
            config = intent_mapping[best_intent]
            return best_intent, config["korean_classification"], config["description"]
    
    # Default fallback
    return "general_inquiry", "일반적인 문의", "일반적인 정보나 가이드 요청"

def classify_intent_with_context_enhanced(user_input: str, chat_history: list, intent_mapping: dict) -> tuple:
    """
    🎯 [📌 REFINED CURSOR INSTRUCTION] 향상된 맥락 기반 의도 분류 및 재분류
    
    If the user's intent is **not clearly classifiable**, refer to prior messages (chat history) 
    to infer their likely goal. Reclassify the intent based on inferred purpose.
    
    Args:
        user_input (str): 사용자 발화
        chat_history (list): 대화 히스토리
        intent_mapping (dict): 의도 매핑 딕셔너리
        
    Returns:
        tuple: (intent, classification, description, tone, style, audience)
    """
    user_input_lower = user_input.lower()
    
    # Combine current input with recent chat history for context analysis
    context_text = user_input_lower
    if chat_history:
        # Extract recent messages for context (last 5 messages for better context)
        recent_messages = chat_history[-5:]
        for message in recent_messages:
            if isinstance(message, dict):
                content = message.get('content', '').lower()
            else:
                content = str(message).lower()
            context_text += " " + content
    
    # Enhanced scoring system with reclassification logic
    intent_scores = {}
    
    for intent, config in intent_mapping.items():
        score = 0
        
        # Direct keyword matching (higher weight)
        for keyword in config["keywords"]:
            if keyword in user_input_lower:
                score += 4  # Increased weight
        
        # Context keyword matching (medium weight)
        for keyword in config.get("context_keywords", []):
            if keyword in context_text:
                score += 3  # Increased weight
        
        # Enhanced context analysis for specific patterns with reclassification
        if intent == "investor_IR_document":
            # Check for IR-related context in chat history
            ir_indicators = ["IR", "투자자", "투자", "investor", "investment", "초안", "draft", "자료", "문서"]
            if any(indicator in context_text for indicator in ir_indicators):
                score += 8  # Very high score for IR context
            # Reclassify from general_inquiry to investor_IR_document
            if "초안" in user_input_lower or "draft" in user_input_lower:
                score += 6
        
        elif intent == "business_plan":
            # Check for business plan context
            business_indicators = ["사업계획서", "비즈니스", "창업", "business", "startup", "company", "계획", "전략"]
            if any(indicator in context_text for indicator in business_indicators):
                score += 7
            # Reclassify from general_inquiry to business_plan
            if "계획서" in user_input_lower or "plan" in user_input_lower:
                score += 5
        
        elif intent == "marketing_copy":
            # Enhanced marketing context detection
            marketing_indicators = ["마케팅", "광고", "홍보", "브랜딩", "marketing", "advertising", "promotion", "branding"]
            if any(indicator in context_text for indicator in marketing_indicators):
                score += 6
            # Check for emotional/people-focused context
            if any(word in context_text for word in ["감성", "자극", "사람", "고객", "emotion", "stimulate", "people", "customer"]):
                score += 5
        
        elif intent == "content_creation":
            # Enhanced content creation context
            content_indicators = ["콘텐츠", "글", "작성", "content", "writing", "article", "post"]
            if any(indicator in context_text for indicator in content_indicators):
                score += 5
            # Check for writing request patterns
            if any(word in user_input_lower for word in ["그냥", "써줘", "just", "write"]):
                score += 4
        
        elif intent == "decision_making":
            # Enhanced decision-making context
            decision_indicators = ["할까", "해야 할까", "어떻게", "시도", "해볼까", "should i", "how", "try", "do it"]
            if any(indicator in context_text for indicator in decision_indicators):
                score += 5
            # Check for judgment/decision context
            if any(word in context_text for word in ["판단", "결정", "judgment", "decision"]):
                score += 3
        
        elif intent == "trend_verification":
            # Enhanced trend verification context
            trend_indicators = ["대세", "요즘", "트렌드", "trend", "popular", "hot", "viral"]
            if any(indicator in context_text for indicator in trend_indicators):
                score += 4
            # Check for popularity/fashion context
            if any(word in context_text for word in ["인기", "유행", "popularity", "fashion"]):
                score += 3
        
        elif intent == "casual_opinion":
            # Enhanced casual opinion context
            opinion_indicators = ["괜찮아", "대박", "좋아", "cool", "awesome", "great", "nice"]
            if any(indicator in context_text for indicator in opinion_indicators):
                score += 4
            # Check for opinion/evaluation context
            if any(word in context_text for word in ["의견", "평가", "opinion", "evaluation"]):
                score += 3
        
        intent_scores[intent] = score
    
    # Find the highest scoring intent with reclassification logic
    if intent_scores:
        best_intent = max(intent_scores, key=intent_scores.get)
        if intent_scores[best_intent] > 0:
            config = intent_mapping[best_intent]
            return (
                best_intent, 
                config["korean_classification"], 
                config["description"],
                config.get("tone", "genuine"),
                config.get("style", "informative"),
                config.get("audience", "general")
            )
    
    # Default fallback with enhanced context
    return (
        "general_inquiry", 
        "일반적인 문의", 
        "일반적인 정보나 가이드 요청",
        "genuine",
        "informative", 
        "general"
    )

def format_chat_history(chat_history: list) -> str:
    """
    채팅 히스토리를 포맷팅하여 맥락 정보를 제공합니다.
    
    Args:
        chat_history (list): 채팅 히스토리 리스트
        
    Returns:
        str: 포맷팅된 채팅 히스토리
    """
    if not chat_history:
        return "이전 대화 기록이 없습니다."
    
    formatted_history = []
    for i, message in enumerate(chat_history[-3:], 1):  # 최근 3개 메시지만 사용
        if isinstance(message, dict):
            role = message.get('role', 'user')
            content = message.get('content', str(message))
        else:
            role = 'user'
            content = str(message)
        
        formatted_history.append(f"{i}. {role}: {content}")
    
    return "\n".join(formatted_history)

def fallback_prompt_from_topic(user_input: str) -> str:
    """
    Generate a purpose-driven fallback prompt based on the content of the user's input.
    This ensures meaningful guidance even when template matching fails.
    """
    lowered = user_input.lower()

    if "아이디어" in lowered or "idea" in lowered:
        return (
            "Please analyze the feasibility of the user's idea and draft a collaboration email. "
            "The response should include:\n"
            "- Summary of the idea\n"
            "- Feasibility and potential\n"
            "- Suggested collaboration plan\n"
            "- Expected outcomes\n"
            "- Next steps"
        )

    elif "사업계획서" in lowered or "business plan" in lowered:
        return (
            "Please create a structured business plan draft that includes:\n"
            "- Executive summary\n"
            "- Market analysis\n"
            "- Value proposition\n"
            "- Roadmap\n"
            "- Risk and budget"
        )

    elif "제안서" in lowered or "proposal" in lowered:
        return (
            "Please draft a public-sector or funding proposal including:\n"
            "- Project overview\n"
            "- Goals and objectives\n"
            "- Implementation strategy\n"
            "- Policy alignment\n"
            "- Impact and sustainability"
        )

    else:
        return (
            "Please interpret the user's request and generate a useful response "
            "using an appropriate prompt format. Include reasoning if needed."
        )

def sanitize_prompt(user_input: str) -> str:
    """
    사용자 입력을 정리합니다.
    
    Args:
        user_input (str): 사용자 입력
        
    Returns:
        str: 정리된 프롬프트
    """
    # 문자열이 아닌 경우 문자열로 변환
    if not isinstance(user_input, str):
        user_input = str(user_input)
    
    # 기본 정리
    user_input = user_input.strip().strip('"""')
    
    # 따옴표 정규화
    if '"' in user_input or """ in user_input or """ in user_input:
        user_input = user_input.replace(""", "\"").replace(""", "\"")
    
    # 원본 입력 반환 (fallback 제거)
    return user_input

def generate_prompt(intent: str, user_input: str, tone: str = "genuine", tense: str = "present", audience: str = "review panel") -> str:
    """
    의도와 사용자 입력을 기반으로 프롬프트를 생성합니다.
    PromptOS 원칙: 절대 실패하지 않음 - LLM fallback이 기본 동작
    
    Args:
        intent (str): 분류된 의도
        user_input (str): 사용자 입력
        tone (str): 톤 (genuine, formal, casual)
        tense (str): 시제 (present, past, future)
        audience (str): 대상 (review panel, customer, expert, student, government)
        
    Returns:
        str: 생성된 프롬프트
    """
    # 의도별 프롬프트 템플릿 (기본 템플릿)
    templates = {
        "business_plan": f"""
사용자가 "{user_input}"를 작성하고자 합니다.
다음 구조에 따라 체계적으로 작성해주세요:

📌 사업 개요
- 비즈니스 모델과 핵심 가치 제안
- 사업의 목적과 비전

📊 시장 분석  
- 시장 현황과 규모
- 경쟁사 분석과 차별화 포인트

🍽️ 서비스 설명
- 핵심 제품/서비스 상세 설명
- 고객 가치와 혜택

📈 실행 계획
- 단계별 실행 전략
- 자원 및 예산 계획

🎯 기대 효과
- 예상 성과 및 지표
- 사회적/경제적 기여도

전문적이고 격식 있는 한글 보고서 형식으로 작성해주세요.
""",
        "collaboration_email": f"""
사용자가 "{user_input}"에 대한 협업 이메일을 작성하고자 합니다.
다음 요소를 포함하여 전문적이고 친근한 톤으로 작성해주세요:

📧 이메일 구조:
- 인사말
- 협업 제안 배경
- 구체적인 협업 방안
- 기대 효과
- 다음 단계 제안
- 마무리 인사

정중하고 설득력 있는 톤으로 작성해주세요.
""",
        "customer_reply": f"""
사용자가 "{user_input}"에 대한 고객 응대를 작성하고자 합니다.
다음 원칙에 따라 작성해주세요:

💬 응대 원칙:
- 공감과 이해를 바탕으로 한 답변
- 구체적이고 실용적인 해결책 제시
- 정중하고 친근한 톤 유지
- 추가 문의에 대한 개방적 태도

고객의 만족도를 높일 수 있는 전문적인 응대문을 작성해주세요.
""",
        "summary": f"""
사용자가 "{user_input}"에 대한 요약을 작성하고자 합니다.
다음 기준에 따라 요약해주세요:

📋 요약 기준:
- 핵심 내용 추출
- 논리적 구조 유지
- 명확하고 간결한 표현
- 중요도에 따른 우선순위

전문적이고 객관적인 요약문을 작성해주세요.
""",
        "complaint": f"""
사용자가 "{user_input}"에 대한 불만 사항을 작성하고자 합니다.
다음 원칙에 따라 작성해주세요:

📝 불만 사항 작성 원칙:
- 구체적이고 객관적인 사실 기술
- 감정적 표현 최소화
- 건설적인 개선 방안 제시
- 전문적이고 정중한 톤 유지

문제 해결을 위한 건설적인 의견서를 작성해주세요.
""",
        "self_intro": f"""
사용자가 "{user_input}"에 대한 자기소개를 작성하고자 합니다.
다음 요소를 포함하여 작성해주세요:

👤 자기소개 구성:
- 인사말
- 주요 경력 및 전문 분야
- 핵심 역량과 강점
- 목표 및 비전
- 마무리

자신감 있고 전문적인 자기소개를 작성해주세요.
""",
        "etc": f"""
사용자가 "{user_input}"에 대한 내용을 작성하고자 합니다.
다음 기준에 따라 작성해주세요:

📝 작성 기준:
- 명확하고 구조화된 내용
- 적절한 톤과 스타일
- 독자 친화적인 표현
- 전문성과 가독성의 균형

요청사항에 맞는 전문적인 내용을 작성해주세요.
"""
    }
    
    # 1. 기본 템플릿에서 찾기
    template = templates.get(intent)
    
    # 2. 템플릿이 없으면 목적 지향적 fallback 사용
    if not template:
        print(f"[Fallback Triggered] No template for intent: {intent}. Using topic-based fallback.")
        
        # 키워드 기반 목적 지향적 fallback 프롬프트 생성
        fallback_prompt = fallback_prompt_from_topic(user_input)
        
        try:
            # LLM 호출하여 최종 응답 생성
            response = call_llm_openrouter(fallback_prompt)
            print(f"[Topic-Based Fallback Success] Generated response for user input: {user_input[:50]}...")
            return response
        except Exception as e:
            print(f"[Topic-Based Fallback Failed] Error: {e}. Using default template.")
            # LLM 호출 실패 시 기본 템플릿 사용
            return templates["etc"]
    
    return template

def extract_conditions(user_input: str) -> dict:
    """
    사용자 입력에서 tone, tense, audience 조건을 추출합니다.
    """
    # 기본값 설정 (시스템 지침에 따라)
    conditions = {
        "tone": "genuine",
        "tense": "present", 
        "audience": "review panel"
    }
    
    # 사용자 입력에서 키워드 기반으로 조건 추출
    user_input_lower = user_input.lower()
    
    # 톤 추출
    if any(word in user_input_lower for word in ["정중한", "공식", "formal", "비즈니스", "professional", "business"]):
        conditions["tone"] = "formal"
    elif any(word in user_input_lower for word in ["친근한", "캐주얼", "informal", "편안한", "casual", "friendly"]):
        conditions["tone"] = "casual"
    elif any(word in user_input_lower for word in ["진정성", "genuine", "authentic", "sincere"]):
        conditions["tone"] = "genuine"
    
    # 시제 추출
    if any(word in user_input_lower for word in ["과거", "했어", "했던", "past", "completed", "finished"]):
        conditions["tense"] = "past"
    elif any(word in user_input_lower for word in ["미래", "할거야", "예정", "future", "will", "going to"]):
        conditions["tense"] = "future"
    elif any(word in user_input_lower for word in ["현재", "지금", "present", "current", "now"]):
        conditions["tense"] = "present"
    
    # 청중 추출
    if any(word in user_input_lower for word in ["고객", "customer", "클라이언트", "client"]):
        conditions["audience"] = "customer"
    elif any(word in user_input_lower for word in ["전문가", "expert", "개발자", "엔지니어", "specialist"]):
        conditions["audience"] = "expert"
    elif any(word in user_input_lower for word in ["학생", "초보자", "beginner", "student"]):
        conditions["audience"] = "student"
    elif any(word in user_input_lower for word in ["정부", "government", "공무원", "official"]):
        conditions["audience"] = "government"
    elif any(word in user_input_lower for word in ["검토", "review", "평가", "evaluation", "심사", "panel"]):
        conditions["audience"] = "review panel"
    
    return conditions

def process_user_request(user_input: str, chat_history: list = None) -> dict:
    """
    사용자 요청을 처리하여 의도 분류와 표준화된 프롬프트 지시사항을 생성합니다.
    
    🧠 [커서 지시글: 목적 기반 템플릿 시스템 초고도화]
    - 명시적 목적이 있는 발화 → 완전한 intent 템플릿 매칭 후 고정 구조 기반 응답
    - 명시적 목적이 없는 발화 → LLM 목적 추론 + 사용자 보완 질의 후 출력
    - 출력은 항상 한국어, 지시문은 영문 코드로
    
    Args:
        user_input (str): 사용자 입력
        chat_history (list): 채팅 히스토리 (선택사항)
        
    Returns:
        dict: 처리 결과 (intent, prompt_instruction, original_input, conditions, intent_analysis, confidence_score)
    """
    try:
        # 입력 정리
        cleaned_input = sanitize_prompt(user_input)
        logger.info(f"입력 정리 완료: {cleaned_input[:50]}...")
        
        # 🧠 목적 기반 템플릿 시스템 사용
        purpose_system = get_purpose_based_template_system()
        purpose_result = purpose_system.process_user_request(cleaned_input, chat_history)
        
        # 목적 기반 시스템에서 명확한 매칭이 된 경우
        if purpose_result["template_matched"]:
            logger.info(f"목적 기반 템플릿 매칭 성공: {purpose_result['intent']}")
            
            return {
                "intent": purpose_result["intent"],
                "prompt_instruction": purpose_result["prompt_instruction"],
                "original_input": user_input,
                "cleaned_input": cleaned_input,
                "conditions": {"tone": "genuine", "tense": "present", "audience": "review panel"},
                "intent_analysis": {"intent": purpose_result["intent"], "description": "목적 기반 템플릿 매칭"},
                "confidence_score": purpose_result["confidence_score"],
                "method": purpose_result["method"],
                "context_used": False,
                "step": purpose_result["step"],
                "additional_questions": purpose_result["additional_questions"]
            }
        
        # 목적이 불명확한 경우 기존 로직 사용
        else:
            logger.info("목적 기반 매칭 실패, 기존 로직 사용")
            
            # 기존 의도 분류 (템플릿 매칭용)
            template_intent = classify_intent(cleaned_input)
            logger.info(f"기존 템플릿 의도 분류 결과: {template_intent}")
            
            # Intent & Purpose Extraction (모호한 입력 분석)
            intent_analysis = extract_intent_and_purpose(cleaned_input, chat_history)
            logger.info(f"Intent & Purpose 분석: {intent_analysis['intent']}")
            
            # 신뢰도 평가
            confidence_score = evaluate_intent_confidence(template_intent, intent_analysis, cleaned_input)
            logger.info(f"의도 분류 신뢰도: {confidence_score}")
            
            # 신뢰도가 높은 경우 기존 템플릿 사용
            if confidence_score >= 0.7:
                logger.info("기존 템플릿 매칭 사용")
                conditions = extract_conditions(cleaned_input)
                prompt_instruction = generate_standardized_prompt_instruction(cleaned_input, intent_analysis, chat_history)
                
                return {
                    "intent": template_intent,
                    "prompt_instruction": prompt_instruction,
                    "original_input": user_input,
                    "cleaned_input": cleaned_input,
                    "conditions": conditions,
                    "intent_analysis": intent_analysis,
                    "confidence_score": confidence_score,
                    "method": "legacy_template_matching",
                    "context_used": False,
                    "step": "Step 2: Legacy Template Matching",
                    "additional_questions": []
                }
            
            # 신뢰도가 낮고 채팅 히스토리가 있는 경우 LLM 기반 추론
            elif chat_history:
                logger.info("LLM 기반 의도 추론 수행")
                advanced_analysis = advanced_intent_reconstruction(cleaned_input, chat_history)
                
                final_intent = advanced_analysis["intent"]
                final_intent_analysis = {
                    "intent": final_intent,
                    "korean_classification": advanced_analysis.get("korean_response", "고급 분석 결과"),
                    "description": f"고급 LLM 분석을 통한 {final_intent} 의도 추론",
                    "tone": advanced_analysis["conditions"]["tone"],
                    "style": "informative",
                    "audience": advanced_analysis["conditions"]["audience"]
                }
                prompt_instruction = generate_standardized_prompt_instruction(cleaned_input, final_intent_analysis, chat_history)
                
                return {
                    "intent": final_intent,
                    "prompt_instruction": prompt_instruction,
                    "original_input": user_input,
                    "cleaned_input": cleaned_input,
                    "conditions": advanced_analysis["conditions"],
                    "intent_analysis": intent_analysis,
                    "confidence_score": confidence_score,
                    "advanced_analysis": advanced_analysis,
                    "method": "llm_purpose_inference",
                    "context_used": True,
                    "user_message": "사용자의 요청이 명확하지 않지만, 이전 대화 흐름을 기반으로 목적을 추론하고 가장 적절한 방식으로 답변을 생성합니다.",
                    "step": "Step 3: Purpose Inference",
                    "additional_questions": purpose_result["additional_questions"]
                }
            
            # 최종 fallback
            else:
                logger.info("최종 fallback 사용")
                fallback_instruction = generate_fallback_instruction(cleaned_input, intent_analysis)
                
                return {
                    "intent": "general_inquiry",
                    "prompt_instruction": fallback_instruction,
                    "original_input": user_input,
                    "cleaned_input": cleaned_input,
                    "conditions": {"tone": "genuine", "tense": "present", "audience": "review panel"},
                    "intent_analysis": intent_analysis,
                    "confidence_score": confidence_score,
                    "method": "final_fallback",
                    "context_used": False,
                    "user_message": "사용자의 요청이 명확하지 않지만, 가장 적절한 방식으로 답변을 생성합니다.",
                    "step": "Step 4: Final Fallback",
                    "additional_questions": purpose_result["additional_questions"]
                }
        
    except Exception as e:
        logger.error(f"요청 처리 중 오류 발생: {e}")
        # 오류 발생 시에도 기본값으로 fallback
        fallback_intent_analysis = extract_intent_and_purpose(user_input)
        fallback_instruction = generate_fallback_instruction(user_input, fallback_intent_analysis)
        
        return {
            "intent": "etc",
            "prompt_instruction": fallback_instruction,
            "original_input": user_input,
            "cleaned_input": user_input,
            "conditions": {"tone": "genuine", "tense": "present", "audience": "review panel"},
            "intent_analysis": fallback_intent_analysis,
            "confidence_score": 0.0,
            "error": str(e),
            "method": "error_fallback",
            "context_used": False,
            "user_message": "사용자의 요청이 명확하지 않아, 관련된 맥락을 기반으로 답변을 생성했습니다.",
            "step": "Error Fallback",
            "additional_questions": ["어떤 종류의 도움이 필요하신가요?"]
        }

def evaluate_intent_confidence(template_intent: str, intent_analysis: dict, user_input: str) -> float:
    """
    의도 분류의 신뢰도를 평가합니다.
    [📌 REFINED CURSOR INSTRUCTION] 향상된 신뢰도 평가
    
    Args:
        template_intent (str): 템플릿 기반 의도 분류 결과
        intent_analysis (dict): Intent & Purpose 분석 결과
        user_input (str): 사용자 입력
        
    Returns:
        float: 신뢰도 점수 (0.0 ~ 1.0)
    """
    confidence_score = 0.0
    input_lower = user_input.lower()
    
    # 1. 템플릿 의도 분류 신뢰도 (0.0 ~ 0.3)
    if template_intent != "etc":
        confidence_score += 0.3
    elif template_intent == "etc":
        confidence_score += 0.1  # 기본 점수
    
    # 2. Intent & Purpose 분석 신뢰도 (0.0 ~ 0.3)
    if intent_analysis["intent"] != "general_inquiry":
        confidence_score += 0.3
    elif intent_analysis["intent"] == "general_inquiry":
        confidence_score += 0.1  # 기본 점수
    
    # 3. 입력 길이 및 복잡성 (0.0 ~ 0.15)
    input_length = len(user_input.strip())
    if input_length > 20:
        confidence_score += 0.15
    elif input_length > 10:
        confidence_score += 0.1
    elif input_length > 5:
        confidence_score += 0.05
    
    # 4. 명확한 키워드 매칭 (0.0 ~ 0.2)
    clear_keywords = {
        "business": ["사업계획서", "비즈니스", "창업", "business plan", "startup", "company"],
        "marketing": ["마케팅", "광고", "홍보", "브랜딩", "marketing", "advertising", "promotion"],
        "proposal": ["제안서", "제안", "proposal", "suggestion", "recommendation"],
        "summary": ["요약", "정리", "summary", "summarize", "brief"],
        "self_intro": ["자기소개", "이력서", "resume", "introduction"],
        "customer": ["고객", "customer", "client", "service"],
        "content": ["콘텐츠", "글", "작성", "content", "writing", "article"],
        "investor": ["IR", "투자자", "투자", "investor", "investment", "초안", "draft"]
    }
    
    keyword_matches = 0
    for category, keywords in clear_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            keyword_matches += 1
    
    if keyword_matches >= 2:
        confidence_score += 0.2
    elif keyword_matches == 1:
        confidence_score += 0.1
    
    # 5. 모호한 패턴 감지 (패널티: -0.0 ~ -0.2) - 패널티 완화
    ambiguous_patterns = {
        "high_ambiguity": ["그냥", "이거", "요즘", "대세", "괜찮아", "대박", "할까", "형", "bro"],
        "medium_ambiguity": ["just", "this", "trend", "cool", "awesome", "should i", "is this ok"],
        "low_ambiguity": ["사람", "감성", "자극", "써줘", "people", "emotion", "stimulate", "write"]
    }
    
    ambiguity_penalty = 0.0
    for level, patterns in ambiguous_patterns.items():
        if any(pattern in input_lower for pattern in patterns):
            if level == "high_ambiguity":
                ambiguity_penalty += 0.2  # 0.3에서 0.2로 완화
            elif level == "medium_ambiguity":
                ambiguity_penalty += 0.1  # 0.2에서 0.1로 완화
            elif level == "low_ambiguity":
                ambiguity_penalty += 0.05  # 0.05에서 0.05로 유지
    
    confidence_score -= ambiguity_penalty
    
    # 6. 문장 구조 및 완성도 (0.0 ~ 0.05)
    if user_input.endswith(('.', '!', '?')):
        confidence_score += 0.05
    
    # 7. 맥락 인식 가능성 (0.0 ~ 0.05)
    context_indicators = ["이전", "앞서", "위에서", "앞의", "이전에", "before", "previous", "above"]
    if any(indicator in input_lower for indicator in context_indicators):
        confidence_score += 0.05
    
    # 8. 의도 분류 일치도 (0.0 ~ 0.1)
    if template_intent != "etc" and intent_analysis["intent"] != "general_inquiry":
        # 두 분류 결과가 모두 구체적인 경우
        if template_intent == intent_analysis["intent"]:
            confidence_score += 0.1
        elif any(keyword in template_intent for keyword in intent_analysis["intent"].split('_')):
            confidence_score += 0.05
    
    # 최종 신뢰도 점수 정규화 (0.0 ~ 1.0)
    final_confidence = max(0.0, min(confidence_score, 1.0))
    
    # 로깅
    logger.info(f"신뢰도 평가 상세:")
    logger.info(f"  - 템플릿 의도: {template_intent}")
    logger.info(f"  - Intent & Purpose: {intent_analysis['intent']}")
    logger.info(f"  - 입력 길이: {input_length}")
    logger.info(f"  - 키워드 매칭: {keyword_matches}")
    logger.info(f"  - 모호성 패널티: {ambiguity_penalty}")
    logger.info(f"  - 최종 신뢰도: {final_confidence:.3f}")
    
    return final_confidence

def advanced_intent_reconstruction(user_input: str, chat_history: list) -> dict:
    """
    [📌 REFINED CURSOR INSTRUCTION] 고급 LLM 기반 의도 재구성
    
    If the user's intent is **not clearly classifiable**, refer to prior messages (chat history) 
    to infer their likely goal. Reclassify the intent based on inferred purpose 
    (e.g., if "Make an IR draft" is detected, override 'general_inquiry' with 'investor_IR_document').
    
    Use the inferred intent to select or construct the appropriate system prompt template.
    Avoid generic fallback templates unless absolutely necessary.
    Always match prompt tone, style, and structure to the purpose 
    (e.g., professional for investors, casual for friend advice).
    
    Args:
        user_input (str): 현재 사용자 입력
        chat_history (list): 대화 히스토리
        
    Returns:
        dict: 고급 분석 결과
    """
    # 최근 3-5개 대화만 사용
    recent_context = format_chat_history(chat_history[-5:])
    
    # 고급 LLM 프롬프트 구성 - 개선된 의도 재분류 로직
    advanced_prompt = f"""---
User input: {user_input}
Conversation context:
{recent_context}

Tasks:
a. Reconstruct user's true intent from context
b. Classify intent type (summary, decision, suggestion, etc.)
c. Suggest appropriate tone, tense, and audience
d. Generate the most relevant and natural response in Korean

분석 지침:
1. 대화 맥락을 종합적으로 분석하여 사용자의 실제 목적을 파악
2. 모호한 표현을 구체적이고 실용적인 요청으로 해석
3. 이전 대화에서 언급된 주제나 목적과 연결
4. 사용자의 상황과 배경을 고려한 맞춤형 응답 구성
5. 한국어 문화와 맥락을 고려한 자연스러운 표현 사용
6. 의도 재분류: 맥락에서 특정 목적이 감지되면 적절한 의도로 재분류
   - IR/투자자 관련: investor_IR_document
   - 사업계획서 관련: business_plan
   - 마케팅 관련: marketing_copy
   - 콘텐츠 작성: content_creation
   - 의사결정: decision_making
   - 트렌드 검증: trend_verification
   - 캐주얼 의견: casual_opinion

출력 형식:
의도 분류: [intent_type]
톤: [tone]
시제: [tense]
대상: [audience]
한국어 응답: [natural_korean_response]

모든 출력은 반드시 한글로 작성하십시오.
사용자의 요청이 명확하지 않지만, 이전 대화 흐름을 기반으로 목적을 추론하고 가장 적절한 방식으로 답변을 생성합니다.
---"""

    try:
        # LLM 호출하여 고급 분석 수행
        llm_response = call_llm_openrouter(advanced_prompt)
        
        # 응답 파싱
        parsed_response = parse_advanced_llm_response(llm_response)
        
        # 신뢰도 재평가
        reconstructed_confidence = evaluate_reconstructed_confidence(
            user_input, chat_history, parsed_response
        )
        
        return {
            "intent": parsed_response.get("intent", "general_inquiry"),
            "llm_prompt": advanced_prompt,
            "llm_response": llm_response,
            "conditions": {
                "tone": parsed_response.get("tone", "genuine"),
                "tense": parsed_response.get("tense", "present"),
                "audience": parsed_response.get("audience", "review panel")
            },
            "korean_response": parsed_response.get("korean_response", ""),
            "confidence": reconstructed_confidence,
            "context_analysis": {
                "context_used": True,
                "context_length": len(recent_context),
                "reconstruction_method": "advanced_llm"
            }
        }
        
    except Exception as e:
        logger.error(f"고급 의도 재구성 중 오류: {e}")
        # 오류 발생 시 기본값 반환
        return {
            "intent": "general_inquiry",
            "llm_prompt": advanced_prompt,
            "llm_response": "오류로 인해 기본 응답을 생성합니다.",
            "conditions": {
                "tone": "genuine",
                "tense": "present", 
                "audience": "review panel"
            },
            "korean_response": f"사용자의 요청이 명확하지 않아, 관련된 맥락을 기반으로 답변을 생성했습니다. '{user_input}'에 대한 응답을 생성하는 중 오류가 발생했습니다. 다시 시도해주세요.",
            "confidence": 0.5,
            "context_analysis": {
                "context_used": True,
                "context_length": len(recent_context),
                "reconstruction_method": "error_fallback"
            }
        }

def generate_enhanced_fallback_prompt(user_input: str, intent_analysis: dict) -> str:
    """
    향상된 fallback 프롬프트를 생성합니다.
    채팅 히스토리가 없지만 신뢰도가 낮은 경우 사용됩니다.
    
    Args:
        user_input (str): 사용자 입력
        intent_analysis (dict): Intent & Purpose 분석 결과
        
    Returns:
        str: 향상된 fallback 프롬프트
    """
    # 사용자 입력에서 키워드 추출
    input_lower = user_input.lower()
    
    # 키워드 기반 목적 추론
    purpose_keywords = {
        "business": ["사업", "비즈니스", "창업", "startup", "business", "company"],
        "marketing": ["마케팅", "광고", "홍보", "브랜딩", "marketing", "advertising"],
        "writing": ["글", "작성", "콘텐츠", "writing", "content", "article"],
        "decision": ["결정", "판단", "할까", "decision", "choice", "should"],
        "analysis": ["분석", "검토", "리뷰", "analysis", "review", "evaluate"],
        "summary": ["요약", "정리", "summary", "summarize", "brief"],
        "proposal": ["제안", "제안서", "proposal", "suggestion", "recommendation"]
    }
    
    detected_purpose = "general"
    for purpose, keywords in purpose_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            detected_purpose = purpose
            break
    
    # 목적별 맞춤형 프롬프트 생성
    purpose_prompts = {
        "business": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'business_plan')}
한국어 분류: {intent_analysis.get('korean_classification', '사업 관련 요청')}

사용자의 요청이 명확하지 않지만, 사업/비즈니스 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 사업적 관점에서 실용적이고 구체적인 조언 제공
2. 시장 분석, 수익성, 리스크 등을 고려한 종합적 평가
3. 다음 단계를 위한 구체적인 액션 플랜 제시
4. 친근하고 전문적인 톤으로 한국어 응답

출력: 한국어로 자연스럽고 실용적인 사업 조언을 제공하세요.
""",
        
        "marketing": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'marketing_copy')}
한국어 분류: {intent_analysis.get('korean_classification', '마케팅 관련 요청')}

사용자의 요청이 명확하지 않지만, 마케팅/홍보 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 타겟 고객층을 고려한 마케팅 전략 제안
2. 감성적이고 설득력 있는 메시지 구성
3. 브랜드 아이덴티티와 일치하는 톤앤매너 적용
4. 구체적이고 실행 가능한 마케팅 아이디어 제시

출력: 한국어로 창의적이고 효과적인 마케팅 조언을 제공하세요.
""",
        
        "writing": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'content_creation')}
한국어 분류: {intent_analysis.get('korean_classification', '콘텐츠 작성 요청')}

사용자의 요청이 명확하지 않지만, 글쓰기/콘텐츠 작성 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 독자층에 맞는 적절한 스타일과 톤 선택
2. 명확하고 흥미로운 구조로 콘텐츠 구성
3. 핵심 메시지를 효과적으로 전달하는 표현 사용
4. SEO나 가독성을 고려한 최적화 제안

출력: 한국어로 매력적이고 효과적인 콘텐츠 작성 조언을 제공하세요.
""",
        
        "decision": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'decision_making')}
한국어 분류: {intent_analysis.get('korean_classification', '의사결정 요청')}

사용자의 요청이 명확하지 않지만, 의사결정/판단 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 장단점을 객관적으로 분석하여 제시
2. 리스크와 기회를 종합적으로 평가
3. 개인적 상황과 목표를 고려한 맞춤형 조언
4. 구체적인 판단 기준과 다음 단계 제안

출력: 한국어로 신중하고 실용적인 의사결정 조언을 제공하세요.
""",
        
        "analysis": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'feasibility_judgment')}
한국어 분류: {intent_analysis.get('korean_classification', '분석/검토 요청')}

사용자의 요청이 명확하지 않지만, 분석/검토 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 객관적이고 체계적인 분석 방법론 적용
2. 데이터와 사실에 기반한 평가 제공
3. 다양한 관점에서의 종합적 분석
4. 개선점과 발전 방향에 대한 구체적 제안

출력: 한국어로 전문적이고 객관적인 분석 결과를 제공하세요.
""",
        
        "summary": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'summary')}
한국어 분류: {intent_analysis.get('korean_classification', '요약/정리 요청')}

사용자의 요청이 명확하지 않지만, 요약/정리 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 핵심 내용을 간결하고 명확하게 정리
2. 중요도에 따른 우선순위 설정
3. 원문의 맥락과 의도를 유지
4. 독자가 쉽게 이해할 수 있는 구조로 구성

출력: 한국어로 명확하고 간결한 요약을 제공하세요.
""",
        
        "proposal": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'proposal')}
한국어 분류: {intent_analysis.get('korean_classification', '제안/제안서 요청')}

사용자의 요청이 명확하지 않지만, 제안/제안서 맥락으로 추론하여 가장 적절한 응답을 생성합니다.

요구사항:
1. 명확한 목표와 가치 제안 제시
2. 실행 가능한 구체적 방안 제시
3. 예상 효과와 성과 지표 명시
4. 리스크 관리 방안 포함

출력: 한국어로 설득력 있고 실현 가능한 제안을 제공하세요.
""",
        
        "general": f"""
사용자 입력: "{user_input}"

분석된 의도: {intent_analysis.get('intent', 'general_inquiry')}
한국어 분류: {intent_analysis.get('korean_classification', '일반적인 요청')}

사용자의 요청이 명확하지 않지만, 가장 적절한 방식으로 응답을 생성합니다.

요구사항:
1. 사용자의 의도를 최대한 이해하고 추론
2. 실용적이고 도움이 되는 정보 제공
3. 친근하고 전문적인 톤 유지
4. 추가 질문이나 구체화를 위한 안내 제공

출력: 한국어로 도움이 되는 응답을 제공하세요.
"""
    }
    
    return purpose_prompts.get(detected_purpose, purpose_prompts["general"])

def parse_advanced_llm_response(llm_response: str) -> dict:
    """
    고급 LLM 응답을 파싱하여 구조화된 데이터로 변환합니다.
    
    Args:
        llm_response (str): LLM 응답
        
    Returns:
        dict: 파싱된 응답 데이터
    """
    try:
        # 기본값 설정
        parsed = {
            "intent": "general_inquiry",
            "tone": "genuine",
            "tense": "present",
            "audience": "review panel",
            "korean_response": llm_response,
            "confidence": 0.8
        }
        
        # 의도 분류 추출 - 더 다양한 패턴 지원
        intent_patterns = [
            r"의도 분류:\s*(\w+)",
            r"intent:\s*(\w+)",
            r"분류:\s*(\w+)",
            r"의도:\s*(\w+)",
            r"목적:\s*(\w+)",
            r"\*\*Intent Classification:\*\*\s*(\w+)",
            r"\*\*의도 분류:\*\*\s*(\w+)",
            r"Intent:\s*(\w+)",
            r"Classification:\s*(\w+)"
        ]
        
        for pattern in intent_patterns:
            match = re.search(pattern, llm_response, re.IGNORECASE)
            if match:
                intent = match.group(1).lower()
                # 의도 매핑 - 새로운 의도 타입들 추가
                intent_mapping = {
                    "marketing": "marketing_copy",
                    "content": "content_creation", 
                    "decision": "decision_making",
                    "trend": "trend_verification",
                    "validation": "validation_seeking",
                    "casual": "casual_opinion",
                    "summary": "summary",
                    "business": "business_plan",
                    "proposal": "proposal",
                    "general": "general_inquiry",
                    "investor": "investor_IR_document",
                    "ir": "investor_IR_document",
                    "investment": "investor_IR_document",
                    "감성적인": "marketing_copy",
                    "마케팅": "marketing_copy",
                    "콘텐츠": "content_creation",
                    "결정": "decision_making",
                    "트렌드": "trend_verification",
                    "검증": "validation_seeking",
                    "캐주얼": "casual_opinion",
                    "요약": "summary",
                    "사업": "business_plan",
                    "제안": "proposal",
                    "투자자": "investor_IR_document",
                    "투자": "investor_IR_document",
                    "요청": "general_inquiry",
                    "suggestion": "suggestion",
                    "content_creation": "content_creation",
                    "marketing_copy": "marketing_copy",
                    "business_plan": "business_plan",
                    "investor_ir_document": "investor_IR_document",
                    "decision_making": "decision_making",
                    "trend_verification": "trend_verification"
                }
                parsed["intent"] = intent_mapping.get(intent, intent)
                break
        
        # 톤 추출
        tone_patterns = [
            r"톤:\s*(\w+)",
            r"tone:\s*(\w+)",
            r"\*\*Tone:\*\*\s*(\w+)",
            r"\*\*톤:\*\*\s*(\w+)",
            r"Tone:\s*(\w+)"
        ]
        
        for pattern in tone_patterns:
            match = re.search(pattern, llm_response, re.IGNORECASE)
            if match:
                tone = match.group(1).lower()
                # 톤 매핑
                tone_mapping = {
                    "genuine": "genuine",
                    "casual": "casual",
                    "formal": "formal",
                    "professional": "professional",
                    "friendly": "friendly",
                    "persuasive": "persuasive",
                    "analytical": "analytical",
                    "supportive": "supportive",
                    "empathetic": "empathetic",
                    "thorough": "thorough",
                    "objective": "objective",
                    "informative": "informative",
                    "감성적": "genuine",
                    "친근한": "friendly",
                    "전문적인": "professional",
                    "격식있는": "formal",
                    "설득적": "persuasive",
                    "분석적": "analytical",
                    "지지적": "supportive",
                    "공감적": "empathetic",
                    "철저한": "thorough",
                    "객관적": "objective",
                    "정보적": "informative",
                    "warm": "genuine"
                }
                parsed["tone"] = tone_mapping.get(tone, tone)
                break
        
        # 시제 추출
        tense_patterns = [
            r"시제:\s*(\w+)",
            r"tense:\s*(\w+)",
            r"\*\*Tense:\*\*\s*(\w+)",
            r"\*\*시제:\*\*\s*(\w+)",
            r"Tense:\s*(\w+)"
        ]
        
        for pattern in tense_patterns:
            match = re.search(pattern, llm_response, re.IGNORECASE)
            if match:
                tense = match.group(1).lower()
                # 시제 매핑
                tense_mapping = {
                    "present": "present",
                    "past": "past",
                    "future": "future",
                    "현재": "present",
                    "과거": "past",
                    "미래": "future"
                }
                parsed["tense"] = tense_mapping.get(tense, tense)
                break
        
        # 대상 추출
        audience_patterns = [
            r"대상:\s*(\w+)",
            r"audience:\s*(\w+)",
            r"\*\*Audience:\*\*\s*(\w+)",
            r"\*\*대상:\*\*\s*(\w+)",
            r"Audience:\s*(\w+)"
        ]
        
        for pattern in audience_patterns:
            match = re.search(pattern, llm_response, re.IGNORECASE)
            if match:
                audience = match.group(1).lower()
                # 대상 매핑
                audience_mapping = {
                    "customer": "customer",
                    "general": "general",
                    "expert": "expert",
                    "review panel": "review panel",
                    "investor": "investor",
                    "personal": "personal",
                    "client": "client",
                    "고객": "customer",
                    "일반": "general",
                    "전문가": "expert",
                    "투자자": "investor",
                    "개인": "personal",
                    "클라이언트": "client"
                }
                parsed["audience"] = audience_mapping.get(audience, audience)
                break
        
        # 한국어 응답 추출 - 더 정교한 패턴 매칭
        korean_patterns = [
            r"한국어 응답:\s*(.+)",
            r"response:\s*(.+)",
            r"응답:\s*(.+)",
            r"korean response:\s*(.+)",
            r"\*\*Response:\*\*\s*(.+)",
            r"\*\*응답:\*\*\s*(.+)",
            r"Response:\s*(.+)"
        ]
        
        korean_response_found = False
        for pattern in korean_patterns:
            match = re.search(pattern, llm_response, re.DOTALL | re.IGNORECASE)
            if match:
                parsed["korean_response"] = match.group(1).strip()
                korean_response_found = True
                break
        
        # 패턴 매칭이 실패한 경우 전체 응답에서 한국어 부분 추출
        if not korean_response_found:
            # 한국어가 포함된 부분을 찾아서 응답으로 사용
            korean_sentences = re.findall(r'[가-힣\s\.,!?]+', llm_response)
            if korean_sentences:
                # 가장 긴 한국어 문장을 선택
                longest_korean = max(korean_sentences, key=len)
                if len(longest_korean.strip()) > 10:
                    parsed["korean_response"] = longest_korean.strip()
                else:
                    # 여러 한국어 문장을 조합
                    combined_korean = " ".join([s.strip() for s in korean_sentences if len(s.strip()) > 5])
                    if combined_korean:
                        parsed["korean_response"] = combined_korean
                    else:
                        parsed["korean_response"] = llm_response.strip()
            else:
                parsed["korean_response"] = llm_response.strip()
        
        # 신뢰도 조정 - 의도 분류가 성공한 경우 높은 신뢰도
        if parsed["intent"] != "general_inquiry":
            parsed["confidence"] = 0.8
        else:
            parsed["confidence"] = 0.5
        
        return parsed
        
    except Exception as e:
        logger.error(f"LLM 응답 파싱 중 오류: {e}")
        return {
            "intent": "general_inquiry",
            "tone": "genuine",
            "tense": "present",
            "audience": "review panel",
            "korean_response": llm_response,
            "confidence": 0.5
        }

def evaluate_reconstructed_confidence(user_input: str, chat_history: list, parsed_response: dict) -> float:
    """
    고급 LLM 재구성 결과의 신뢰도를 평가합니다.
    
    Args:
        user_input (str): 사용자 입력
        chat_history (list): 대화 히스토리
        parsed_response (dict): 고급 LLM 재구성 결과
        
    Returns:
        float: 신뢰도 점수 (0.0 ~ 1.0)
    """
    confidence_score = 0.0
    input_lower = user_input.lower()
    
    # 1. 고급 LLM 재구성 결과의 의도 분류 신뢰도 (0.0 ~ 0.3)
    if parsed_response["intent"] != "general_inquiry":
        confidence_score += 0.3
    elif parsed_response["intent"] == "general_inquiry":
        confidence_score += 0.1  # 기본 점수
    
    # 2. 입력 길이 및 복잡성 (0.0 ~ 0.15)
    input_length = len(user_input.strip())
    if input_length > 20:
        confidence_score += 0.15
    elif input_length > 10:
        confidence_score += 0.1
    elif input_length > 5:
        confidence_score += 0.05
    
    # 3. 모호한 패턴 감지 (패널티: -0.0 ~ -0.2) - 패널티 완화
    ambiguous_patterns = {
        "high_ambiguity": ["그냥", "이거", "요즘", "대세", "괜찮아", "대박", "할까", "형", "bro"],
        "medium_ambiguity": ["just", "this", "trend", "cool", "awesome", "should i", "is this ok"],
        "low_ambiguity": ["사람", "감성", "자극", "써줘", "people", "emotion", "stimulate", "write"]
    }
    
    ambiguity_penalty = 0.0
    for level, patterns in ambiguous_patterns.items():
        if any(pattern in input_lower for pattern in patterns):
            if level == "high_ambiguity":
                ambiguity_penalty += 0.2  # 0.3에서 0.2로 완화
            elif level == "medium_ambiguity":
                ambiguity_penalty += 0.1  # 0.2에서 0.1로 완화
            elif level == "low_ambiguity":
                ambiguity_penalty += 0.05  # 0.05에서 0.05로 유지
    
    confidence_score -= ambiguity_penalty
    
    # 4. 문장 구조 및 완성도 (0.0 ~ 0.05)
    if user_input.endswith(('.', '!', '?')):
        confidence_score += 0.05
    
    # 5. 맥락 인식 가능성 (0.0 ~ 0.05)
    context_indicators = ["이전", "앞서", "위에서", "앞의", "이전에", "before", "previous", "above"]
    if any(indicator in input_lower for indicator in context_indicators):
        confidence_score += 0.05
    
    # 6. 의도 분류 일치도 (0.0 ~ 0.1)
    if parsed_response["intent"] != "general_inquiry":
        # 구체적인 의도 분류가 있는 경우
        confidence_score += 0.1
    elif parsed_response["intent"] == "general_inquiry":
        # 일반적인 의도 분류인 경우
        confidence_score += 0.05
    
    # 최종 신뢰도 점수 정규화 (0.0 ~ 1.0)
    final_confidence = max(0.0, min(confidence_score, 1.0))
    
    # 로깅
    logger.info(f"고급 의도 재구성 신뢰도 평가 상세:")
    logger.info(f"  - 고급 LLM 의도: {parsed_response['intent']}")
    logger.info(f"  - 입력 길이: {input_length}")
    logger.info(f"  - 모호성 패널티: {ambiguity_penalty}")
    logger.info(f"  - 최종 신뢰도: {final_confidence:.3f}")
    
    return final_confidence

def generate_standardized_prompt_instruction(user_input: str, intent_analysis: dict, chat_history: list = None) -> str:
    """
    📋 [Prompt Instruction Format] 생성
    
    사용자의 발화를 기반으로 표준화된 프롬프트 지시사항을 생성합니다.
    이는 최종 LLM 응답이 아닌, LLM이 따라야 할 지시사항입니다.
    
    Args:
        user_input (str): 사용자 발화
        intent_analysis (dict): 의도 분석 결과
        chat_history (list): 대화 히스토리 (선택사항)
        
    Returns:
        str: 표준화된 프롬프트 지시사항
    """
    intent = intent_analysis.get("intent", "general_inquiry")
    korean_classification = intent_analysis.get("korean_classification", "일반적인 문의")
    description = intent_analysis.get("description", "일반적인 정보나 가이드 요청")
    tone = intent_analysis.get("tone", "genuine")
    style = intent_analysis.get("style", "informative")
    audience = intent_analysis.get("audience", "general")
    
    # 의도별 구체적인 목적과 작업 구성요소 정의
    intent_purposes = {
        "marketing_copy": {
            "purpose": "감성적이고 설득력 있는 마케팅 카피를 작성하여 고객의 관심을 끌고 행동을 유도",
            "tasks": [
                "제품/서비스의 핵심 가치와 혜택을 강조",
                "고객의 감정과 욕구에 호소하는 메시지 구성",
                "명확한 행동 유도 문구(CTA) 포함",
                "브랜드 톤과 일치하는 스타일 적용"
            ]
        },
        "content_creation": {
            "purpose": "독자에게 가치를 제공하는 유용하고 흥미로운 콘텐츠 작성",
            "tasks": [
                "주제에 대한 명확하고 구조화된 정보 제공",
                "독자의 관심을 끌 수 있는 흥미로운 각도로 접근",
                "실용적이고 실행 가능한 인사이트 포함",
                "독자와의 연결감을 형성하는 친근한 톤 유지"
            ]
        },
        "business_plan": {
            "purpose": "투자자나 이해관계자에게 사업의 가치와 잠재력을 명확하게 전달하는 사업계획서 작성",
            "tasks": [
                "사업 모델과 수익 구조를 명확하게 설명",
                "시장 분석과 경쟁 우위를 제시",
                "재무 계획과 성장 전략을 구체적으로 기술",
                "리스크 요인과 대응 방안을 포함"
            ]
        },
        "investor_IR_document": {
            "purpose": "투자자에게 회사의 투자 가치와 성장 잠재력을 설득력 있게 전달하는 IR 문서 작성",
            "tasks": [
                "회사의 핵심 경쟁력과 시장 포지션을 강조",
                "재무 성과와 성장 지표를 명확하게 제시",
                "미래 전략과 투자 기회를 구체적으로 설명",
                "투자자 관점에서 중요한 정보를 체계적으로 정리"
            ]
        },
        "decision_making": {
            "purpose": "사용자가 현명한 결정을 내릴 수 있도록 객관적이고 실용적인 조언 제공",
            "tasks": [
                "상황을 종합적으로 분석하여 장단점 제시",
                "관련된 위험 요소와 기회 요인을 식별",
                "구체적이고 실행 가능한 다음 단계 제안",
                "사용자의 상황과 목표에 맞는 맞춤형 조언 제공"
            ]
        },
        "trend_verification": {
            "purpose": "현재 트렌드나 주제의 관련성과 중요성을 객관적으로 분석하여 정보 제공",
            "tasks": [
                "해당 트렌드의 현재 상황과 발전 방향 분석",
                "시장이나 사회에 미치는 영향 평가",
                "관련된 기회와 도전 과제 식별",
                "실용적인 관점에서의 의미와 시사점 제시"
            ]
        },
        "casual_opinion": {
            "purpose": "친근하고 솔직한 관점에서 사용자의 질문이나 주제에 대한 의견 제공",
            "tasks": [
                "개인적 경험과 관점을 바탕으로 한 솔직한 의견 제시",
                "긍정적이면서도 현실적인 관점 유지",
                "사용자와의 공감대 형성을 위한 친근한 톤 사용",
                "필요시 추가 정보나 맥락을 제공"
            ]
        },
        "general_inquiry": {
            "purpose": "사용자의 질문이나 요청에 대해 유용하고 정확한 정보 제공",
            "tasks": [
                "질문의 핵심을 파악하여 명확하고 간결한 답변 제공",
                "관련된 배경 정보나 맥락을 포함",
                "실용적이고 실행 가능한 조언이나 제안 포함",
                "사용자가 추가 질문을 할 수 있도록 친근한 톤 유지"
            ]
        }
    }
    
    # 의도에 따른 목적과 작업 구성요소 가져오기
    intent_config = intent_purposes.get(intent, intent_purposes["general_inquiry"])
    purpose = intent_config["purpose"]
    tasks = intent_config["tasks"]
    
    # 톤과 스타일을 한국어로 변환
    tone_korean = {
        "persuasive": "설득적",
        "informative": "정보 제공적",
        "genuine": "진정성 있는",
        "professional": "전문적",
        "casual": "친근한",
        "analytical": "분석적",
        "supportive": "지지하는",
        "empathetic": "공감하는"
    }.get(tone, "적절한")
    
    style_korean = {
        "emotional": "감성적",
        "informative": "정보 제공적",
        "strategic": "전략적",
        "structured": "구조화된",
        "creative": "창의적",
        "practical": "실용적"
    }.get(style, "적절한")
    
    audience_korean = {
        "customer": "고객",
        "investor": "투자자",
        "client": "클라이언트",
        "general": "일반",
        "personal": "개인"
    }.get(audience, "일반")
    
    # 표준화된 프롬프트 지시사항 생성
    instruction = f"""📋 [Prompt Instruction Format]

User utterance: "{user_input}"
Intent: {intent}
Reconstructed Purpose: {purpose}
Instruction:
"""
    
    # 작업 구성요소 추가
    for task in tasks:
        instruction += f"- {task}\n"
    
    # 톤, 스타일, 대상, 언어 지정
    instruction += f"- {tone_korean} 톤과 {style_korean} 스타일로 {audience_korean} 대상에게 적합한 응답\n"
    instruction += "- Output must be in Korean"
    
    return instruction

def generate_fallback_instruction(user_input: str, intent_analysis: dict) -> str:
    """
    Step 4: Fallback Handling - 템플릿 매칭이 없는 경우 기본 지시사항 생성
    
    사용자의 가능한 목적을 추론하고, 도움이 되는 맥락 인식 응답을 한국어로 생성하며,
    필요한 경우 명확화를 위한 후속 질문을 제안합니다.
    
    Args:
        user_input (str): 사용자 입력
        intent_analysis (dict): 의도 분석 결과
        
    Returns:
        str: 기본 fallback 지시사항
    """
    return f"""📋 [Prompt Instruction Format]

User utterance: "{user_input}"
Intent: general_inquiry
Reconstructed Purpose: 사용자의 요청을 분석하여 가능한 목적을 추론하고 도움이 되는 응답 제공
Instruction:
- 사용자의 발화에서 핵심 키워드나 주제를 식별
- 가능한 목적이나 의도를 추론하여 맥락에 맞는 응답 생성
- 한국어로 친근하고 도움이 되는 톤으로 응답
- 필요시 명확화를 위한 후속 질문 제안
- 사용자가 추가 정보를 제공할 수 있도록 안내
- 진정성 있는 톤과 정보 제공적 스타일로 일반 대상에게 적합한 응답
- Output must be in Korean

추가 지침:
- 사용자의 요청이 모호한 경우, 가능한 해석들을 제시
- 구체적인 예시나 단계별 가이드 제공
- 사용자의 상황에 맞는 실용적인 조언 포함
- 필요시 추가 질문을 통해 더 정확한 도움을 제공할 수 있도록 안내"""

# 테스트 함수
def test_prompt_generator():
    """
    프롬프트 생성기를 테스트합니다.
    """
    test_inputs = [
        "사업계획서를 작성해주세요",
        "협업 제안 이메일을 보내야 해",
        "고객 문의에 답변해야 해",
        "회의 내용을 요약해주세요",
        "서비스에 대한 불만을 제기하고 싶어",
        "자기소개서를 작성해야 해",
        # 새로운 fallback 시스템 테스트 케이스들
        "I have a great idea. What should I do with it?",
        "startup funding needed",
        "마케팅 전략이 필요해",
        "기술 개발 방법을 알려줘",
        "투자 유치하고 싶어",
        "help me with my business",
        "어떻게 해야 할지 모르겠어"
    ]
    
    for test_input in test_inputs:
        print(f"\n=== 테스트: {test_input} ===")
        result = process_user_request(test_input)
        print(f"의도: {result['intent']}")
        print(f"조건: {result['conditions']}")
        print(f"프롬프트 길이: {len(result['prompt'])}")
        print(f"프롬프트 미리보기: {result['prompt'][:150]}...")
        
        # fallback 시스템 테스트
        if result['intent'] == 'etc':
            print("🔍 Fallback 시스템이 작동했습니다!")
            fallback_prompt = fallback_prompt_from_topic(test_input)
            print(f"Fallback 프롬프트 길이: {len(fallback_prompt)}")
            print(f"Fallback 프롬프트 미리보기: {fallback_prompt[:100]}...")

if __name__ == "__main__":
    test_prompt_generator()
