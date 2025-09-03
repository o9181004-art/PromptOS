# ✅ Purpose-Driven Prompt Template System
# This file defines all intent-specific prompt templates with strict mapping.
# Explicit intents follow fixed structures; implicit intents require inference + follow-up handling.

TEMPLATES_BY_INTENT = {
    "summary": {
        "title": "전문적 요약문 생성 템플릿",
        "description": "사용자의 요청을 요약하는 템플릿입니다. 핵심 내용, 논리 구조, 중요도 기반으로 구성됨.",
        "template": "다음 기준에 따라 요약해주세요:\n\n- 핵심 내용 추출\n- 논리적 구조 유지\n- 명확하고 간결한 표현\n- 중요도에 따른 우선순위\n\n전문적이고 객관적인 요약문을 작성해주세요.",
        "output_language": "ko"
    },
    "ir_draft": {
        "title": "투자자용 IR 문서 초안 생성 템플릿",
        "description": "투자자 대상 IR 초안을 생성하는 템플릿입니다.",
        "template": "다음 기준에 따라 IR 문서를 작성해주세요:\n\n1. 회사 개요 및 비전\n2. 핵심 제품/서비스 설명\n3. 시장 규모 및 성장 가능성\n4. 수익모델 및 비즈니스 전략\n5. 투자 제안 내용\n6. 기대 수익 및 Exit 전략\n\n투자자의 신뢰를 얻을 수 있는 전문적이고 간결한 형식으로 작성해주세요.",
        "output_language": "ko"
    },
    "customer_reply": {
        "title": "고객 응대 템플릿",
        "description": "공감과 실용성을 바탕으로 한 고객 응대용 템플릿입니다.",
        "template": "다음 원칙에 따라 고객 문의에 응답해주세요:\n\n- 공감과 이해를 바탕으로 한 답변\n- 구체적이고 실용적인 해결책 제시\n- 정중하고 친근한 톤 유지\n- 추가 문의에 대한 개방적 태도\n\n고객의 만족도를 높일 수 있는 전문적인 응대문을 작성해주세요.",
        "output_language": "ko"
    },
    "collab_email": {
        "title": "협업 제안 이메일 템플릿",
        "description": "아이디어 협업을 위한 이메일 작성 템플릿입니다.",
        "template": "다음 이메일 구조에 따라 작성해주세요:\n\n1. 인사말\n2. 협업 제안 배경\n3. 구체적인 협업 방안\n4. 기대 효과\n5. 다음 단계 제안\n6. 마무리 인사\n\n정중하고 설득력 있는 톤을 유지해주세요.",
        "output_language": "ko"
    },
    "biz_plan": {
        "title": "사업계획서 구성 템플릿",
        "description": "아이디어 또는 예비창업자의 발화를 기반으로 한 사업계획서 자동 생성 템플릿입니다.",
        "template": "다음 기준에 따라 사업계획서를 작성해주세요:\n\n📌 사업 개요\n- 비즈니스 모델과 핵심 가치 제안\n- 사업의 목적과 비전\n\n📊 시장 분석\n- 시장 현황과 규모\n- 경쟁사 분석과 차별화 포인트\n\n🍽️ 서비스 설명\n- 핵심 제품/서비스 상세 설명\n- 고객 가치와 혜택\n\n📈 실행 계획\n- 단계별 실행 전략\n- 자원 및 예산 계획\n\n🎯 기대 효과\n- 예상 성과 및 지표\n- 사회적/경제적 기여도\n\n전문적이고 격식 있는 보고서 형식으로 작성해주세요.",
        "output_language": "ko"
    },
    "marketing_copy": {
        "title": "마케팅 카피 생성 템플릿",
        "description": "감성적이고 설득력 있는 마케팅 카피를 생성하는 템플릿입니다.",
        "template": "다음 기준에 따라 마케팅 카피를 작성해주세요:\n\n🎯 핵심 메시지\n- 제품/서비스의 핵심 가치\n- 고객이 얻을 수 있는 혜택\n\n💡 감성적 어필\n- 고객의 니즈와 감정에 호소\n- 공감할 수 있는 스토리텔링\n\n✨ 차별화 포인트\n- 경쟁사 대비 우위\n- 독특한 특징과 장점\n\n🚀 행동 유도\n- 명확한 CTA (Call-to-Action)\n- 즉시 행동할 수 있는 동기 부여\n\n감성적이고 설득력 있는 마케팅 카피를 작성해주세요.",
        "output_language": "ko"
    },
    "self_intro": {
        "title": "자기소개서 작성 템플릿",
        "description": "자신감 있고 진정성 있는 자기소개서를 작성하는 템플릿입니다.",
        "template": "다음 기준에 따라 자기소개서를 작성해주세요:\n\n👤 개인적 배경\n- 성장 과정과 가치관\n- 개인적 특성과 강점\n\n🎓 학력 및 경험\n- 교육 배경과 주요 성과\n- 관련 경험과 스킬\n\n💼 직무 적합성\n- 지원 직무와의 연관성\n- 해당 분야에 대한 열정과 준비도\n\n🎯 미래 계획\n- 직무 목표와 비전\n- 조직 기여 방안\n\n자신감 있고 진정성 있는 자기소개서를 작성해주세요.",
        "output_language": "ko"
    },
    "proposal": {
        "title": "제안서 작성 템플릿",
        "description": "전문적이고 체계적인 제안서를 작성하는 템플릿입니다.",
        "template": "다음 기준에 따라 제안서를 작성해주세요:\n\n📋 제안 개요\n- 제안 배경과 목적\n- 핵심 제안 사항\n\n📊 현황 분석\n- 현재 상황과 문제점\n- 개선의 필요성\n\n💡 제안 내용\n- 구체적인 해결 방안\n- 기대 효과와 혜택\n\n📈 실행 계획\n- 단계별 실행 방안\n- 일정 및 자원 계획\n\n💰 예산 및 투자\n- 필요한 예산과 투자\n- ROI 및 성과 지표\n\n전문적이고 체계적인 제안서를 작성해주세요.",
        "output_language": "ko"
    },
    "meeting_summary": {
        "title": "회의 요약서 작성 템플릿",
        "description": "객관적이고 요약적인 회의 요약서를 작성하는 템플릿입니다.",
        "template": "다음 기준에 따라 회의 요약서를 작성해주세요:\n\n📅 회의 정보\n- 일시, 장소, 참석자\n- 회의 주제와 목적\n\n📝 주요 논의 사항\n- 핵심 안건과 토론 내용\n- 주요 의견과 제안\n\n✅ 결정 사항\n- 확정된 사항과 결론\n- 다음 단계와 액션 아이템\n\n📋 후속 조치\n- 담당자와 일정\n- 추진 계획과 마감일\n\n객관적이고 요약적인 회의 요약서를 작성해주세요.",
        "output_language": "ko"
    },
    "code_run": {
        "title": "코드 실행 및 분석 템플릿",
        "description": "코드 실행과 분석을 위한 전문적인 템플릿입니다.",
        "template": "다음 기준에 따라 코드를 분석하고 실행해주세요:\n\n🔍 코드 분석\n- 코드 구조와 로직 파악\n- 잠재적 문제점 식별\n\n⚙️ 실행 환경\n- 필요한 라이브러리와 의존성\n- 실행 환경 설정\n\n🚀 실행 결과\n- 코드 실행 결과\n- 오류 발생 시 해결 방안\n\n📊 성능 분석\n- 실행 시간과 메모리 사용량\n- 최적화 방안 제시\n\n전문적이고 정확한 코드 분석과 실행을 수행해주세요.",
        "output_language": "ko"
    }
    # ✅ 모든 명시적 intent는 위처럼 추가 가능. 이후 자동으로 분류됨.
}

