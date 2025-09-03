import streamlit as st
from intent_classifier import classify_intent
from prompt_generator import extract_conditions, generate_prompt
from prompt_builder import get_template, extract_placeholders, prompt_missing_values, fill_template
from fallback_manager import fallback_manager

def create_copy_js(text_to_copy):
    """복사 기능을 위한 JavaScript 생성"""
    return f"""
    <script>
    function copyToClipboard() {{
        const text = `{text_to_copy}`;
        navigator.clipboard.writeText(text).then(function() {{
            // 복사 성공 시 버튼 텍스트 변경
            const btn = document.querySelector('.copy-btn');
            if (btn) {{
                const originalText = btn.innerHTML;
                btn.innerHTML = '✅ 복사됨!';
                setTimeout(() => {{
                    btn.innerHTML = originalText;
                }}, 2000);
            }}
        }}).catch(function(err) {{
            console.error('복사 실패:', err);
        }});
    }}
    </script>
    """

def main():
    st.set_page_config(page_title="PromptOS - 프롬프트 생성기", layout="wide")
    st.title("💡 PromptOS 자동 생성기")
    st.write("자연어 한 줄 → 고품질 프롬프트 완성")

    # 사용자 입력
    st.markdown("### 🧠 자연어로 원하는 작업을 설명해주세요")
    utterance = st.text_input("입력", placeholder="예: 광고 스크립트 작성", label_visibility="collapsed")

    if st.button("프롬프트 생성하기"):
        if not utterance.strip():
            st.warning("⚠️ 작업 내용을 입력해주세요.")
            return

        # 1. 의도 분류
        parsed = classify_intent(utterance)
        intent = parsed.get("intent") or "unknown"
        sub_intent = parsed.get("sub_intent")
        domain = parsed.get("domain")

        # 2. 조건 추출
        conditions = extract_conditions(utterance)
        tone = conditions.get("tone") or "중립적"
        tense = conditions.get("tense") or "현재시제"
        audience = conditions.get("audience") or "정부 관계자"
        
        # 3. 분석 결과 표시 (카드 형태)
        st.markdown("### 🔍 분석 결과")
        
        # 메트릭 카드들
        metric_cols = st.columns(3)
        
        # intent가 unknown인지 확인
        is_unknown_intent = intent == "unknown"
        
        metrics = [
            {"icon": "🎯", "label": "분류된 의도", "value": intent, "col": 0, "is_unknown": is_unknown_intent},
            {"icon": "🎨", "label": "감지된 톤", "value": tone, "col": 1, "is_unknown": False},
            {"icon": "👥", "label": "대상 청중", "value": audience, "col": 2, "is_unknown": False}
        ]
        
        for metric in metrics:
            with metric_cols[metric["col"]]:
                # unknown intent인 경우 배지 추가
                badge_html = ""
                if metric["is_unknown"]:
                    badge_html = """
                    <div style="position: absolute; top: -8px; right: -8px; background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; z-index: 10;">
                        🤖 AI 생성
                    </div>
                    """
                
                st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 8px 0; background-color: #f8f9fa; position: relative;">
                    {badge_html}
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 8px;">{metric['icon']}</div>
                        <div style="font-weight: bold; color: #333; margin-bottom: 4px;">{metric['label']}</div>
                        <div style="color: #666; font-size: 0.9rem;">{metric['value']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 4. 템플릿 키 조합
        template_key = intent
        if sub_intent:
            template_key += f"_{sub_intent}"
        if domain:
            template_key += f"_{domain}"
        
        # unknown intent인 경우 다른 스타일 적용
        if is_unknown_intent:
            st.markdown(f"""
            <div style="border: 1px solid #ffc107; border-radius: 8px; padding: 16px; margin: 16px 0; background-color: #fff3cd;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem; margin-right: 8px;">🤖</span>
                    <strong>AI가 직접 생성한 결과입니다</strong>
                </div>
                <div style="color: #856404;">
                    <code>{template_key}</code> 템플릿을 찾을 수 없어 LLM이 직접 프롬프트를 생성합니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="border: 1px solid #28a745; border-radius: 8px; padding: 16px; margin: 16px 0; background-color: #d4edda;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.2rem; margin-right: 8px;">🔑</span>
                    <strong>선택된 템플릿:</strong> <code>{template_key}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 5. 템플릿 불러오기
        template_text = get_template(template_key, utterance=utterance)
        if not template_text:
            st.warning("⚠️ 템플릿을 찾을 수 없습니다. LLM에게 직접 프롬프트 생성을 요청합니다...")
            
            with st.spinner("🤖 LLM이 프롬프트를 생성하고 있습니다..."):
                final_prompt = fallback_manager.generate_prompt_with_llm(utterance, intent)
            
            st.success("✅ LLM이 프롬프트를 생성했습니다.")
            
            # 프롬프트 결과 카드 (복사 버튼 포함)
            escaped_prompt = final_prompt.replace('`', '\\`').replace('${', '\\${')
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 16px 0; background-color: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: bold; color: #333;">📝 LLM 생성 프롬프트</span>
                    <button class="copy-btn" onclick="copyToClipboard()" style="background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">📋 복사하기</button>
                </div>
                <div style="background: white; padding: 12px; border-radius: 4px; border: 1px solid #ddd; font-family: monospace; white-space: pre-wrap; max-height: 400px; overflow-y: auto;">{escaped_prompt}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript for clipboard copy
            st.markdown(create_copy_js(final_prompt.replace("'", "\\'")), unsafe_allow_html=True)
            return

        # 6. 누락된 값 입력
        placeholders = extract_placeholders(template_text)
        values = {
            "user_utterance": utterance,
            "intent": intent,
            "sub_intent": sub_intent,
            "domain": domain,
            "tone": tone,
            "tense": tense,
            "audience": audience,
        }

        missing_keys = [ph for ph in placeholders if ph not in values or not values[ph]]
        if missing_keys:
            st.info(f"⚠️ 누락된 값: {', '.join(missing_keys)}")
            user_inputs = prompt_missing_values(missing_keys, utterance, intent)
            values.update(user_inputs)

        # 7. 프롬프트 완성
        final_prompt = fill_template(template_text, values)

        # 8. 결과 출력
        # 프롬프트 결과 카드 (복사 버튼 포함)
        escaped_prompt = final_prompt.replace('`', '\\`').replace('${', '\\${')
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 16px 0; background-color: #f8f9fa;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-weight: bold; color: #333;">📝 생성된 프롬프트</span>
                <button class="copy-btn" onclick="copyToClipboard()" style="background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">📋 복사하기</button>
            </div>
            <div style="background: white; padding: 12px; border-radius: 4px; border: 1px solid #ddd; font-family: monospace; white-space: pre-wrap; max-height: 400px; overflow-y: auto;">{escaped_prompt}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # JavaScript for clipboard copy
        st.markdown(create_copy_js(final_prompt.replace("'", "\\'")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
