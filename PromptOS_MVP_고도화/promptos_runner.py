import os
from dotenv import load_dotenv
from llm_api.llm_client import call_llm_openrouter
from llm_utils import classify_intent_llm
from prompt_generator import (
    extract_conditions,
    generate_prompt,
    generate_prompt_from_llm,
    evaluate_prompt_quality
)
from prompt_builder import (
    extract_placeholders,
    prompt_missing_values,
    fill_template,
    get_template
)

load_dotenv()

def clean_conditions(conditions):
    """
    조건값에서 '**', 공백 등 불필요한 기호 제거
    """
    cleaned = {}
    for key, value in conditions.items():
        value = value.replace("*", "").replace("-", "").strip()
        cleaned[key] = value
    return cleaned

def run_promptos():
    print("\U0001f9e0 PromptOS MVP - Start\n")

    # 1. 사용자 발화 입력
    utterance = input("💬 Enter your instruction: ")

    # 2. Intent 분류
    intent = classify_intent_llm(utterance).strip().lower()
    print(f"✅ Detected Intent: {intent}")

    if intent == "unknown":
        print("❌ 알 수 없는 작업입니다. 예: 요약 / 자기소개 / 고객 응대 등")
        return

    # 3. 조건 추출 및 정제
    raw_conditions = extract_conditions(utterance)
    conditions = clean_conditions(raw_conditions)
    print(f"✅ Extracted Conditions: {conditions}")

    # 4. 템플릿 불러오기
    base_template = get_template(intent)

    if base_template is None:
        print("⚙️ 템플릿 미존재 → LLM으로 자동 프롬프트 생성")
        final_prompt = generate_prompt_from_llm(intent, conditions)
    else:
        # 5. 보완값 입력
        placeholders = extract_placeholders(base_template)
        missing_placeholders = [ph for ph in placeholders if ph not in conditions]
        user_values = prompt_missing_values(missing_placeholders)

        # 6. 최종 프롬프트 생성
        all_values = {**conditions, **user_values}
        final_prompt = fill_template(base_template, all_values)

    print("\n🟢 Final Prompt:")
    print(final_prompt)

    # ✅ 7. 프롬프트 품질 평가
    print("\n📊 Evaluating Prompt Quality...")
    evaluation = evaluate_prompt_quality(utterance, final_prompt, conditions)
    print("\n📋 Prompt Evaluation Result:")
    print(evaluation)

    # ✅ 8. LLM 호출
    print("\n🤖 Calling LLM...")

    system_prompt = "You are a helpful assistant that generates content based on the given prompt."
    llm_response = call_llm_openrouter(system_prompt, final_prompt)

    print("\n📬 GPT Response:\n")
    print(llm_response)

if __name__ == "__main__":
    run_promptos()

