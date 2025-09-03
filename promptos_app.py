"""
PromptOS Streamlit App
기존 HTML UI와 Python 백엔드를 연동하는 메인 애플리케이션
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# core 모듈에서 prompt_engine 가져오기
try:
    from core.prompt_engine import prompt_engine
    print("✅ prompt_engine 로드 성공")
except ImportError as e:
    print(f"❌ prompt_engine 로드 실패: {e}")
    # fallback: 기존 모듈들 사용
    try:
        from prompt_generator import generate_prompt
        from llm_utils import classify_intent_llm
        from fallback_manager import FallbackManager
        
        class FallbackPromptEngine:
            def __init__(self):
                self.fallback_manager = FallbackManager()
            
            def generate_prompt_from_input(self, user_input):
                try:
                    intent = classify_intent_llm(user_input).strip().lower()
                    if intent == "unknown":
                        fallback_prompt = self.fallback_manager.generate_prompt_with_llm(user_input)
                        return {
                            'success': True,
                            'prompt': fallback_prompt,
                            'intent': 'fallback',
                            'method': 'llm_fallback'
                        }
                    
                    generated_prompt = generate_prompt(intent, user_input)
                    if generated_prompt:
                        return {
                            'success': True,
                            'prompt': generated_prompt,
                            'intent': intent,
                            'method': 'template_based'
                        }
                    else:
                        fallback_prompt = self.fallback_manager.generate_prompt_with_llm(user_input, intent)
                        return {
                            'success': True,
                            'prompt': fallback_prompt,
                            'intent': intent,
                            'method': 'llm_fallback'
                        }
                except Exception as e:
                    return {
                        'success': False,
                        'error': str(e),
                        'prompt': None,
                        'intent': None
                    }
            
            def clear_input(self):
                return {
                    'success': True,
                    'message': '입력이 초기화되었습니다.'
                }
        
        prompt_engine = FallbackPromptEngine()
        print("✅ fallback prompt_engine 생성 완료")
    except ImportError as e2:
        print(f"❌ fallback 모듈 로드도 실패: {e2}")
        # 최종 fallback: 모의 응답
        class MockPromptEngine:
            def generate_prompt_from_input(self, user_input):
                return {
                    'success': True,
                    'prompt': f"모의 프롬프트 응답: {user_input}",
                    'intent': 'mock',
                    'method': 'mock_response'
                }
            
            def clear_input(self):
                return {
                    'success': True,
                    'message': '입력이 초기화되었습니다.'
                }
        
        prompt_engine = MockPromptEngine()
        print("✅ mock prompt_engine 생성 완료")

def load_html_file(file_path):
    """HTML 파일을 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"HTML 파일을 찾을 수 없습니다: {file_path}")
        return None
    except Exception as e:
        st.error(f"HTML 파일 로드 중 오류 발생: {e}")
        return None

def create_api_endpoint():
    """Streamlit API 엔드포인트를 생성합니다."""
    @st.cache_data  # updated from experimental_memo to cache_data
    def generate_prompt_api(user_input):
        """프롬프트 생성 API"""
        try:
            result = prompt_engine.generate_prompt_from_input(user_input)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'prompt': None,
                'intent': None
            }
    
    @st.cache_data  # updated from experimental_memo to cache_data
    def clear_input_api():
        """입력 초기화 API"""
        try:
            result = prompt_engine.clear_input()
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    return generate_prompt_api, clear_input_api

