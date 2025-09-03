# 📁 promptos_runner.py

import os
from dotenv import load_dotenv
from llm_api import call_llm_openrouter
from llm_utils import classify_intent_llm
from prompt_generator import extract_conditions, generate_prompt
from prompt_builder import extract_placeholders, prompt_missing_values, fill_template, get_template
from fallback_manager import fallback_manager

load_dotenv()

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

    # 3. 조건 추출
    conditions = extract_conditions(utterance)
    print(f"✅ Extracted Conditions: {conditions}")

    # 4. 템플릿 불러오기
    base_template = get_template(intent)
    if base_template is None:
        print("⚠️ 템플릿을 찾을 수 없습니다. LLM에게 직접 프롬프트 생성을 요청합니다...")
        final_prompt = fallback_manager.generate_prompt_with_llm(utterance, intent)
        print(f"\n🟢 LLM 생성 프롬프트:")
        print(final_prompt)
        
        # 7. LLM 호출
        print("\n🤖 Calling LLM...")
        llm_response = call_llm_openrouter(final_prompt)
        print("\n📬 GPT Response:\n")
        print(llm_response)
        return

    # 5. 보완값 입력 (조건 중 누락된 placeholder)
    placeholders = extract_placeholders(base_template)
    missing_placeholders = [ph for ph in placeholders if ph not in conditions]
    user_values = prompt_missing_values(missing_placeholders, utterance, intent)

    # 6. 최종 프롬프트 생성
    all_values = {**conditions, **user_values}
    final_prompt = fill_template(base_template, all_values)

    print("\n🟢 Final Prompt:")
    print(final_prompt)

    # 7. LLM 호출
    print("\n🤖 Calling LLM...")
    llm_response = call_llm_openrouter(final_prompt)
    print("\n📬 GPT Response:\n")
    print(llm_response)

if __name__ == "__main__":
    run_promptos()