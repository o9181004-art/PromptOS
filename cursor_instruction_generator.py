# cursor_instruction_generator.py

"""
This script dynamically determines the user's purpose (explicit or inferred),
and assigns a predefined template structure accordingly.

If the purpose is unclear, it triggers a user clarification prompt
before proceeding with answer generation.

Instructions are returned in Prompt Instruction Format.
"""

import logging
from typing import Dict, List, Optional, Any

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_instruction(user_utterance: str) -> Dict[str, Any]:
    """
    사용자 발화를 분석하여 적절한 지시사항을 생성합니다.
    
    Args:
        user_utterance: 사용자 입력
        
    Returns:
        Dict[str, Any]: 생성된 지시사항과 메타데이터
    """
    logger.info(f"🔍 지시사항 생성 시작: {user_utterance}")
    
    # STEP 1: Explicit Purpose Extraction
    explicit_purposes = {
        "투자자에게 보낼 IR 자료": "investment_IR",
        "이 아이디어를 특허로 출원": "patent_draft",
        "자기소개서 작성": "self_intro",
        "정책 제안서 만들어줘": "policy_proposal",
        "정부지원사업 신청서 작성": "grant_application",
        "사업계획서": "business_plan",
        "마케팅 카피": "marketing_copy",
        "회의 요약": "meeting_summary",
        "코드 실행": "code_run",
        "고객 응대": "customer_reply",
        "협업 제안": "collaboration_email",
        "제안서": "proposal",
        "IR 자료": "ir_draft",
        "특허": "patent_draft",
        "정책": "policy_proposal",
        "정부지원": "grant_application"
    }

    # 명시적 목적 검색
    for keyword, intent in explicit_purposes.items():
        if keyword in user_utterance:
            logger.info(f"✅ 명시적 목적 감지: {keyword} → {intent}")
            return build_template_instruction(intent, user_utterance)
    
    # STEP 2: LLM 추론 기반 목적 추정
    logger.info("🤖 LLM 기반 목적 추론 시작")
    inferred_intent = classify_intent_llm(user_utterance)
    if inferred_intent:
        logger.info(f"✅ 추론된 목적: {inferred_intent}")
        return build_template_instruction(inferred_intent, user_utterance)

    # STEP 3: 목적 불명확 → 사용자 재질문 유도
    logger.warning("❓ 목적 불명확, 사용자 재질문 필요")
    return {
        "intent": "unknown",
        "confidence": 0.0,
        "reconstructed_purpose": "사용자의 요청 목적이 명확하지 않음",
        "instruction": [
            "사용자의 발화에서 주제 또는 목적을 추정할 수 없음",
            "다음 중 어느 목적에 해당하는지 선택해 주세요:",
            "1) 자기소개서 2) 정책 제안 3) 특허 명세서 4) 투자자료 5) 사업계획서 6) 마케팅 카피 7) 기타",
            "정확한 응답을 위해 목적 선택이 필요합니다"
        ],
        "requires_clarification": True
    }

def classify_intent_llm(user_utterance: str) -> Optional[str]:
    """
    LLM을 사용하여 사용자 발화의 의도를 추론합니다.
    
    Args:
        user_utterance: 사용자 입력
        
    Returns:
        Optional[str]: 추론된 의도 또는 None
    """
    # 간단한 키워드 기반 추론 (실제로는 LLM API 호출)
    intent_keywords = {
        "business_plan": ["창업", "사업", "계획", "비즈니스", "스타트업"],
        "marketing_copy": ["마케팅", "홍보", "광고", "카피", "브랜딩"],
        "self_intro": ["자기소개", "소개서", "면접", "이력서"],
        "meeting_summary": ["회의", "요약", "정리", "회의록"],
        "code_run": ["코드", "실행", "프로그램", "개발"],
        "customer_reply": ["고객", "응대", "답변", "서비스"],
        "collaboration_email": ["협업", "제안", "이메일", "파트너십"],
        "proposal": ["제안서", "제안", "안건", "계획서"],
        "ir_draft": ["투자", "IR", "투자자", "자료"],
        "patent_draft": ["특허", "출원", "명세서", "지적재산권"],
        "policy_proposal": ["정책", "제안", "정부", "규정"],
        "grant_application": ["지원사업", "지원", "정부", "사업"]
    }
    
    user_lower = user_utterance.lower()
    
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in user_lower:
                logger.info(f"🔍 키워드 매칭: {keyword} → {intent}")
                return intent
    
    return None

