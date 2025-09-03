# prompt_builder.py

import os
import re
import json
from llm_api import call_llm_openrouter
import streamlit as st
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_template_error(template_key: str, error_type: str, error_message: str, utterance: str = None):
    """
    템플릿 관련 오류를 로그 파일에 기록합니다.
    """
    try:
        # logs 디렉토리 생성
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # 날짜별 로그 파일명
        today = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(logs_dir, f"error_{today}.log")
        
        # 로그 엔트리 생성
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] TEMPLATE_ERROR - Key: '{template_key}' | Type: {error_type} | Error: {error_message}"
        if utterance:
            log_entry += f" | Utterance: '{utterance}'"
        log_entry += "\n"
        
        # 로그 파일에 기록
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
        logger.error(f"템플릿 오류가 로그 파일에 기록되었습니다: {log_file}")
        
    except Exception as e:
        logger.error(f"로그 파일 작성 실패: {e}")

def generate_followup_question(missing_info: str, intent: str = None) -> str:
    """
    누락된 정보에 대한 follow-up 질문을 생성합니다.
    
    Args:
        missing_info (str): 누락된 정보 유형
        intent (str): 의도 (선택사항)
        
    Returns:
        str: follow-up 질문
    """
    followup_questions = {
        "business_item": "Could you tell me what your business item is?",
        "target_audience": "Who is your target audience?",
        "purpose": "What is the main purpose of this document?",
        "tone": "What tone would you prefer? (formal, casual, professional)",
        "length": "How detailed should this be? (brief, comprehensive)",
        "context": "Could you provide more context about your situation?",
        "deadline": "When do you need this completed?",
        "budget": "What is your budget range?",
        "competitors": "Who are your main competitors?",
        "unique_value": "What makes your offering unique?"
    }
    
    return followup_questions.get(missing_info, "Could you provide more details about your request?")

def generate_fallback_prompt(template_key: str, utterance: str = None, intent: str = None) -> str:
    """
    템플릿을 찾지 못했을 때 사용할 fallback 프롬프트를 생성합니다.
    PromptOS 원칙: AI가 사용자에게 적응해야 함
    """
    # 기본값 설정 (시스템 지침에 따라)
    default_tone = "genuine"
    default_tense = "present"
    default_audience = "review panel"
    
    # 의도별 기본 템플릿
    intent_templates = {
        "business_plan": f"""
[Business Plan Generator] 기본 사업계획서 프롬프트

사용자 요청: {utterance or '사업계획서 작성'}
의도: business_plan
톤: {default_tone}
시제: {default_tense}
대상: {default_audience}

지침:
사업계획서를 작성해주세요. 다음 구조를 포함하세요:
1. 사업 개요 및 비전
2. 시장 분석
3. 경쟁사 분석
4. 마케팅 전략
5. 재무 계획
6. 실행 계획

사용자가 "{utterance or '사업계획서 작성'}"을 요청했습니다.
전문적이고 체계적인 사업계획서 프롬프트를 생성해주세요.
""",
        "proposal": f"""
[Proposal Generator] 기본 제안서 프롬프트

사용자 요청: {utterance or '제안서 작성'}
의도: proposal
톤: {default_tone}
시제: {default_tense}
대상: {default_audience}

지침:
제안서를 작성해주세요. 다음 요소를 포함하세요:
1. 제안 개요
2. 문제 정의
3. 해결 방안
4. 기대 효과
5. 예산 및 일정
6. 결론

사용자가 "{utterance or '제안서 작성'}"을 요청했습니다.
설득력 있고 전문적인 제안서 프롬프트를 생성해주세요.
""",
        "default": f"""
[Generic Prompt Generator] 기본 프롬프트

사용자 요청: {utterance or '작업 요청'}
의도: {intent or template_key}
톤: {default_tone}
시제: {default_tense}
대상: {default_audience}

지침:
사용자의 요청에 맞는 전문적이고 효과적인 프롬프트를 생성해주세요.
구체적이고 실행 가능한 지침을 제공하세요.

사용자가 "{utterance or '작업 요청'}"을 요청했습니다.
위 요청에 맞는 최적화된 프롬프트를 생성해주세요.
"""
    }
    
    # 의도에 따른 템플릿 선택
    fallback_content = intent_templates.get(intent, intent_templates["default"])
    
    # 오류 로깅
    log_template_error(template_key, "TEMPLATE_NOT_FOUND", f"Fallback prompt generated for '{template_key}'", utterance)
    
    return fallback_content

TEMPLATE_DIR = "templates"

