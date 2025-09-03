#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
app.py 로직 테스트 스크립트
"""

import logging
from intent_classifier import classify_intent
from prompt_generator import extract_conditions
from template_loader import get_template
from prompt_builder import extract_placeholders, fill_template

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_app_logic():
    """app.py의 메인 로직을 테스트합니다."""
    
    print("🔍 app.py 로직 테스트 시작\n")
    
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
            logger.info("의도 분류 시작...")
            parsed = classify_intent(utterance)
            logger.info(f"의도 분류 결과: {parsed}")
            print(f"✅ 의도 분류: {parsed}")
            
            if not isinstance(parsed, dict):
                print("❌ 의도 분류 실패: dict가 아님")
                continue
            
            # 2. Intent 구성
            intent = parsed.get("intent", "unknown")
            sub_intent = parsed.get("sub_intent")
            domain = parsed.get("domain", "general")
            audience = parsed.get("audience", "general")
            
            if intent == "unknown":
                print("❌ 의도 분류 실패: unknown")
                continue
            print(f"✅ Intent 구성: {intent}, {sub_intent}, {domain}")
            
            # 3. 조건 추출
            conditions = extract_conditions(utterance)
            tone = conditions.get("tone", "중립적")
            tense = conditions.get("tense", "현재시제")
            audience = conditions.get("audience", "일반")
            print(f"✅ 조건 추출: {tone}, {tense}, {audience}")
            
            # 4. 템플릿 키 생성
            template_key = intent
            if sub_intent:
                template_key = f"{intent}_{sub_intent}"
            print(f"✅ 템플릿 키: {template_key}")
            
            # 5. 템플릿 로딩
            logger.info(f"템플릿 로딩 시작: {template_key}")
            template_text = get_template(template_key, utterance=utterance)
            logger.info(f"템플릿 로딩 결과: 길이={len(template_text) if template_text else 0}")
            
            if not template_text:
                print("❌ 템플릿 로딩 실패")
                continue
            
            print(f"✅ 템플릿 로딩: 길이 {len(template_text)} 문자")
            
            # 6. 플레이스홀더 추출
            logger.info("플레이스홀더 추출 시작...")
            placeholders = extract_placeholders(template_text)
            logger.info(f"플레이스홀더 추출 결과: {len(placeholders)}개")
            print(f"✅ 플레이스홀더 추출: {len(placeholders)}개")
            
            # 7. 값 구성
            values = {
                "user_utterance": utterance,
                "intent": intent,
                "sub_intent": sub_intent,
                "domain": domain,
                "tone": tone,
                "tense": tense,
                "audience": audience,
            }
            
            # 7-1. LLM 슬롯 추출 시도
            try:
                from prompt_builder import extract_slots_with_llm
                print("🔍 LLM 슬롯 추출 시도...")
                extracted_slots = extract_slots_with_llm(utterance, intent, placeholders)
                
                if extracted_slots:
                    print(f"✅ LLM 슬롯 추출 성공: {len(extracted_slots)}개")
                    values.update(extracted_slots)
                else:
                    print("⚠️ LLM 슬롯 추출 실패")
                    
            except Exception as e:
                print(f"❌ LLM 슬롯 추출 오류: {e}")
            
            # 누락된 플레이스홀더에 기본값 추가
            for placeholder in placeholders:
                if placeholder not in values:
                    values[placeholder] = "N/A"
            
            print(f"✅ 값 구성: {len(values)}개")
            
            # 8. 최종 프롬프트 생성
            logger.info("최종 프롬프트 생성 시작...")
            all_filled = all(values.get(k) for k in placeholders) if placeholders else True
            logger.info(f"플레이스홀더 채움 상태: {all_filled}")
            
            if all_filled:
                final_prompt = fill_template(template_text, values)
                logger.info(f"최종 프롬프트 생성 완료: 길이={len(final_prompt)}")
                
                if final_prompt and len(final_prompt.strip()) > 10:
                    print(f"✅ 최종 프롬프트 생성: 길이 {len(final_prompt)} 문자")
                    print(f"📄 프롬프트 미리보기: {final_prompt[:100]}...")
                else:
                    print("❌ 최종 프롬프트 생성 실패 (너무 짧거나 비어있음)")
            else:
                print("❌ 플레이스홀더가 모두 채워지지 않음")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            print(f"📋 상세 오류: {traceback.format_exc()}")
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    test_app_logic() 