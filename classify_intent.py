from llm_api import call_llm_openrouter

def classify_intent(utterance: str) -> str:
    """
    사용자 발화를 기반으로 intent를 분류합니다.
    OpenRouter API를 사용하여 LLM 기반 분류를 수행합니다.
    
    Args:
        utterance (str): 분류할 사용자 발화
        
    Returns:
        str: 분류된 intent (사업계획서 작성, 이메일 작성, 보고서 작성, 설명문 작성, 
             고객 응대, 홍보문구, 계획 수립, 요약 요청)
    """
    utterance = utterance.strip()
    
    if not utterance:
        return "unknown"
    
    prompt = f"""
You are an intent classifier for a prompt generation system.

Given the following user input, classify it into one of the predefined intents below:

['사업계획서 작성', '이메일 작성', '보고서 작성', '설명문 작성', '고객 응대', '홍보문구', '계획 수립', '요약 요청']

User Input: "{utterance}"

Respond with only one intent from the list above. Do not explain anything.
"""
    
    try:
        response = call_llm_openrouter(prompt)
        intent = response.strip()
        
        # 대괄호나 따옴표 제거
        intent = intent.replace('[', '').replace(']', '').replace('"', '').replace("'", '').strip()
        
        # 유효한 intent인지 확인
        valid_intents = [
            "사업계획서 작성",
            "이메일 작성", 
            "보고서 작성",
            "설명문 작성",
            "고객 응대",
            "홍보문구",
            "계획 수립",
            "요약 요청"
        ]
        
        if intent in valid_intents:
            return intent
        else:
            print(f"LLM 분류 결과 '{intent}'가 유효하지 않음. 'unknown' 반환")
            return "unknown"
            
    except Exception as e:
        print(f"LLM 분류 실패: {e}. 'unknown' 반환")
        return "unknown"

# 새로운 의도 분류 시스템은 단순하고 직접적인 LLM 호출을 사용합니다.
# 복잡한 fallback 로직은 제거하고 핵심 기능에 집중합니다.
