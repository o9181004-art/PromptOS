# app.py

import streamlit as st
import time
import json
import os
import sys
import logging
from intent_classifier import classify_intent
from template_system import get_template, fill_template
from prompt_builder import extract_placeholders
from keyword_classifier import KeywordClassifier
from domain_inference import DomainInference
from prompt_generator import process_user_request

# 디버깅을 위한 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 페이지 설정
st.set_page_config(
    page_title="PromptOS 자연어 생성기",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""
if 'show_examples' not in st.session_state:
    st.session_state.show_examples = False
if 'selected_example' not in st.session_state:
    st.session_state.selected_example = ""
if 'consecutive_failures' not in st.session_state:
    st.session_state.consecutive_failures = 0
if 'last_failure_time' not in st.session_state:
    st.session_state.last_failure_time = None
if 'followup_mode' not in st.session_state:
    st.session_state.followup_mode = False
if 'selected_intent' not in st.session_state:
    st.session_state.selected_intent = None

# 조건 추출 함수 (시스템 지침에 따라)
def extract_conditions(utterance: str):
    """
    사용자 입력에서 tone, tense, audience 조건을 추출합니다.
    PromptOS 원칙: 기본값을 제공하여 실패하지 않도록 함
    """
    # 기본값 설정 (시스템 지침에 따라)
    conditions = {
        "tone": "genuine",  # genuine, formal, casual
        "tense": "present",  # present, past, future
        "audience": "review panel"  # review panel, customer, expert, student, government
    }
    
    # 사용자 입력에서 키워드 기반으로 조건 추출
    utterance_lower = utterance.lower()
    
    # 톤 추출
    if any(word in utterance_lower for word in ["정중한", "공식", "formal", "비즈니스", "professional", "business"]):
        conditions["tone"] = "formal"
    elif any(word in utterance_lower for word in ["친근한", "캐주얼", "informal", "편안한", "casual", "friendly"]):
        conditions["tone"] = "casual"
    elif any(word in utterance_lower for word in ["진정성", "genuine", "authentic", "sincere"]):
        conditions["tone"] = "genuine"
    
    # 시제 추출
    if any(word in utterance_lower for word in ["과거", "했어", "했던", "past", "completed", "finished"]):
        conditions["tense"] = "past"
    elif any(word in utterance_lower for word in ["미래", "할거야", "예정", "future", "will", "going to"]):
        conditions["tense"] = "future"
    elif any(word in utterance_lower for word in ["현재", "지금", "present", "current", "now"]):
        conditions["tense"] = "present"
    
    # 청중 추출
    if any(word in utterance_lower for word in ["고객", "customer", "클라이언트", "client"]):
        conditions["audience"] = "customer"
    elif any(word in utterance_lower for word in ["전문가", "expert", "개발자", "엔지니어", "specialist"]):
        conditions["audience"] = "expert"
    elif any(word in utterance_lower for word in ["학생", "초보자", "beginner", "student"]):
        conditions["audience"] = "student"
    elif any(word in utterance_lower for word in ["정부", "government", "공무원", "official"]):
        conditions["audience"] = "government"
    elif any(word in utterance_lower for word in ["검토", "review", "평가", "evaluation", "심사", "panel"]):
        conditions["audience"] = "review panel"
    
    return conditions

# fallback 용도: 주요 키워드 기반 보정 (시스템 지침에 따라)
fallback_keywords = {
    "business_plan": ["사업계획서", "창업계획서", "예비창업자", "창업지원", "비즈니스모델", "사업계획", "business plan", "startup", "proposal", "idea", "비즈니스", "창업", "사업"],
    "report_summary": ["요약", "정리", "분석 결과", "리포트", "요약문", "정리문", "summary", "report"],
    "self_intro": ["자기소개", "소개서", "지원동기", "자기소개서", "introduction", "소개"],
    "proposal": ["제안서", "제안", "proposal", "기획서", "제안안"],
    "marketing_copy": ["마케팅", "광고", "홍보", "마케팅콘텐츠", "광고문구", "marketing", "advertisement"],
    "customer_reply": ["고객응대", "고객문의", "고객답변", "고객서비스", "customer", "응대"],
    "email": ["이메일", "email", "메일", "편지", "mail"],
    "summary_meeting": ["회의록", "회의요약", "미팅록", "회의정리", "meeting", "회의"]
}

def fallback_intent_check(user_input):
    """
    키워드 기반 fallback 의도 분류
    """
    user_input_lower = user_input.lower()
    for intent, keywords in fallback_keywords.items():
        if any(keyword in user_input_lower for keyword in keywords):
            return intent
    return None

def handle_unknown_intent(utterance):
    """
    의도 분류 실패 시 처리
    PromptOS 원칙: AI가 사용자에게 적응해야 함 - 절대 실패하지 않음
    """
    fallback_intent = fallback_intent_check(utterance)
    
    if fallback_intent:
        logger.info(f"Fallback 키워드 매칭 성공: {fallback_intent}")
        return fallback_intent
    else:
        # 시스템 지침: 기본적으로 business_plan으로 fallback
        logger.info("키워드 매칭 실패, 기본 business_plan으로 fallback")
        
        # 사용자에게 알림
        st.markdown(f"""
        <div class="custom-alert alert-info">
            <span style="font-size: 1.2rem;">💡</span>
            <div>
                <strong>기본 사업계획서 모드로 설정</strong><br>
                입력을 완전히 이해하지 못했지만, 기본 사업계획서 프롬프트를 생성합니다.
                <br><br>
                <em>더 정확한 결과를 원하시면 "사업계획서", "제안서", "자기소개서" 등의 키워드를 포함해주세요.</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return "business_plan"  # 기본 fallback

def followup_question_mode(question):
    """
    Follow-up 질문 모드로 전환
    """
    st.markdown(f"""
    <div class="custom-alert alert-warning">
        <span style="font-size: 1.5rem;">🤔</span>
        <div>
            <strong>의도를 명확히 해주세요</strong><br>
            {question}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 의도 선택 버튼들
    st.markdown("### 🎯 의도 선택")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 사업계획서 작성", use_container_width=True):
            st.session_state.selected_intent = "business_plan"
            st.session_state.followup_mode = True
            st.rerun()
        
        if st.button("📝 자기소개서 작성", use_container_width=True):
            st.session_state.selected_intent = "self_intro"
            st.session_state.followup_mode = True
            st.rerun()
    
    with col2:
        if st.button("📄 제안서 작성", use_container_width=True):
            st.session_state.selected_intent = "proposal"
            st.session_state.followup_mode = True
            st.rerun()
        
        if st.button("📊 보고서/요약", use_container_width=True):
            st.session_state.selected_intent = "report_summary"
            st.session_state.followup_mode = True
            st.rerun()
    
    with col3:
        if st.button("📧 이메일 작성", use_container_width=True):
            st.session_state.selected_intent = "email"
            st.session_state.followup_mode = True
            st.rerun()
        
        if st.button("🎯 마케팅 콘텐츠", use_container_width=True):
            st.session_state.selected_intent = "marketing_copy"
            st.session_state.followup_mode = True
            st.rerun()
    
    st.markdown("---")
    st.markdown("**💡 다른 의도가 있으시면 아래에 직접 입력해주세요:**")
    
    custom_intent = st.text_input(
        "직접 입력",
        placeholder="예: 고객 응대, 회의록 작성 등",
        key="custom_intent_input"
    )
    
    if st.button("✅ 선택 완료", use_container_width=True):
        if custom_intent:
            st.session_state.selected_intent = custom_intent
        st.session_state.followup_mode = True
        st.rerun()
    
    st.stop()

# 실패 로깅 함수
def log_failure(utterance: str, error_type: str, error_message: str):
    """
    실패한 입력을 로깅합니다.
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] FAILURE - Input: '{utterance}' | Type: {error_type} | Error: {error_message}\n"
    
    # 로그 파일에 저장
    try:
        with open("failure_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        logger.error(f"로그 파일 작성 실패: {e}")
    
    # 세션 상태 업데이트
    st.session_state.consecutive_failures += 1
    st.session_state.last_failure_time = timestamp

# 클립보드 복사 JavaScript 함수
def create_copy_js(text_to_copy):
    return f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText(`{text_to_copy}`).then(function() {{
            console.log('Copied to clipboard');
        }}).catch(function(err) {{
            console.error('Failed to copy: ', err);
        }});
    }}
    </script>
    """

# 튜토리얼 오버레이 함수
def show_tutorial_overlay():
    """
    연속 실패 시 튜토리얼 오버레이를 표시합니다.
    """
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                background: rgba(0,0,0,0.8); z-index: 1000; display: flex; 
                align-items: center; justify-content: center;">
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    max-width: 500px; text-align: center;">
            <h3>💡 사용 팁</h3>
            <p>더 나은 결과를 위해 다음과 같이 입력해보세요:</p>
            <ul style="text-align: left;">
                <li><strong>구체적으로:</strong> "AI 기반 제안서를 정부에 제출할거야"</li>
                <li><strong>목적을 명확히:</strong> "고객을 위한 정중한 이메일을 작성해줘"</li>
                <li><strong>대상을 지정:</strong> "학생들을 위한 간단한 설명이 필요해"</li>
            </ul>
            <button onclick="this.parentElement.parentElement.style.display='none'" 
                    style="background: #3B82F6; color: white; border: none; 
                           padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                알겠습니다
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 고급 CSS 스타일
def load_premium_css():
    theme_vars = {
        'bg_primary': '#FAFBFC',
        'bg_secondary': '#FFFFFF',
        'bg_tertiary': '#F6F8FA',
        'text_primary': '#1F2328',
        'text_secondary': '#656D76',
        'border_color': '#D1D9E0',
        'accent_color': '#3B82F6',
        'success_color': '#10B981',
        'warning_color': '#F59E0B',
        'error_color': '#EF4444'
    }

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background: {theme_vars['bg_primary']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* 입력 섹션 */
    .input-section {{
        margin-bottom: 2rem;
    }}

    .stTextInput > div > div > input {{
        background: {theme_vars['bg_secondary']};
        color: {theme_vars['text_primary']};
        border: 2px solid {theme_vars['border_color']};
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {theme_vars['accent_color']};
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        outline: none;
    }}

    .stButton > button {{
        margin-top: 1rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 10px;
        font-size: 0.95rem;
        background: linear-gradient(135deg, {theme_vars['accent_color']} 0%, #1D4ED8 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(59, 130, 246, 0.3);
    }}



    /* 프롬프트 결과 카드 */
    .prompt-result-card {{
        background: {theme_vars['bg_secondary']};
        border: 2px solid {theme_vars['accent_color']};
        border-radius: 16px;
        margin-top: 2rem;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
    }}

    .prompt-header {{
        background: linear-gradient(135deg, {theme_vars['accent_color']} 0%, #1D4ED8 100%);
        color: white;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .prompt-content {{
        padding: 2rem;
        font-family: 'Malgun Gothic', '맑은 고딕', 'Noto Sans KR', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        color: {theme_vars['text_primary']};
        white-space: pre-wrap;
        background: {theme_vars['bg_tertiary']};
        margin: 0;
        font-weight: 400;
    }}

    .copy-btn {{
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        font-size: 0.875rem;
    }}

    .copy-btn:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }}

    /* 카드 */
    .premium-card {{
        background: {theme_vars['bg_secondary']};
        border: 1px solid {theme_vars['border_color']};
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }}

    .premium-card:hover {{
        border-color: {theme_vars['accent_color']};
    }}

    /* 메트릭 카드 */
    .metric-card {{
        background: {theme_vars['bg_tertiary']};
        border: 1px solid {theme_vars['border_color']};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .metric-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.1);
    }}

    .metric-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }}

    .metric-label {{
        font-size: 0.75rem;
        font-weight: 500;
        color: {theme_vars['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .metric-value {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {theme_vars['accent_color']};
    }}

    /* 반응형 */
    @media (max-width: 768px) {{
        .input-section {{
            margin-bottom: 1rem;
        }}
        .stTextInput > div > div > input {{
            font-size: 0.9rem;
            padding: 0.65rem 0.9rem;
        }}
        .stButton > button {{
            font-size: 0.9rem;
            padding: 0.6rem 1.2rem;
        }}
    }}

    /* Hero 헤더 스타일 */
    .hero-header {{
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
        position: relative;
        overflow: hidden;
    }}

    .hero-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }}

    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -0.02em;
    }}

    .hero-subtitle {{
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}

    /* 애니메이션 효과 */
    .fade-in-up {{
        animation: fadeInUp 0.8s ease-out;
    }}

    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* 다크모드 토글 스타일 */
    .dark-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(139, 92, 246, 0.1);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 50px;
        padding: 0.5rem;
        cursor: pointer;
        font-size: 1.2rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        z-index: 1000;
    }}

    .dark-toggle:hover {{
        background: rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.5);
        transform: scale(1.1);
    }}

    /* 알림 스타일 */
    .custom-alert {{
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        border-left: 4px solid;
    }}

    .alert-success {{
        background: rgba(16, 185, 129, 0.1);
        border-left-color: #10B981;
        color: #065F46;
    }}

    .alert-warning {{
        background: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
        color: #92400E;
    }}

    .alert-error {{
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #EF4444;
        color: #991B1B;
    }}

    /* 예시 툴팁 스타일 */
    .example-tooltip {{
        background: rgba(139, 92, 246, 0.05);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}

    /* 모바일 반응형 Hero */
    @media (max-width: 768px) {{
        .hero-header {{
            padding: 2rem 1rem;
            margin: 1rem 0;
        }}
        
        .hero-title {{
            font-size: 2.5rem;
        }}
        
        .hero-subtitle {{
            font-size: 1rem;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS 로드
load_premium_css()



# 히어로 헤더
st.markdown("""
<div class="hero-header fade-in-up">
    <div class="hero-title">🧠 PromptOS</div>
    <div class="hero-subtitle">자연어를 완벽한 AI 프롬프트로 변환하는 지능형 생성기</div>
</div>
""", unsafe_allow_html=True)

# 메인 레이아웃
left_col, right_col = st.columns([1, 1], gap="large")

# 좌측: 기능 설명
with left_col:
    st.markdown("### ✨ 핵심 기능")
    
    features = [
        {"icon": "🎯", "title": "지능형 의도 분류", "desc": "자연어 입력을 분석하여 최적의 템플릿을 자동 선택"},
        {"icon": "⚡", "title": "실시간 조건 추출", "desc": "톤, 시제, 대상을 즉시 인식하여 맞춤형 프롬프트 생성"},
        {"icon": "🎨", "title": "다양한 템플릿", "desc": "업무, 창작, 분석 등 전문 도메인별 특화 템플릿"},
        {"icon": "📋", "title": "원클릭 복사", "desc": "생성된 프롬프트를 클립보드에 즉시 복사"}
    ]
    
    for feature in features:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1rem 0; padding: 1rem; background: rgba(59, 130, 246, 0.05); border-radius: 8px;">
            <span style="font-size: 1.5rem; margin-right: 1rem;">{feature['icon']}</span>
            <div>
                <div style="font-weight: 600; margin-bottom: 0.25rem;">{feature['title']}</div>
                <div style="font-size: 0.875rem; opacity: 0.8;">{feature['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 우측: 입력 및 결과
with right_col:
    st.markdown("### 🧠 자연어로 원하는 작업을 설명해주세요")
    
    # 메인 입력 필드 (단일)
    utterance = st.text_input(
        "입력",
        value=st.session_state.selected_example,
        placeholder="예: AI 기반 제안서를 정부에 제출할거야",
        key="main_input",
        help="구체적이고 명확하게 작성할수록 더 정확한 프롬프트가 생성됩니다",
        label_visibility="collapsed"
    )
    
    # 생성 버튼 (여백 추가)
    st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
    generate_btn = st.button("✍️ 프롬프트 생성하기", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 예시 토글 버튼 (중앙 정렬) - 인라인 스타일 적용
    st.markdown("""
    <style>
    .example-toggle-btn button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .example-toggle-btn button:hover {
        background: linear-gradient(135deg, #5a6fd8, #6a4190) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="example-toggle-btn">', unsafe_allow_html=True)
    if st.button("💡 사용 예시 보기", use_container_width=True):
        st.session_state.show_examples = not st.session_state.show_examples
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 예시 말풍선
    if st.session_state.show_examples:
        examples = [
            "AI 기반 제안서를 정부에 제출할거야",
            "고객을 위한 정중한 이메일을 작성해줘", 
            "창의적인 마케팅 콘텐츠를 만들어야 해",
            "학생들을 위한 간단한 설명이 필요해"
        ]
        
        st.markdown("""
        <style>
        .example-buttons button {
            background: linear-gradient(135deg, #f093fb, #f5576c) !important;
            color: white !important;
            box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        .example-buttons button:hover {
            background: linear-gradient(135deg, #e885f7, #e54b60) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 20px 50px rgba(240, 147, 251, 0.5) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="example-buttons">', unsafe_allow_html=True)
        for example in examples:
            if st.button(f"'{example}'", key=f"example_{hash(example)}", use_container_width=True):
                st.session_state.selected_example = example
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Follow-up 모드에서 선택된 의도 처리
if st.session_state.followup_mode and st.session_state.selected_intent:
    logger.info(f"Follow-up 모드에서 선택된 의도: {st.session_state.selected_intent}")
    
    # 선택된 의도로 프롬프트 생성
    intent = st.session_state.selected_intent
    sub_intent = None
    domain = "general"
    audience = "general"
    
    # 조건 추출
    conditions = extract_conditions(utterance)
    tone = conditions.get("tone", "중립적")
    tense = conditions.get("tense", "현재시제")
    
    # Follow-up 모드 리셋
    st.session_state.followup_mode = False
    st.session_state.selected_intent = None
    
    st.markdown(f"""
    <div class="custom-alert alert-success">
        <span style="font-size: 1.2rem;">✅</span>
        <div>
            <strong>의도 선택 완료</strong><br>
            선택된 의도: <code>{intent}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 프롬프트 생성 로직 (개선된 버전)
if generate_btn and utterance:
    logger.info(f"프롬프트 생성 시작: {utterance}")
    
    with st.spinner("🤖 AI가 프롬프트를 생성하고 있습니다..."):
        time.sleep(1.5)  # 로딩 효과
        
        try:
            # 새로운 process_user_request 함수 사용 (절대 실패하지 않음)
            logger.info("개선된 프롬프트 생성 시스템 시작...")
            result = process_user_request(utterance)
            
            # 결과 추출
            intent = result["intent"]
            prompt_instruction = result["prompt_instruction"]
            conditions = result["conditions"]
            
            # 조건 정보
            tone = conditions["tone"]
            tense = conditions["tense"]
            audience = conditions["audience"]
            
            logger.info(f"프롬프트 생성 완료: intent={intent}, tone={tone}, tense={tense}, audience={audience}")
            
            # 성공 메시지 표시
            st.markdown(f"""
            <div class="custom-alert alert-success">
                <span style="font-size: 1.2rem;">✅</span>
                <div>
                    <strong>프롬프트 생성 완료</strong><br>
                    의도: <code>{intent}</code> | 톤: <code>{tone}</code> | 대상: <code>{audience}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            

            
            # 생성된 프롬프트 지시사항 표시
            st.markdown(f"""
            <div class="prompt-result-card fade-in-up">
                <div class="prompt-header">
                    <span>📋 생성된 프롬프트 지시사항</span>
                    <button class="copy-btn" onclick="copyToClipboard()">📋 복사하기</button>
                </div>
                <div class="prompt-content">{prompt_instruction}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript for clipboard copy
            st.markdown(create_copy_js(prompt_instruction.replace("'", "\\'")), unsafe_allow_html=True)
            
            # 성공 시 연속 실패 카운터 리셋
            st.session_state.consecutive_failures = 0
            
        except Exception as e:
            logger.error(f"프롬프트 생성 중 오류 발생: {e}")
            
            # 오류 발생 시에도 fallback 처리
            st.markdown(f"""
            <div class="custom-alert alert-warning">
                <span style="font-size: 1.2rem;">⚠️</span>
                <div>
                    <strong>시스템 오류 발생</strong><br>
                    기본 프롬프트를 생성합니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 기본 fallback 프롬프트 생성
            fallback_prompt = f"""
사용자의 요청에 맞는 전문적인 프롬프트를 생성해주세요.

사용자 입력: {utterance}

다음 기준에 따라 프롬프트를 작성해주세요:
1. 명확하고 구체적인 지침
2. 전문적이고 효과적인 표현
3. 사용자의 목적에 맞는 구조화된 내용
4. 실행 가능한 단계별 가이드

전문적이고 효과적인 프롬프트를 생성해주세요.
"""
            
            # 생성된 프롬프트 표시
            st.markdown(f"""
            <div class="prompt-result-card fade-in-up">
                <div class="prompt-header">
                    <span>📝 기본 프롬프트 (Fallback)</span>
                    <button class="copy-btn" onclick="copyToClipboard()">📋 복사하기</button>
                </div>
                <div class="prompt-content">{fallback_prompt}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript for clipboard copy
            st.markdown(create_copy_js(fallback_prompt.replace("'", "\\'")), unsafe_allow_html=True)
            
            # 상세한 에러 정보 수집
            error_traceback = traceback.format_exc()
            error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 에러 로그 파일에 기록
            try:
                logs_dir = "logs"
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir)
                
                today = datetime.now().strftime("%Y%m%d")
                log_file = os.path.join(logs_dir, f"error_{today}.log")
                
                log_entry = f"""
[{error_time}] PROMPT_GENERATION_ERROR
Input: '{utterance}'
Error: {str(e)}
Traceback:
{error_traceback}
{'='*80}
"""
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                
                logger.error(f"프롬프트 생성 오류가 로그 파일에 기록되었습니다: {log_file}")
                
            except Exception as log_error:
                logger.error(f"로그 파일 작성 실패: {log_error}")
            
            # 사용자에게 친절한 에러 메시지 표시
            st.markdown(f"""
            <div class="custom-alert alert-error">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div>
                    <strong>프롬프트 생성 중 오류 발생</strong><br>
                    시스템에서 예상치 못한 오류가 발생했습니다.
                    <br><br>
                    <strong>🔧 해결 방법:</strong>
                    <ul>
                        <li>입력 내용을 다시 확인해보세요</li>
                        <li>페이지를 새로고침 후 다시 시도해보세요</li>
                        <li>문제가 지속되면 관리자에게 문의하세요</li>
                    </ul>
                    <details>
                        <summary>기술적 오류 정보 (관리자용)</summary>
                        <code>시간: {error_time}</code><br>
                        <code>입력: {utterance}</code><br>
                        <code>오류: {str(e)}</code><br>
                        <code>로그 파일: logs/error_{today}.log</code>
                    </details>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif generate_btn and not utterance:
    st.markdown("""
    <div class="custom-alert alert-warning">
        <span style="font-size: 1.2rem;">💡</span>
        <div><strong>입력이 필요합니다</strong><br>자연어 입력란에 내용을 작성한 후 다시 시도해주세요.</div>
    </div>
    """, unsafe_allow_html=True)

# 사용된 프롬프트 히스토리 (선택사항)
if st.session_state.generated_prompt:
    with st.expander("📚 생성된 프롬프트 히스토리"):
        st.code(st.session_state.generated_prompt, language="text")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem 2rem; opacity: 0.7;">
    <div style="font-size: 1.5rem; margin-bottom: 1rem;">🚀</div>
    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">PromptOS</div>
    <div style="font-size: 0.9rem;">AI 기반 자연어 프롬프트 생성 플랫폼</div>
    <div style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.6;">더 나은 AI 상호작용을 위한 스마트 솔루션</div>
</div>
""", unsafe_allow_html=True)