def main():
    """메인 애플리케이션"""
    st.set_page_config(
        page_title="PromptOS - AI Prompt Platform",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 고품질 글래스모피즘 스타일 적용
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
                 * {
             font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
             line-height: 1.6;
             letter-spacing: 0.3px;
         }
        
        .main > div { padding-top: 0; }
        .stApp { 
            background: linear-gradient(135deg, #0f0f23 0%, #1a1b3c 25%, #2d1b69 50%, #4a1b8a 75%, #6b1baa 100%);
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* 전체 페이지 스타일 */
        .stApp > div > div {
            background: transparent !important;
        }
        
        /* 제목 스타일 - 네온 글로우 효과 */
        .main h1 {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 800 !important;
            font-size: 3rem !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.5), 0 0 40px rgba(102, 126, 234, 0.3) !important;
            background: linear-gradient(135deg, #ffffff 0%, #667eea 50%, #764ba2 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        .main p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: 400 !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
        }
        
        /* 구분선 스타일 - 네온 효과 */
        .main hr {
            border: none !important;
            height: 2px !important;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.8), rgba(255,255,255,0.8), rgba(102, 126, 234, 0.8), transparent) !important;
            margin: 3rem 0 !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.5) !important;
        }
        
                 /* 입력 영역 스타일 - 균형잡힌 글래스모피즘 */
         .stTextArea > div > div > textarea {
             background: rgba(255, 255, 255, 0.05) !important;
             backdrop-filter: blur(20px) !important;
             border: 1px solid rgba(255, 255, 255, 0.15) !important;
             border-radius: 20px !important;
             color: #ffffff !important;
             font-family: 'Inter', sans-serif !important;
             font-size: 16px !important;
             font-weight: 400 !important;
             line-height: 1.5 !important;
             padding: 1rem !important;
             height: 120px !important;
             min-height: 120px !important;
             max-height: 120px !important;
             display: flex !important;
             align-items: center !important;
             justify-content: center !important;
             box-shadow: 
                 0 8px 32px rgba(0, 0, 0, 0.3),
                 inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
             transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
             resize: none !important;
             letter-spacing: 0.3px !important;
         }
        
        .stTextArea > div > div > textarea:focus {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(102, 126, 234, 0.5) !important;
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.15),
                0 0 0 1px rgba(102, 126, 234, 0.2),
                0 0 15px rgba(102, 126, 234, 0.2) !important;
            transform: translateY(-1px) !important;
        }
        
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
            font-weight: 400 !important;
            line-height: 1.5 !important;
        }
        
        /* 라벨 스타일 */
        .stTextArea > label {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.8rem !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
        }
        
                 /* 버튼 컨테이너 스타일 */
         .stButton {
             display: flex !important;
             gap: 1rem !important;
             width: 100% !important;
         }
         
         /* 모든 버튼 공통 적용 */
         div.stButton > button {
             height: 60px !important;
             width: 100% !important;
             flex: 1 !important;
             font-size: 18px !important;
             font-weight: 600 !important;
             display: flex !important;
             justify-content: center !important;
             align-items: center !important;
             background: linear-gradient(to right, #9146FF, #6A00FF) !important;
             color: white !important;
             border-radius: 12px !important;
             border: none !important;
             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
             transition: all 0.2s ease-in-out !important;
             font-family: 'Inter', sans-serif !important;
             position: relative !important;
             overflow: hidden !important;
             padding: 1.2rem 0 !important;
             text-align: center !important;
             letter-spacing: 0.3px !important;
         }

        /* 마우스 호버 시 */
        div.stButton > button:hover {
            transform: scale(1.03) !important;
            background: linear-gradient(to right, #A164FF, #8546FF) !important;
        }
        

        
        /* 결과 영역 스타일 - 글래스모피즘 */
        .stSuccess {
            background: rgba(76, 175, 80, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(76, 175, 80, 0.3) !important;
            border-radius: 20px !important;
            color: #4caf50 !important;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2) !important;
        }
        
        .stError {
            background: rgba(244, 67, 54, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(244, 67, 54, 0.3) !important;
            border-radius: 20px !important;
            color: #f44336 !important;
            box-shadow: 0 8px 25px rgba(244, 67, 54, 0.2) !important;
        }
        
        .stWarning {
            background: rgba(255, 152, 0, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 152, 0, 0.3) !important;
            border-radius: 20px !important;
            color: #ff9800 !important;
            box-shadow: 0 8px 25px rgba(255, 152, 0, 0.2) !important;
        }
        
        .stInfo {
            background: rgba(33, 150, 243, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(33, 150, 243, 0.3) !important;
            border-radius: 20px !important;
            color: #2196f3 !important;
            box-shadow: 0 8px 25px rgba(33, 150, 243, 0.2) !important;
        }
        
        /* 코드 블록 스타일 - 다크 글래스모피즘 */
        .stCodeBlock {
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        }
        
        /* 제목 스타일 */
        .main h3 {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            margin: 2rem 0 1.5rem 0 !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.3) !important;
        }
        
        /* 스피너 스타일 - 네온 효과 */
        .stSpinner > div {
            border-color: #667eea !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.5) !important;
        }
        

        
        /* 푸터 스타일 */
        .footer {
            text-align: center;
            color: #ccc;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 400;
            margin-top: 4rem;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .footer p {
            margin: 0.3rem 0;
            color: #ccc !important;
            text-shadow: 0 0 5px rgba(204, 204, 204, 0.3);
        }
        
        /* 기능 카드 스타일 - 고급 글래스모피즘 */
        .feature-card {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 25px !important;
            padding: 2rem !important;
            text-align: center !important;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .feature-card:hover {
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 
                0 15px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2),
                0 0 30px rgba(102, 126, 234, 0.2) !important;
        }
        
        .feature-card::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
            opacity: 0 !important;
            transition: opacity 0.3s ease !important;
        }
        
        .feature-card:hover::before {
            opacity: 1 !important;
        }
        
        .feature-icon {
            font-size: 3rem !important;
            margin-bottom: 1.5rem !important;
            display: block !important;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.5) !important;
        }
        
        .feature-title {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            margin: 0 0 1rem 0 !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
        }
        
        .feature-description {
            color: rgba(255, 255, 255, 0.8) !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
            margin: 0 !important;
        }
        
                 /* 빠른 시작 예시 그리드 컨테이너 */
         .quick-start-grid {
             display: grid !important;
             grid-template-columns: repeat(3, 1fr) !important;
             gap: 1rem !important;
             max-width: 720px !important;
             margin: 0 auto !important;
             padding: 20px 0 !important;
             justify-items: center !important;
             align-items: center !important;
         }
        
        /* 반응형 그리드 */
        @media (max-width: 768px) {
            .quick-start-grid {
                grid-template-columns: repeat(2, 1fr) !important;
                max-width: 480px !important;
            }
        }
        
        @media (max-width: 600px) {
            .quick-start-grid {
                grid-template-columns: repeat(1, 1fr) !important;
                max-width: 240px !important;
            }
        }
        
                 /* 빠른 시작 버튼 스타일 */
         .quick-button {
             display: flex !important;
             justify-content: center !important;
             align-items: center !important;
             width: 220px !important;
             height: 60px !important;
             font-size: 17px !important;
             font-weight: 600 !important;
             color: white !important;
             border-radius: 12px !important;
             background: linear-gradient(to right, #9146FF, #6A00FF) !important;
             box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
             text-align: center !important;
             font-family: 'Inter', sans-serif !important;
             border: none !important;
             cursor: pointer !important;
             transition: all 0.3s ease !important;
             text-decoration: none !important;
             margin: 0 !important;
             padding: 0 !important;
             letter-spacing: 0.3px !important;
         }
        
        .quick-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.4) !important;
            background: linear-gradient(135deg, #7c8ff0 0%, #8a5db8 50%, #a16ff8 100%) !important;
        }
        
        .quick-button:active {
            transform: translateY(0) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        /* 숨겨진 Streamlit 버튼 스타일 */
        .stButton > button[data-testid*="hidden_example"] {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 220px !important;
            height: 60px !important;
            opacity: 0 !important;
            z-index: 10 !important;
            background: transparent !important;
            border: none !important;
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 직접 fallback UI 표시 (HTML 대신 Streamlit UI 사용)
    show_fallback_ui()

def show_fallback_ui():
    """Streamlit 전용 UI"""
    st.title("🧠 PromptOS - AI Prompt Platform")
    st.markdown("차원이 다른 혁신적인 AI 프롬프트로 변화하는 지능형 생성기")
    
    st.markdown("---")
    
    # 세션 상태 초기화
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'generated_result' not in st.session_state:
        st.session_state.generated_result = None
    
    # 입력 영역
    user_input = st.text_area(
        "자연어로 원하는 작업을 설명해주세요",
        value=st.session_state.user_input,
        placeholder="예: 마케팅 카피를 쓰거나, 기술 문서를 작성하고 싶어요...",
        height=120,
        key="input_text_area"
    )
    
    # 입력값을 session_state에 저장
    st.session_state.user_input = user_input
    
    # 버튼 영역 (적절한 간격 추가)
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        clear_button = st.button("🔥 입력창 초기화", use_container_width=True, key="clear_btn")
        if clear_button:
            st.session_state.user_input = ""
            st.session_state.generated_result = None
            st.rerun()
    
    with col2:
        generate_button = st.button("⚡ 프롬프트 생성하기", use_container_width=True, key="generate_btn")
        if generate_button:
            if user_input.strip():
                with st.spinner("프롬프트를 생성하고 있습니다..."):
                    try:
                        # 직접 프롬프트 생성 로직 호출
                        result = prompt_engine.generate_prompt_from_input(user_input)
                        if result and result.get('success'):
                            st.session_state.generated_result = result
                            st.rerun()
                        else:
                            st.error("프롬프트 생성에 실패했습니다.")
                    except Exception as e:
                        st.error(f"오류 발생: {str(e)}")
                        # 디버깅을 위한 로그
                        st.write(f"Debug: {type(e).__name__}: {e}")
            else:
                                 st.warning("먼저 작업 내용을 입력해주세요.")
    
    # 결과 표시 영역 (적절한 간격 추가)
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    if st.session_state.generated_result:
        result = st.session_state.generated_result
        
        if result['success']:
            st.success("프롬프트 생성 완료!")
            st.markdown("### 생성된 프롬프트:")
            st.code(result['prompt'], language="text")
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.info(f"의도: {result.get('intent', 'N/A')}")
            with col_info2:
                st.info(f"방법: {result.get('method', 'N/A')}")
        else:
            st.error(f"프롬프트 생성 실패: {result.get('error', '알 수 없는 오류')}")
    
    # 빠른 시작 예시
    st.markdown("---")
    st.markdown("### 💡 빠른 시작 예시")
    
    examples = ["마케팅 카피", "기술 문서", "콘텐츠 기획", "이메일 작성", "프레젠테이션", "코드 분석"]
    
    # 3열 그리드 레이아웃으로 버튼 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for i in range(2):
            if st.button(examples[i], key=f"example_{i}", use_container_width=True):
                st.session_state.user_input = f"{examples[i]}에 대한 프롬프트를 만들어주세요."
                st.session_state.generated_result = None
                st.rerun()
    
    with col2:
        for i in range(2, 4):
            if st.button(examples[i], key=f"example_{i}", use_container_width=True):
                st.session_state.user_input = f"{examples[i]}에 대한 프롬프트를 만들어주세요."
                st.session_state.generated_result = None
                st.rerun()
    
    with col3:
        for i in range(4, 6):
            if st.button(examples[i], key=f"example_{i}", use_container_width=True):
                st.session_state.user_input = f"{examples[i]}에 대한 프롬프트를 만들어주세요."
                st.session_state.generated_result = None
                st.rerun()
    
    # 기능 카드 섹션
    st.markdown("---")
    st.markdown("### 🚀 주요 기능")
    
    feature_cols = st.columns(3)
    
    with feature_cols[0]:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h4 class="feature-title">지능형 의도 분류</h4>
            <p class="feature-description">사용자 입력을 분석하여 정확한 의도를 파악합니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[1]:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <h4 class="feature-title">실시간 프롬프트 생성</h4>
            <p class="feature-description">고품질 AI 프롬프트를 즉시 생성합니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[2]:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔧</span>
            <h4 class="feature-title">템플릿 기반 시스템</h4>
            <p class="feature-description">검증된 템플릿으로 일관된 품질을 보장합니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🚀 PromptOS™ — 특허출원번호: 2025-0094464</p>
        <p>PATENT APPLICATION NO. 2025-0094464 (KIPO)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 특허 문구 하단 삽입
    st.markdown("""
    <p style="text-align: center; font-size: 13px; color: rgba(255,255,255,0.4); margin-top: 40px; font-family: 'Inter', sans-serif; letter-spacing: 0.3px;">
    ⓒ 2025 PromptOS | Patent pending in KR, PCT. All rights reserved.
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 