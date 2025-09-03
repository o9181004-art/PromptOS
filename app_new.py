# app_new.py - 새로운 템플릿 시스템을 사용하는 PromptOS

import streamlit as st
import logging
import re
from intent_classifier import classify_intent
from template_system import build_prompt, run_final_llm_response

def sanitize_prompt(user_input):
    """
    사용자 입력을 정리하고 너무 짧거나 모호한 경우 구조화된 fallback으로 대체합니다.
    
    Args:
        user_input (str): 사용자 입력
        
    Returns:
        str: 정리된 프롬프트
    """
    # 문자열이 아닌 경우 문자열로 변환
    if not isinstance(user_input, str):
        user_input = str(user_input)
    
    # 사용자가 제안한 입력 정리 로직 적용
    user_input = user_input.strip().strip('"""')
    
    # 따옴표 정규화
    if '"' in user_input or """ in user_input or """ in user_input:
        user_input = user_input.replace(""", "\"").replace(""", "\"")
    
    # 너무 짧거나 모호한 입력인 경우 구조화된 fallback 사용
    if len(user_input.strip()) < 20:
        return (
            "정부 지원금 신청을 위한 예비창업자 패키지용 사업계획서를 작성해주세요. "
            "다음 항목을 포함하여 격식 있는 한글 보고서 형식으로 작성해주세요: "
            "1. 사업 개요, 2. 시장 분석, 3. 서비스 설명, 4. 실행 계획, 5. 기대 효과. "
            "정부 심사관이 검토할 수 있도록 전문적이고 체계적으로 작성해주세요."
        )
    
    return user_input

def display_structured_response(response_text: str, intent: str):
    """
    AI 응답을 의도에 따라 구조화하여 표시합니다.
    
    Args:
        response_text (str): AI 응답 텍스트
        intent (str): 의도 분류 결과
    """
    
    # 의도별 섹션 매핑
    intent_sections = {
        "사업계획서 작성": [
            ("📌 사업 개요", ["사업 개요", "비즈니스 모델", "핵심 가치"]),
            ("📊 시장 분석", ["시장 분석", "시장 현황", "경쟁 분석"]),
            ("🍽️ 서비스 설명", ["서비스 설명", "제품 설명", "핵심 서비스"]),
            ("📈 실행 계획", ["실행 계획", "마케팅 전략", "운영 계획"])
        ],
        "이메일 작성": [
            ("📧 이메일 제목", ["제목", "subject", "title"]),
            ("👋 인사말", ["인사말", "greeting", "안녕하세요"]),
            ("📝 본문 내용", ["본문", "내용", "body"]),
            ("🙏 마무리", ["마무리", "마지막", "감사합니다"])
        ],
        "보고서 작성": [
            ("📋 보고서 개요", ["개요", "요약", "executive summary"]),
            ("📊 주요 내용", ["주요 내용", "핵심 내용", "main content"]),
            ("📈 분석 결과", ["분석 결과", "결과", "analysis"]),
            ("💡 결론 및 제안", ["결론", "제안", "conclusion"])
        ],
        "설명문 작성": [
            ("📖 개요 설명", ["개요", "개념", "overview"]),
            ("🔍 상세 설명", ["상세 설명", "자세한 설명", "detailed"]),
            ("💡 핵심 포인트", ["핵심 포인트", "중요한 점", "key points"]),
            ("📝 요약", ["요약", "정리", "summary"])
        ],
        "고객 응대": [
            ("👋 인사말", ["인사말", "greeting", "안녕하세요"]),
            ("📝 응답 내용", ["응답 내용", "답변", "response"]),
            ("💡 해결 방안", ["해결 방안", "조치 사항", "solution"]),
            ("🙏 마무리", ["마무리", "감사합니다", "closing"])
        ],
        "홍보문구": [
            ("🎯 핵심 메시지", ["핵심 메시지", "main message", "key message"]),
            ("✨ 제품/서비스 특징", ["특징", "장점", "features"]),
            ("📢 홍보 문구", ["홍보 문구", "slogan", "copy"]),
            ("💡 활용 방안", ["활용 방안", "사용법", "usage"])
        ],
        "계획 수립": [
            ("📋 계획 개요", ["계획 개요", "overview", "개요"]),
            ("📅 세부 일정", ["세부 일정", "일정", "schedule"]),
            ("🎯 주요 목표", ["주요 목표", "목표", "objectives"]),
            ("📊 실행 방안", ["실행 방안", "방안", "action plan"])
        ],
        "요약 요청": [
            ("📝 원문 요약", ["요약", "summary", "핵심 내용"]),
            ("💡 주요 포인트", ["주요 포인트", "key points", "중요한 점"]),
            ("📊 분석 결과", ["분석 결과", "결과", "analysis"])
        ]
    }
    
    # 의도에 따른 섹션 가져오기
    sections = intent_sections.get(intent, [
        ("📝 내용", ["내용", "content", "text"])
    ])
    
    # 응답 텍스트를 섹션별로 분할
    lines = response_text.split('\n')
    current_section = "📝 전체 내용"
    current_content = []
    
    # 섹션별로 내용 분류
    section_contents = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 섹션 헤더인지 확인
        section_found = False
        for section_title, keywords in sections:
            for keyword in keywords:
                if keyword.lower() in line.lower():
                    if current_content:
                        section_contents[current_section] = '\n'.join(current_content)
                    current_section = section_title
                    current_content = []
                    section_found = True
                    break
            if section_found:
                break
        
        if not section_found:
            current_content.append(line)
    
    # 마지막 섹션 추가
    if current_content:
        section_contents[current_section] = '\n'.join(current_content)
    
    # 섹션이 없으면 전체 내용으로 표시
    if not section_contents:
        section_contents["📝 전체 내용"] = response_text
    
    # 섹션별로 표시
    for section_title, content in section_contents.items():
        st.subheader(section_title)
        
        # 내용을 불릿 포인트로 변환
        content_lines = content.split('\n')
        formatted_content = []
        
        for line in content_lines:
            line = line.strip()
            if line:
                # 이미 불릿 포인트나 번호가 있으면 그대로 사용
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    formatted_content.append(line)
                else:
                    formatted_content.append(f"• {line}")
        
        st.markdown('\n'.join(formatted_content))
        st.markdown("---")

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 페이지 설정
st.set_page_config(
    page_title="PromptOS 자연어 생성기",
    page_icon="🧠",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
.custom-alert {
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.alert-success {
    background-color: #d1fae5;
    border: 1px solid #10b981;
    color: #065f46;
}

.alert-warning {
    background-color: #fef3c7;
    border: 1px solid #f59e0b;
    color: #92400e;
}

.alert-info {
    background-color: #dbeafe;
    border: 1px solid #3b82f6;
    color: #1e40af;
}

.prompt-result-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.prompt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    font-weight: bold;
    color: #374151;
}

.copy-btn {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
}

.copy-btn:hover {
    background: #2563eb;
}

.prompt-content {
    background: #f9fafb;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    line-height: 1.5;
}

.analysis-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    text-align: center;
}