def extract_placeholders(template: str) -> list:
    return re.findall(r"{(.*?)}", template)

def extract_slots_with_llm(utterance: str, intent: str, placeholders: list) -> dict:
    """
    LLM을 사용하여 사용자 발화에서 슬롯 값을 자동 추출합니다.
    
    Args:
        utterance (str): 사용자 발화
        intent (str): 분류된 의도
        placeholders (list): 템플릿에서 필요한 슬롯 목록
        
    Returns:
        dict: 추출된 슬롯 값들
    """
    if not placeholders:
        return {}
    
    print(f"🔍 LLM 슬롯 추출 시작:")
    print(f"   발화: {utterance}")
    print(f"   의도: {intent}")
    print(f"   필요한 슬롯: {placeholders}")
    
    # Intent별 슬롯 추출 전략 정의
    slot_extraction_strategies = {
        "self_intro": {
            "system_prompt": """당신은 자기소개서 작성에 필요한 정보를 추출하는 전문가입니다.
다음 정보들을 사용자 발화에서 추출해주세요:
- motivation: 지원 동기나 목적
- strengths: 본인의 핵심 역량이나 기술
- experience: 관련된 과거 경험이나 성과
- goals: 향후 목표나 포부

JSON 형태로만 응답하세요. 추출할 수 없는 정보는 null로 설정하세요.""",
            "slots": ["motivation", "strengths", "experience", "goals"]
        },
        "customer_reply": {
            "system_prompt": """당신은 고객 응대 상황을 분석하는 전문가입니다.
다음 정보들을 사용자 발화에서 추출해주세요:
- situation: 고객 불만이나 문제 상황
- tone: 응대 톤 (정중, 친근, 공식적 등)
- urgency: 긴급도 (높음, 보통, 낮음)

JSON 형태로만 응답하세요. 추출할 수 없는 정보는 null로 설정하세요.""",
            "slots": ["situation", "tone", "urgency"]
        },
        "summary": {
            "system_prompt": """당신은 요약 작업에 필요한 정보를 추출하는 전문가입니다.
다음 정보들을 사용자 발화에서 추출해주세요:
- content: 요약할 대상 내용 (문장 그대로)
- tone: 요약 톤 (간결, 상세, 전문적 등)
- audience: 대상 청중

JSON 형태로만 응답하세요. 추출할 수 없는 정보는 null로 설정하세요.""",
            "slots": ["content", "tone", "audience"]
        },
        "proposal": {
            "system_prompt": """당신은 제안서 작성에 필요한 정보를 추출하는 전문가입니다.
다음 정보들을 사용자 발화에서 추출해주세요:
- proposal_field: 제안 분야나 주제
- core_technology: 핵심 기술이나 솔루션
- application_area: 적용 분야나 대상
- expected_effect: 기대 효과나 성과
- investment_scale: 투자 규모나 예산

JSON 형태로만 응답하세요. 추출할 수 없는 정보는 null로 설정하세요.""",
            "slots": ["proposal_field", "core_technology", "application_area", "expected_effect", "investment_scale"]
        }
    }
    
    # 기본 전략 (일반적인 슬롯 추출)
    default_strategy = {
        "system_prompt": f"""당신은 사용자 발화에서 필요한 정보를 추출하는 전문가입니다.
다음 슬롯들을 사용자 발화에서 추출해주세요: {', '.join(placeholders)}

JSON 형태로만 응답하세요. 추출할 수 없는 정보는 null로 설정하세요.""",
        "slots": placeholders
    }
    
    # Intent별 전략 선택
    strategy = slot_extraction_strategies.get(intent, default_strategy)
    
    # LLM 프롬프트 구성
    system_message = strategy["system_prompt"]
    user_message = f"사용자 발화: {utterance}\n\n위 발화에서 필요한 정보를 추출해주세요."
    
    full_prompt = f"{system_message}\n\n{user_message}"
    
    try:
        # LLM 호출
        response = call_llm_openrouter(full_prompt)
        print(f"   LLM 응답: {response[:200]}...")
        
        # JSON 파싱 시도
        try:
            # 마크다운 코드 블록 제거
            cleaned_response = response.strip()
            if cleaned_response.startswith('```'):
                lines = cleaned_response.split('\n')
                cleaned_response = '\n'.join(lines[1:-1]) if len(lines) > 2 else cleaned_response
            
            extracted_slots = json.loads(cleaned_response)
            print(f"   JSON 파싱 성공: {extracted_slots}")
            
            # 템플릿에 필요한 슬롯만 필터링
            result = {}
            for slot in placeholders:
                if slot in extracted_slots and extracted_slots[slot] is not None:
                    result[slot] = extracted_slots[slot]
                    print(f"   ✅ {slot}: {extracted_slots[slot]}")
                else:
                    print(f"   ❌ {slot}: 추출 실패")
            
            print(f"   최종 추출 결과: {len(result)}개 슬롯")
            return result
            
        except json.JSONDecodeError:
            print(f"⚠️ LLM 응답을 JSON으로 파싱할 수 없습니다: {response}")
            # 간단한 키워드 기반 추출 시도
            return _extract_slots_by_keywords(utterance, placeholders)
            
    except Exception as e:
        print(f"❌ 슬롯 추출 중 오류 발생: {e}")
        # 간단한 키워드 기반 추출 시도
        return _extract_slots_by_keywords(utterance, placeholders)

