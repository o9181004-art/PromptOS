from llm_api.llm_client import call_llm_openrouter

# 🎯 1. 의도 자동 분류 (LLM 기반)
def classify_intent(text):
    system_prompt = "You're an AI assistant that classifies user intent."
    user_prompt = f"""
다음 문장의 목적을 하나 또는 복수로 분류해줘. 가능한 카테고리는 다음과 같아:

['summary', 'self_intro', 'customer_reply', 'business_plan', 'report_write', 'email_reply', 'idea_generation']

문장: "{text}"

응답 형식:
Intent: [카테고리1, 카테고리2, ...]
    """
    response = call_llm_openrouter(system_prompt, user_prompt)
    intent_line = [line for line in response.strip().splitlines() if line.lower().startswith("intent")]
    if intent_line:
        raw = intent_line[0].split(":", 1)[-1].strip()
        return [i.strip() for i in raw.strip('[]').split(',') if i.strip()]
    return []

# 🧠 2. 조건 추출 (시제, 어조, 독자 대상)
def extract_conditions(utterance):
    system_prompt = "You are a professional language analyzer that returns structured results."
    user_prompt = f"""
다음 문장의 시제, 어조, 대상 독자를 분석해줘.
문장: "{utterance}"

출력 형식:
Tense: [present/past/future]
Tone: [formal/informal/neutral]
Audience: [general/expert/customer]
    """
    response = call_llm_openrouter(system_prompt, user_prompt)
    lines = response.strip().splitlines()
    conditions = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip().lower()
            if "tense" in key:
                conditions["tense"] = value
            elif "tone" in key:
                conditions["tone"] = value
            elif "audience" in key:
                conditions["audience"] = value
    return conditions

# 🧱 3. 템플릿 매핑 함수
def get_template(intent):
    templates = {
        "summary": "Please summarize the following content in a {tone} tone for a {audience} audience.",
        "self_intro": "Introduce yourself focusing on your strengths and experience, using a {tone} tone.",
        "customer_reply": "Respond to the customer's complaint in a {tone} tone, addressing the key concerns.",
        "business_plan": "Write a business plan in a {tone} tone for a {audience} audience.",
        "report_write": "Generate a formal report about the following topic in a {tone} tone.",
        "email_reply": "Compose an email reply with a {tone} tone to a {audience}.",
        "idea_generation": "Generate creative ideas about the following topic in a {tone} tone."
    }
    return templates.get(intent)

# ⚙ 4. 템플릿 기반 프롬프트 생성
def generate_prompt(intent, conditions):
    template = get_template(intent)
    if not template:
        print("⚙️ 템플릿 미존재 → LLM으로 자동 프롬프트 생성")
        return generate_prompt_from_llm(intent, conditions)
    try:
        return template.format(**conditions)
    except KeyError:
        return template

# 🧬 5. 템플릿이 없을 때 LLM 생성
def generate_prompt_from_llm(intent, conditions):
    system_prompt = "You're a prompt engineer AI. Generate a well-structured GPT prompt based on the user's intent and style conditions."
    user_prompt = f"""
[Intent]: {intent}
[Conditions]:
- Tense: {conditions.get('tense')}
- Tone: {conditions.get('tone')}
- Audience: {conditions.get('audience')}

Generate a natural, effective GPT prompt that fits these conditions.
Return only the prompt, no explanation.
    """
    return call_llm_openrouter(system_prompt, user_prompt).strip()

# 🔍 6. 누락 질문 생성
def generate_followup_question(placeholder):
    system_prompt = "You're a helpful assistant that generates clarification questions."
    user_prompt = f"""
사용자가 작성한 프롬프트에 필요한 값이 누락되었습니다.
다음 정보를 얻기 위해 어떤 질문을 할지 생성해주세요.

[항목]: {placeholder}

- 한국어로 1문장 질문만 출력
- 예: '당신의 강점은 무엇인가요?'
    """
    return call_llm_openrouter(system_prompt, user_prompt).strip()

# 📊 7. 품질 평가
def evaluate_prompt_quality(utterance, prompt, conditions):
    system_prompt = "You are an expert in prompt engineering and prompt evaluation."
    user_prompt = f"""
사용자가 입력한 요청: "{utterance}"
생성된 프롬프트: "{prompt}"

조건:
- Tense: {conditions.get("tense")}
- Tone: {conditions.get("tone")}
- Audience: {conditions.get("audience")}

다음 항목에 따라 프롬프트를 5점 만점으로 평가해주세요:
1. 목적 적합성 (Intent Alignment)
2. 명확성 (Clarity)
3. 완결성 (Completeness)
4. 스타일 일관성 (Style Consistency)

형식 예시:
Intent Alignment: 5  
Clarity: 4  
Completeness: 4  
Style Consistency: 5  

+ 간단한 개선 의견 1줄 포함
    """
    return call_llm_openrouter(system_prompt, user_prompt).strip()