.analysis-label {
    font-size: 0.75rem;
    color: #6b7280;
    margin-bottom: 0.5rem;
}

.analysis-value {
    font-size: 1rem;
    font-weight: bold;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

# 메인 UI
st.title("🧠 PromptOS - 자연어 기반 프롬프트 생성기")
st.markdown("AI가 당신의 요청을 이해하고 최적의 프롬프트를 생성합니다")

# 사용자 입력
user_input = st.text_area(
    "작업 설명을 입력하세요",
    placeholder="예: 예비창업자 패키지용 사업계획서를 작성해줘",
    height=100
)

# 제출 버튼
if st.button("🚀 프롬프트 생성", type="primary"):
    if user_input.strip():
        try:
            # 프롬프트 정리
            cleaned_input = sanitize_prompt(user_input)
            logger.info(f"프롬프트 생성 시작: {cleaned_input}")
            
            # 의도 분류
            logger.info("의도 분류 시작...")
            intent_result = classify_intent(cleaned_input)
            logger.info(f"의도 분류 결과: {intent_result}")
            
            # LLM 의도 분류 결과 추출
            if isinstance(intent_result, dict):
                llm_intent = intent_result.get('intent', 'unknown')
            else:
                llm_intent = str(intent_result)
            
            logger.info(f"LLM 의도 분류 결과: {llm_intent}")
            
            # 새로운 템플릿 시스템 사용
            if llm_intent != "unknown":
                logger.info(f"새로운 프롬프트 빌더 사용: {llm_intent}")
                
                # 한국어 의도로 매핑
                korean_intent_mapping = {
                    "business_plan": "사업계획서 작성",
                    "email": "이메일 작성",
                    "report": "보고서 작성",
                    "explanation": "설명문 작성",
                    "customer_service": "고객 응대",
                    "marketing": "홍보문구",
                    "planning": "계획 수립",
                    "summary": "요약 요청"
                }
                
                korean_intent = korean_intent_mapping.get(llm_intent, "unknown")
                logger.info(f"한국어 의도 매핑: {korean_intent}")
                
                # 프롬프트 생성
                final_prompt = build_prompt(korean_intent, cleaned_input)
                logger.info(f"프롬프트 생성 완료: 길이={len(final_prompt)}")
                
                # 프롬프트 결과 카드
                escaped_prompt = final_prompt.replace('`', '\\`').replace('${', '\\${')
                st.markdown(f"""
                <div class="prompt-result-card">
                    <div class="prompt-header">
                        <span>📝 생성된 프롬프트</span>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped_prompt}`)">📋 복사하기</button>
                    </div>
                    <div class="prompt-content">{escaped_prompt}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 분석 결과 카드
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("""
                    <div class="analysis-card">
                        <div class="analysis-label">의도</div>
                        <div class="analysis-value">{}</div>
                    </div>
                    """.format(korean_intent), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="analysis-card">
                        <div class="analysis-label">도메인</div>
                        <div class="analysis-value">{}</div>
                    </div>
                    """.format(intent_result.get('domain', 'N/A')), unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="analysis-card">
                        <div class="analysis-label">대상</div>
                        <div class="analysis-value">{}</div>
                    </div>
                    """.format(intent_result.get('audience', 'N/A')), unsafe_allow_html=True)
                
                with col4:
                    status = "템플릿" if llm_intent != "unknown" else "AI 생성"
                    st.markdown("""
                    <div class="analysis-card">
                        <div class="analysis-label">상태</div>
                        <div class="analysis-value">{}</div>
                    </div>
                    """.format(status), unsafe_allow_html=True)
                
                # LLM 응답 생성
                with st.spinner("AI가 응답을 생성하고 있습니다..."):
                    llm_response = run_final_llm_response(final_prompt)
                    logger.info(f"LLM 응답 생성 완료: 길이={len(llm_response)}")
                
                # LLM 응답 표시 - 구조화된 형태
                st.markdown("### ✨ AI 응답")
                
                # 응답을 구조화하여 표시
                if llm_response.startswith("❌"):
                    # 오류 메시지인 경우
                    st.error(llm_response)
                else:
                    # 성공적인 응답인 경우 구조화하여 표시
                    display_structured_response(llm_response, korean_intent)
                    
                    # 전체 응답 복사 버튼
                    escaped_response = llm_response.replace('`', '\\`').replace('${', '\\${')
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: 1rem;">
                        <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped_response}`)" style="background: #4CAF50; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">
                            📋 전체 응답 복사하기
                        </button>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                logger.info("의도 분류 실패. 기본 fallback 사용")
                
                st.markdown("""
                <div class="custom-alert alert-warning">
                    <span style="font-size: 1.5rem;">⚠️</span>
                    <div>
                        <strong>AI가 요청을 이해하지 못했습니다</strong><br>
                        다른 표현으로 다시 시도해보세요.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 기본 fallback 템플릿 사용
                final_prompt = f"사용자 요청에 대한 응답을 생성합니다: {cleaned_input}"
                
                # fallback 프롬프트 결과 카드
                escaped_prompt = final_prompt.replace('`', '\\`').replace('${', '\\${')
                st.markdown(f"""
                <div class="prompt-result-card">
                    <div class="prompt-header">
                        <span>📝 기본 프롬프트</span>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped_prompt}`)">📋 복사하기</button>
                    </div>
                    <div class="prompt-content">{escaped_prompt}</div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            logger.error(f"프롬프트 생성 중 오류 발생: {e}")
            st.error(f"❌ 오류가 발생했습니다: {e}")
    else:
        st.warning("⚠️ 작업 설명을 입력해주세요.")

# 사용 예시
with st.expander("💡 사용 예시"):
    st.markdown("""
    ### 📋 지원하는 작업 유형
    
    **📊 사업계획서 작성**
    - "예비창업자 패키지용 사업계획서를 작성해줘"
    - "AI 스타트업 사업계획서가 필요해"
    
    **📧 이메일 작성**
    - "고객에게 정중한 이메일을 작성해줘"
    - "업무 협력 제안 이메일을 보내야 해"
    
    **📋 보고서 작성**
    - "분기별 실적 보고서를 작성해줘"
    - "프로젝트 진행상황 보고서가 필요해"
    
    **📖 설명문 작성**
    - "비전문가가 이해할 수 있도록 설명해줘"
    - "복잡한 기술을 쉽게 설명해줘"
    
    **👥 고객 응대**
    - "고객 문의에 친절하게 응답해줘"
    - "클레임 처리 방법을 알려줘"
    
    **📢 홍보문구**
    - "제품 홍보 문구를 만들어줘"
    - "서비스 소개 문구가 필요해"
    
    **📅 계획 수립**
    - "월간 업무 계획을 수립해줘"
    - "프로젝트 일정 계획이 필요해"
    
    **📝 요약 요청**
    - "긴 문서를 요약해줘"
    - "핵심 내용만 정리해줘"
    """)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    🧠 PromptOS - 자연어 기반 프롬프트 생성기<br>
    AI가 당신의 요청을 이해하고 최적의 프롬프트를 생성합니다
</div>
""", unsafe_allow_html=True) 