def _extract_slots_by_keywords(utterance: str, placeholders: list) -> dict:
    """
    키워드 기반으로 간단한 슬롯 추출을 시도합니다.
    """
    print(f"🔍 키워드 기반 슬롯 추출 시도...")
    result = {}
    
    # 간단한 키워드 매핑
    keyword_mapping = {
        "proposal_field": ["제안", "분야", "주제", "사업", "기술"],
        "core_technology": ["기술", "솔루션", "시스템", "플랫폼", "AI", "인공지능"],
        "application_area": ["적용", "분야", "대상", "시장", "고객"],
        "expected_effect": ["효과", "성과", "결과", "기대", "목표"],
        "investment_scale": ["투자", "예산", "규모", "금액", "비용"],
        "motivation": ["동기", "목적", "이유", "원인"],
        "strengths": ["강점", "역량", "기술", "능력", "장점"],
        "experience": ["경험", "실적", "성과", "과거"],
        "goals": ["목표", "포부", "계획", "미래"],
        "situation": ["상황", "문제", "불만", "이슈"],
        "urgency": ["긴급", "시급", "중요", "우선순위"]
    }
    
    for placeholder in placeholders:
        if placeholder in keyword_mapping:
            keywords = keyword_mapping[placeholder]
            for keyword in keywords:
                if keyword in utterance:
                    # 키워드 주변 텍스트 추출
                    start_idx = utterance.find(keyword)
                    end_idx = min(start_idx + len(keyword) + 20, len(utterance))
                    extracted_text = utterance[start_idx:end_idx].strip()
                    result[placeholder] = extracted_text
                    print(f"   ✅ 키워드 기반 {placeholder}: {extracted_text}")
                    break
    
    return result

def prompt_missing_values(placeholders: list, utterance: str = "", intent: str = "") -> dict:
    """
    누락된 슬롯 값을 처리합니다. LLM 자동 추출을 먼저 시도하고, 
    실패 시 사용자 입력을 받습니다.
    """
    values = {}
    
    # LLM 자동 추출 시도 (utterance와 intent가 제공된 경우)
    if utterance and intent:
        extracted_values = extract_slots_with_llm(utterance, intent, placeholders)
        values.update(extracted_values)
        
        # 추출된 슬롯 제거
        remaining_placeholders = [ph for ph in placeholders if ph not in values]
        
        if remaining_placeholders:
            print(f"🤖 LLM이 자동으로 추출한 값: {extracted_values}")
            print(f"💬 추가 입력이 필요한 항목: {', '.join(remaining_placeholders)}")
            
            # 남은 슬롯은 사용자 입력 받기
            for ph in remaining_placeholders:
                user_input = input(f"💬 '{ph}' 값을 입력해주세요: ").strip()
                values[ph] = user_input
    else:
        # 기존 방식: 모든 슬롯을 사용자 입력으로 받기
        for ph in placeholders:
            user_input = input(f"💬 '{ph}' 값을 입력해주세요: ").strip()
            values[ph] = user_input
    
    return values

