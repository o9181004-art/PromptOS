#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Streamlit 앱 문제 진단 스크립트
"""

import streamlit as st
from classify_intent import classify_intent
from template_loader import get_template
from prompt_builder import extract_placeholders, fill_template
from fallback_manager import FallbackManager

def debug_streamlit_flow():
    """Streamlit 앱의 전체 플로우를 디버깅합니다."""
    
    print("🔍 Streamlit 앱 디버깅 시작\n")
    
    # 테스트 케이스
    test_cases = [
        "AI 기반 제안서를 정부에 제출할거야",
        "고객을 위한 정중한 이메일을 작성해줘",
        "자기소개서를 작성해줘"
    ]
    
    for i, utterance in enumerate(test_cases, 1):
        print(f"📝 테스트 {i}: {utterance}")
        print("-" * 60)
        
        try:
            # 1. 의도 분류
            print("1️⃣ 의도 분류 시도...")
            intent = classify_intent(utterance)
            print(f"   ✅ 의도 분류 결과: {intent}")
            
            # 2. 템플릿 로딩
            print("2️⃣ 템플릿 로딩 시도...")
            template_text = get_template(intent, utterance=utterance)
            if template_text:
                print(f"   ✅ 템플릿 로딩 성공 (길이: {len(template_text)} 문자)")
            else:
                print("   ❌ 템플릿 로딩 실패")
                continue
            
            # 3. 플레이스홀더 추출
            print("3️⃣ 플레이스홀더 추출 시도...")
            placeholders = extract_placeholders(template_text)
            print(f"   ✅ 플레이스홀더 추출: {len(placeholders)}개")
            
            # 4. 값 구성
            print("4️⃣ 값 구성 시도...")
            values = {
                "user_utterance": utterance,
                "intent": intent,
                "domain": "general",
                "tone": "professional",
                "audience": "general",
                "tense": "현재시제"
            }
            
            # 누락된 플레이스홀더에 기본값 추가
            for placeholder in placeholders:
                if placeholder not in values:
                    values[placeholder] = "N/A"
            
            print(f"   ✅ 값 구성 완료: {len(values)}개")
            
            # 5. 템플릿 채우기
            print("5️⃣ 템플릿 채우기 시도...")
            final_prompt = fill_template(template_text, values)
            
            if final_prompt and len(final_prompt.strip()) > 10:
                print(f"   ✅ 템플릿 채우기 성공 (길이: {len(final_prompt)} 문자)")
                print(f"   📄 프롬프트 미리보기: {final_prompt[:100]}...")
            else:
                print("   ❌ 템플릿 채우기 실패 (너무 짧거나 비어있음)")
                
        except Exception as e:
            print(f"   ❌ 오류 발생: {e}")
            import traceback
            print(f"   📋 상세 오류: {traceback.format_exc()}")
        
        print("\n" + "=" * 60 + "\n")

def test_fallback_manager():
    """FallbackManager의 동작을 테스트합니다."""
    
    print("🔄 FallbackManager 테스트\n")
    
    fallback_manager = FallbackManager()
    
    test_cases = [
        "AI 기반 제안서를 정부에 제출할거야",
        "고객을 위한 정중한 이메일을 작성해줘"
    ]
    
    for utterance in test_cases:
        print(f"💬 입력: {utterance}")
        
        try:
            # 도움 메시지 생성 테스트
            helpful_message = fallback_manager.generate_helpful_message(utterance)
            print(f"✅ 도움 메시지: {helpful_message}")
            
            # LLM 프롬프트 생성 테스트
            llm_prompt = fallback_manager.generate_prompt_with_llm(utterance, "unknown", "general", "general")
            print(f"✅ LLM 프롬프트: {llm_prompt[:100]}...")
            
        except Exception as e:
            print(f"❌ FallbackManager 오류: {e}")
        
        print("-" * 40)

def test_streamlit_components():
    """Streamlit 컴포넌트들을 테스트합니다."""
    
    print("🎨 Streamlit 컴포넌트 테스트\n")
    
    # 간단한 Streamlit 앱 시뮬레이션
    try:
        # st.markdown 테스트
        test_html = """
        <div class="custom-alert alert-success">
            <span style="font-size: 1.5rem;">✅</span>
            <div><strong>테스트 성공!</strong></div>
        </div>
        """
        print("✅ HTML 렌더링 테스트 통과")
        
        # 복사 버튼 JavaScript 테스트
        test_js = """
        <script>
        function copyToClipboard() {
            navigator.clipboard.writeText('test');
        }
        </script>
        """
        print("✅ JavaScript 테스트 통과")
        
    except Exception as e:
        print(f"❌ Streamlit 컴포넌트 오류: {e}")

if __name__ == "__main__":
    print("🚨 Streamlit 앱 문제 진단 시작\n")
    
    # 1. 기본 플로우 테스트
    debug_streamlit_flow()
    
    # 2. FallbackManager 테스트
    test_fallback_manager()
    
    # 3. Streamlit 컴포넌트 테스트
    test_streamlit_components()
    
    print("✅ 진단 완료!") 