# Implicit case 처리용 LLM fallback 기본 지시문
IMPLICIT_PURPOSE_FALLBACK = {
    "instruction": "사용자의 발화는 다음과 같습니다: '{user_input}'\n\n이전 대화 흐름 및 문맥을 고려하여 사용자의 목적을 추론하세요. 추론된 목적에 따라 가장 적절한 구조와 톤으로 응답을 생성하십시오.\n\n목적이 명확하지 않은 경우, 추가 정보를 요청할 수 있는 친근하고 정중한 문장으로 안내하세요.",
    "output_language": "ko"
}

# 신뢰도 임계값 설정
CONFIDENCE_THRESHOLDS = {
    "high_confidence": 0.6,
    "medium_confidence": 0.4,
    "low_confidence": 0.3,
    "fallback_threshold": 0.2
}

# 템플릿 우선순위 설정
TEMPLATE_PRIORITY = {
    "explicit_intent": 1.0,
    "keyword_matching": 0.9,
    "similarity_matching": 0.8,
    "llm_inference": 0.7,
    "fallback": 0.5
}

# 출력 언어 설정
SUPPORTED_LANGUAGES = {
    "ko": "한국어",
    "en": "English",
    "ja": "日本語",
    "zh": "中文"
}

# 기본 설정
DEFAULT_CONFIG = {
    "output_language": "ko",
    "max_response_length": 2000,
    "include_examples": True,
    "enable_followup_questions": True
} 