def fill_template(template: str, values: dict) -> str:
    """
    템플릿을 값으로 채웁니다. 누락된 값은 'N/A'로 대체합니다.
    
    Args:
        template: 템플릿 문자열
        values: 채울 값들의 딕셔너리
        
    Returns:
        str: 채워진 템플릿
    """
    try:
        # 디버깅: 입력값 확인
        print(f"🔍 fill_template 디버깅:")
        print(f"   템플릿 길이: {len(template)}")
        print(f"   값 개수: {len(values)}")
        print(f"   값들: {list(values.keys())}")
        
        # 누락된 플레이스홀더를 'N/A'로 대체
        safe_values = {}
        placeholders = extract_placeholders(template)
        
        print(f"   발견된 플레이스홀더: {placeholders}")
        
        for placeholder in placeholders:
            if placeholder in values and values[placeholder]:
                safe_values[placeholder] = values[placeholder]
                print(f"   ✅ {placeholder}: {values[placeholder]}")
            else:
                safe_values[placeholder] = "N/A"
                print(f"   ❌ {placeholder}: N/A (값 없음)")
        
        # 템플릿 채우기
        filled_template = template.format(**safe_values)
        
        # 결과 검증
        if not filled_template or filled_template.strip() == "":
            print(f"⚠️ 경고: 채워진 템플릿이 비어있습니다!")
            return _generate_fallback_prompt(values)
        
        print(f"   ✅ 템플릿 채우기 완료: 길이 {len(filled_template)}")
        return filled_template
        
    except Exception as e:
        print(f"❌ 템플릿 채우기 중 오류 발생: {e}")
        return _generate_fallback_prompt(values)

def _generate_fallback_prompt(values: dict) -> str:
    """
    템플릿 채우기 실패 시 안전한 fallback 프롬프트를 생성합니다.
    """
    return f"""
다음 요청에 맞는 프롬프트를 생성해주세요:

사용자 요청: {values.get('user_utterance', 'N/A')}
의도: {values.get('intent', 'N/A')}
도메인: {values.get('domain', 'N/A')}
톤: {values.get('tone', 'N/A')}
대상: {values.get('audience', 'N/A')}

위 정보를 바탕으로 명령형 문장으로 시작하고, 목적과 결과가 분명히 드러나게 구성해주세요.
"""

def get_template(template_key: str, base_dir="templates", fallback="unknown", utterance: str = None) -> str:
    """
    템플릿 키 기반으로 다단계 탐색
    예: "proposal_ai_government" → templates/proposal/ai/government.txt
        "self_intro" → templates/self_intro.txt
    """
    logger = logging.getLogger(__name__)

    # 1. 직접 매핑 시도 (templates/template_key.txt)
    direct_path = os.path.join(base_dir, f"{template_key}.txt")
    if os.path.isfile(direct_path):
        logger.info(f"✅ 직접 매핑 성공: {direct_path}")
        with open(direct_path, encoding="utf-8") as f:
            return f.read()

    # 2. 하위 폴더 매핑 시도 (templates/proposal/ai/government.txt 등)
    nested_path = os.path.join(base_dir, *template_key.split("_")) + ".txt"
    if os.path.isfile(nested_path):
        logger.info(f"✅ 하위 폴더 매핑 성공: {nested_path}")
        with open(nested_path, encoding="utf-8") as f:
            return f.read()

    # 3. intent별 하위 폴더에서 템플릿 찾기
    intent_dir = os.path.join(base_dir, template_key)
    if os.path.exists(intent_dir) and os.path.isdir(intent_dir):
        # 첫 번째 템플릿 파일 찾기
        for file in os.listdir(intent_dir):
            if file.endswith('.txt'):
                template_path = os.path.join(intent_dir, file)
                logger.info(f"✅ intent 폴더에서 템플릿 발견: {template_path}")
                with open(template_path, encoding="utf-8") as f:
                    return f.read()

    # 4. fallback 템플릿 사용
    fallback_path = os.path.join(base_dir, f"{fallback}.txt")
    if os.path.isfile(fallback_path):
        logger.warning(f"⚠️ [템플릿 없음] '{template_key}' 관련 템플릿을 찾지 못해 fallback({fallback})을 반환합니다.")
        log_template_error(template_key, "FALLBACK_USED", f"Using fallback template: {fallback}", utterance)
        st.error(f"❗ '{template_key}' 관련 템플릿을 찾지 못해 기본 템플릿({fallback})을 사용합니다.")
        with open(fallback_path, encoding="utf-8") as f:
            return f.read()

    # 5. 완전 실패: generate_fallback_prompt() 사용
    logger.error(f"❌ [템플릿 없음] '{template_key}' 관련 템플릿과 fallback 템플릿 모두 찾지 못했습니다.")
    log_template_error(template_key, "COMPLETE_FAILURE", "No template or fallback found", utterance)
    
    # fallback 프롬프트 생성
    fallback_prompt = generate_fallback_prompt(template_key, utterance, template_key)
    
    st.error(f"❌ '{template_key}' 관련 템플릿을 찾지 못했습니다. AI가 직접 프롬프트를 생성합니다.")
    return fallback_prompt