def build_template_instruction(intent: str, user_utterance: str) -> Dict[str, Any]:
    """
    의도에 따른 템플릿 지시사항을 생성합니다.
    
    Args:
        intent: 분류된 의도
        user_utterance: 사용자 입력
        
    Returns:
        Dict[str, Any]: 템플릿 지시사항
    """
    templates = {
        "business_plan": {
            "title": "사업계획서 작성",
            "description": "체계적이고 전문적인 사업계획서를 작성합니다.",
            "sections": [
                "1. 사업 개요 및 비전",
                "2. 시장 분석 및 경쟁사 분석", 
                "3. 사업 모델 및 수익 모델",
                "4. 마케팅 전략",
                "5. 조직 구성 및 인력 계획",
                "6. 재무 계획 및 자금 조달",
                "7. 위험 요소 및 대응 방안"
            ]
        },
        "marketing_copy": {
            "title": "마케팅 카피 작성",
            "description": "감성적이고 설득력 있는 마케팅 카피를 작성합니다.",
            "sections": [
                "1. 핵심 메시지 및 가치 제안",
                "2. 타겟 고객 분석",
                "3. 감성적 어필 포인트",
                "4. 행동 유도 문구",
                "5. 브랜드 톤앤매너"
            ]
        },
        "self_intro": {
            "title": "자기소개서 작성",
            "description": "진정성 있고 설득력 있는 자기소개서를 작성합니다.",
            "sections": [
                "1. 개인적 배경 및 성장 과정",
                "2. 학력 및 경력 사항",
                "3. 핵심 역량 및 강점",
                "4. 지원 동기 및 포부",
                "5. 차별화된 경험 및 성과"
            ]
        },
        "meeting_summary": {
            "title": "회의 요약서 작성",
            "description": "명확하고 체계적인 회의 요약서를 작성합니다.",
            "sections": [
                "1. 회의 개요 및 참석자",
                "2. 주요 논의 사항",
                "3. 결정 사항 및 액션 아이템",
                "4. 다음 단계 및 일정",
                "5. 특이사항 및 후속 조치"
            ]
        },
        "code_run": {
            "title": "코드 실행 및 분석",
            "description": "코드를 실행하고 결과를 분석합니다.",
            "sections": [
                "1. 코드 분석 및 이해",
                "2. 실행 환경 설정",
                "3. 코드 실행 및 결과 확인",
                "4. 오류 분석 및 디버깅",
                "5. 최적화 제안"
            ]
        },
        "customer_reply": {
            "title": "고객 응대 메시지 작성",
            "description": "공감적이고 도움이 되는 고객 응대 메시지를 작성합니다.",
            "sections": [
                "1. 공감 표현 및 상황 이해",
                "2. 문제 분석 및 원인 파악",
                "3. 해결 방안 제시",
                "4. 추가 지원 및 후속 조치",
                "5. 감사 표현 및 관계 유지"
            ]
        },
        "collaboration_email": {
            "title": "협업 제안 이메일 작성",
            "description": "전문적이고 협력적인 협업 제안 이메일을 작성합니다.",
            "sections": [
                "1. 인사 및 상황 설명",
                "2. 협업 제안 배경 및 목적",
                "3. 제안하는 협업 방안",
                "4. 기대 효과 및 시너지",
                "5. 다음 단계 및 연락처"
            ]
        },
        "proposal": {
            "title": "제안서 작성",
            "description": "체계적이고 설득력 있는 제안서를 작성합니다.",
            "sections": [
                "1. 제안 개요 및 배경",
                "2. 문제 분석 및 필요성",
                "3. 제안 방안 및 해결책",
                "4. 기대 효과 및 성과",
                "5. 일정 및 예산",
                "6. 위험 요소 및 대응 방안"
            ]
        },
        "ir_draft": {
            "title": "IR 자료 작성",
            "description": "투자자를 대상으로 한 전문적인 IR 자료를 작성합니다.",
            "sections": [
                "1. 회사 개요 및 비전",
                "2. 사업 모델 및 시장 분석",
                "3. 재무 현황 및 전망",
                "4. 경쟁 우위 및 성장 전략",
                "5. 투자 포인트 및 기회"
            ]
        },
        "patent_draft": {
            "title": "특허 명세서 작성",
            "description": "법적 요건을 충족하는 특허 명세서를 작성합니다.",
            "sections": [
                "1. 발명의 명칭 및 기술분야",
                "2. 배경기술 및 선행기술",
                "3. 발명의 개요 및 해결하고자 하는 과제",
                "4. 발명의 상세한 설명",
                "5. 청구범위 및 도면 설명"
            ]
        },
        "policy_proposal": {
            "title": "정책 제안서 작성",
            "description": "정책적이고 논리적인 정책 제안서를 작성합니다.",
            "sections": [
                "1. 정책 제안 배경 및 필요성",
                "2. 현행 정책 분석 및 문제점",
                "3. 제안 정책의 내용 및 방향",
                "4. 기대 효과 및 영향 분석",
                "5. 추진 방안 및 일정"
            ]
        },
        "grant_application": {
            "title": "정부지원사업 신청서 작성",
            "description": "정부 지원사업 요건에 맞는 신청서를 작성합니다.",
            "sections": [
                "1. 사업 개요 및 목적",
                "2. 사업의 필요성 및 기대효과",
                "3. 사업 내용 및 추진 계획",
                "4. 사업 추진 체계 및 인력",
                "5. 사업비 산정 및 자금 조달 계획",
                "6. 사업 성과 측정 방안"
            ]
        },
        "investment_IR": {
            "title": "투자자 IR 자료 작성",
            "description": "투자자를 대상으로 한 전문적인 IR 자료를 작성합니다.",
            "sections": [
                "1. 회사 개요 및 투자 포인트",
                "2. 사업 모델 및 시장 분석",
                "3. 재무 현황 및 성장 전략",
                "4. 경쟁 우위 및 차별화 요소",
                "5. 투자 기회 및 전망"
            ]
        }
    }
    
    template = templates.get(intent, {
        "title": "일반 문서 작성",
        "description": "사용자 요청에 따른 문서를 작성합니다.",
        "sections": [
            "1. 문서 개요",
            "2. 주요 내용",
            "3. 결론 및 제안"
        ]
    })
    
    instruction = [
        f"📋 {template['title']}",
        f"📝 {template['description']}",
        "",
        "📌 작성 구조:",
        *template["sections"],
        "",
        f"사용자 요청: {user_utterance}",
        "",
        "위 구조에 따라 전문적이고 체계적인 문서를 작성해주세요."
    ]
    
    return {
        "intent": intent,
        "confidence": 0.9,
        "reconstructed_purpose": template["title"],
        "instruction": instruction,
        "template_info": template,
        "requires_clarification": False
    }

