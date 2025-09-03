import streamlit as st
from prompt_generator import classify_intent, extract_conditions, generate_prompt, evaluate_prompt_quality
from llm_api.llm_client import call_llm_openrouter

st.set_page_config(page_title="PromptOS MVP", layout="wide")

st.title("🧠 PromptOS - 웹버전 MVP")

# 1. 사용자 입력
utterance = st.text_input("💬 Enter your instruction", placeholder="예: 자기소개서 작성해줘")

if utterance:
    # 2. 의도 분석
    intent = classify_intent(utterance)
    st.write(f"✅ Detected Intent: `{intent}`")

    # 3. 조건 추출
    conditions = extract_conditions(utterance)
    st.write("✅ Extracted Conditions:", conditions)

    # 4. 프롬프트 생성
    final_prompt = generate_prompt(intent, conditions)
    st.markdown("### 🟢 Final Prompt")
    st.code(final_prompt)

    # 5. 품질 평가
    st.markdown("### 📊 Evaluating Prompt Quality...")
    evaluation = evaluate_prompt_quality(utterance, final_prompt, conditions)
    st.markdown("### 📋 Prompt Evaluation Result:")
    st.text(evaluation)

    # 6. LLM 최종 응답
    st.markdown("### 🤖 Calling LLM for final response...")

    system_prompt = "You are a helpful assistant that generates high-quality responses based on the user's prompt."
    gpt_response = call_llm_openrouter(system_prompt, final_prompt)
    
    st.markdown("### 📬 GPT Response:")
    st.success(gpt_response)
