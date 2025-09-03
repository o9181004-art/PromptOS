def ask_with_retry(prompt_text, valid_options=None):
    while True:
        value = input(prompt_text).strip().lower()
        if value:
            if valid_options and value not in valid_options:
                print(f"❗ Invalid input. Valid options: {', '.join(valid_options)}")
                continue
            return value
        print("⚠️ Input is required. Please try again.")


def extract_conditions():
    tense = ask_with_retry("🕒 Enter the tense (present/past/future): ", ["present", "past", "future"])
    tone = ask_with_retry("🎙️ Enter the tone (formal/informal/neutral): ", ["formal", "informal", "neutral"])
    audience = ask_with_retry("👥 Enter the audience (general/expert/customer/etc):")
    return {
        "tense": tense,
        "tone": tone,
        "audience": audience
    }


def get_template(intent):
    TEMPLATES = {
        "summary": "Please summarize the following content in a {tone} tone for a {audience} audience using {tense} tense.",
        "self_intro": "Introduce yourself focusing on your strengths and experience, using a {tone} tone and {tense} tense for a {audience} audience.",
        "customer_reply": "Respond to the customer's complaint in a {tone} tone using {tense} tense, addressing the key concerns for the {audience}.",
        "code_run": "Explain the following Python code in {tense} tense to a {audience} audience using a {tone} tone."
    }
    return TEMPLATES.get(intent)


def generate_prompt(intent, conditions):
    template = get_template(intent)
    if not template:
        return None
    try:
        main_prompt = template.format(**conditions)

        # ✅ 정확성 강화 문구 자동 삽입
        fact_statement = (
            "\n\n※ Please use only factual information based on verifiable data. "
            "If unsure, respond with 'Insufficient information to answer.'"
        )
        return main_prompt + fact_statement

    except KeyError:
        return template