def get_system_stats() -> Dict[str, Any]:
    """
    시스템 통계 정보를 반환합니다.
    
    Returns:
        Dict[str, Any]: 시스템 통계
    """
    return {
        "system_name": "Cursor Instruction Generator",
        "version": "1.0.0",
        "supported_intents": [
            "business_plan", "marketing_copy", "self_intro", "meeting_summary",
            "code_run", "customer_reply", "collaboration_email", "proposal",
            "ir_draft", "patent_draft", "policy_proposal", "grant_application",
            "investment_IR"
        ],
        "features": [
            "명시적 목적 감지",
            "LLM 기반 의도 추론", 
            "템플릿 기반 지시사항 생성",
            "사용자 명확화 질문"
        ]
    }

# 테스트 함수
def test_generator():
    """시스템 테스트 함수"""
    test_cases = [
        "사업계획서 써줘",
        "마케팅 카피 만들어줘", 
        "자기소개서 작성 도와줘",
        "회의 요약해줘",
        "그냥 써줘"
    ]
    
    print("🧪 Cursor Instruction Generator 테스트")
    print("=" * 50)
    
    for test_input in test_cases:
        result = generate_instruction(test_input)
        print(f"📝 입력: {test_input}")
        print(f"🎯 의도: {result['intent']}")
        print(f"📊 신뢰도: {result['confidence']}")
        print(f"❓ 명확화 필요: {result['requires_clarification']}")
        print("-" * 30)

if __name__ == "__main__":
    test_generator() 