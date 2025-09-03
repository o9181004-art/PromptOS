from promptos_runner import call_llm_openrouter  # LLM 호출 함수 사용

def classify_intent(utterance):
    prompt = f"""
다음 문장의 의도를 판단해서 아래 보기 중 하나로만 대답해줘:
- summary
- self_intro
- customer_reply
- code_run

문장: "{utterance}"

정확하게 한 단어로만 대답해줘. 다른 말 하지 마.
"""
    response = call_llm_openrouter(prompt)
    intent = response.strip().lower()

    # 허용된 intent 목록
    valid_intents = ["summary", "self_intro", "customer_reply", "code_run"]
    if intent in valid_intents:
        return intent
    else:
        return "unknown"
