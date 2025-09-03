import streamlit as st
import streamlit.components.v1 as components
import os

def load_html_file(file_path):
    """HTML 파일을 읽어서 반환합니다."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    st.set_page_config(
        page_title="PromptOS - AI Prompt Platform",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS 스타일 제거 (HTML에서 처리)
    st.markdown("""
        <style>
        .main > div {
            padding-top: 0;
        }
        .stApp {
            background: transparent;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    # HTML 파일 경로
    html_file_path = "static/index.html"
    
    # HTML 파일이 존재하는지 확인
    if os.path.exists(html_file_path):
        # HTML 파일 읽기
        html_content = load_html_file(html_file_path)
        
        # HTML을 Streamlit에 렌더링
        components.html(
            html_content,
            height=800,
            scrolling=True
        )
    else:
        st.error(f"HTML 파일을 찾을 수 없습니다: {html_file_path}")
        st.info("static/index.html 파일이 프로젝트 루트에 있는지 확인해주세요.")

if __name__ == "__main__":
    main() 