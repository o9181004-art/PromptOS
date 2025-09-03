import streamlit as st

# 템플릿 정의 (한글)
TEMPLATES = {
    "summary": "다음 내용을 {tone} 어조로 {audience} 대상에게 요약해 주세요.",
    "self_intro": "{tone} 어조로 본인의 강점과 경험을 중심으로 자기소개를 작성해 주세요.",
    "customer_reply": "고객의 불만 사항을 {tone} 어조로 정중하게 응답해 주세요.",
    "code_run": "{tense} 시제 기준으로 {audience} 대상에게 다음 Python 명령어를 실행하세요: python {command}"
}

INTENTS = {
    "summary": "요약",
    "self_intro": "자기소개",
    "customer_reply": "고객 응답",
    "code_run": "코드 실행"
}

TONES = ["격식체", "반말", "중립"]
TENSES = ["현재", "과거", "미래"]

# 제목
st.title("🧠 PromptOS MVP (프롬프트 생성기)")

# 선택: 사용자 Intent
intent_label = st.selectbox("💡 어떤 작업을 하시겠습니까?", list(INTENTS.values()))
intent = list(INTENTS.keys())[list(INTENTS.values()).index(intent_label)]

# 시제, 어조, 대상
col1, col2 = st.columns(2)
tense = col1.selectbox("🕒 시제 선택", TENSES)
tone = col2.selectbox("🎙️ 어조 선택", TONES)
audience = st.text_input("👥 수신 대상 입력 (예: 일반인, 고객, 관리자 등)")

# 코드 실행 명령어 입력 (code_run일 때만)
command = ""
if intent == "code_run":
    command = st.text_input("💻 실행할 Python 명령어 입력")

# 프롬프트 생성
if st.button("🚀 프롬프트 생성"):
    # 조건 구성
    conditions = {
        "tense": tense,
        "tone": tone,
        "audience": audience,
        "command": command
    }

    # 템플릿 가져오기 및 렌더링
    template = TEMPLATES.get(intent)
    try:
        prompt = template.format(**conditions)
    except KeyError:
        prompt = "⚠️ 입력 항목이 부족합니다. 모든 값을 입력해 주세요."

    st.subheader("✅ 생성된 프롬프트")
    st.code(prompt, language='markdown')
