#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧠 [커서 지시글: 목적 기반 템플릿 시스템 초고도화]

완전한 목적 키워드 기반 템플릿 분류 및 매칭 시스템
- 명확한 목적이 있는 경우: 완전한 템플릿 리스트에서 정밀 매칭
- 불명확한 경우: LLM 기반 추론 + 보완 질문
"""

import logging
from typing import Dict, List, Optional, Tuple
from llm_api import call_llm_openrouter as call_llm_api

logger = logging.getLogger(__name__)

class PurposeBasedTemplateSystem:
    """
    목적 기반 템플릿 시스템
    사용자 발화의 목적을 정확히 파악하고 적절한 템플릿을 매칭하는 시스템
    """
    
    def __init__(self):
        # ✅ 1. 목적 키워드 기반 템플릿 분류 기준 (완전 리스트)
        self.purpose_keywords = {
            # 사업 및 제안 관련
            "사업계획서": "startup_business_plan",
            "사업 계획서": "startup_business_plan",
            "비즈니스 플랜": "startup_business_plan",
            "비즈니스플랜": "startup_business_plan",
            "IR": "investor_IR_doc",
            "IR자료": "investor_IR_doc",
            "IR 자료": "investor_IR_doc",
            "투자자자료": "investor_IR_doc",
            "투자자 자료": "investor_IR_doc",
            "제안서": "project_proposal",
            "프로젝트 제안서": "project_proposal",
            "정부과제": "gov_grant_proposal",
            "정부 과제": "gov_grant_proposal",
            "정부지원": "gov_grant_proposal",
            "정부 지원": "gov_grant_proposal",
            "입찰서": "bidding_doc",
            "입찰 문서": "bidding_doc",
            "실증계획": "PoC_plan",
            "실증 계획": "PoC_plan",
            "PoC": "PoC_plan",
            "개념증명": "PoC_plan",

            # 마케팅/홍보 관련
            "보도자료": "press_release",
            "보도 자료": "press_release",
            "프레스릴리즈": "press_release",
            "홍보문구": "marketing_copy",
            "홍보 문구": "marketing_copy",
            "마케팅카피": "marketing_copy",
            "마케팅 카피": "marketing_copy",
            "광고문구": "marketing_copy",
            "광고 문구": "marketing_copy",
            "소개자료": "product_promo_material",
            "소개 자료": "product_promo_material",
            "제품소개": "product_promo_material",
            "제품 소개": "product_promo_material",

            # 커뮤니케이션 응답
            "고객응대": "customer_support",
            "고객 응대": "customer_support",
            "고객서비스": "customer_support",
            "고객 서비스": "customer_support",
            "문의 답변": "faq_response",
            "FAQ": "faq_response",
            "자주묻는질문": "faq_response",
            "자주 묻는 질문": "faq_response",
            "협업 제안": "collab_email",
            "협업제안": "collab_email",
            "파트너십": "collab_email",
            "파트너쉽": "collab_email",
            
            # 개인/커리어 관련
            "자기소개": "self_intro",
            "자기 소개": "self_intro",
            "자기소개서": "self_intro",
            "이력서": "resume_writing",
            "경력기술서": "resume_writing",
            "경력 기술서": "resume_writing",
            "면접 준비": "interview_prep",
            "면접준비": "interview_prep",
            "면접대비": "interview_prep",
            "면접 대비": "interview_prep",

            # 전략 및 분석 보고
            "전략보고서": "strategy_report",
            "전략 보고서": "strategy_report",
            "전략계획": "strategy_report",
            "전략 계획": "strategy_report",
            "시장분석": "market_analysis",
            "시장 분석": "market_analysis",
            "시장조사": "market_analysis",
            "시장 조사": "market_analysis",
            "경쟁사분석": "competitor_analysis",
            "경쟁사 분석": "competitor_analysis",
            "경쟁분석": "competitor_analysis",
            "경쟁 분석": "competitor_analysis",
            "실행계획": "execution_plan",
            "실행 계획": "execution_plan",
            "액션플랜": "execution_plan",
            "액션 플랜": "execution_plan",
            "사업성분석": "biz_viability",
            "사업성 분석": "biz_viability",
            "사업성검토": "biz_viability",
            "사업성 검토": "biz_viability",
            "수익성분석": "biz_viability",
            "수익성 분석": "biz_viability",

            # 정책/행정/공공
            "정책제안": "policy_recommendation",
            "정책 제안": "policy_recommendation",
            "정책권고": "policy_recommendation",
            "정책 권고": "policy_recommendation",
            "행정요청": "official_request",
            "행정 요청": "official_request",
            "공식요청": "official_request",
            "공식 요청": "official_request",

            # 기술/제품
            "기능정의": "feature_spec",
            "기능 정의": "feature_spec",
            "기능명세": "feature_spec",
            "기능 명세": "feature_spec",
            "기술명세서": "tech_spec",
            "기술 명세서": "tech_spec",
            "기술사양": "tech_spec",
            "기술 사양": "tech_spec",
            "특허": "patent_draft",
            "특허출원": "patent_draft",
            "특허 출원": "patent_draft",
            "특허명세서": "patent_draft",
            "특허 명세서": "patent_draft",
            
            # 기타
            "회의요약": "meeting_summary",
            "회의 요약": "meeting_summary",
            "회의록": "meeting_summary",
            "이메일": "generic_email",
            "메일": "generic_email",
            "요약": "summary_request",
            "분석": "analytical_report",
            "검토요청": "review_request",
            "검토 요청": "review_request",
            "검토": "review_request"
        }
        
        # ✅ 3. 템플릿 구조 예시 매칭
        self.template_structures = {
            "startup_business_plan": {
                "structure": ["요약", "문제 정의", "솔루션", "시장 분석", "비즈니스 모델", "로드맵", "재무 계획"],
                "tone": "격식 있고 논리적인",
                "output_language": "Korean",
                "description": "스타트업 사업계획서 작성"
            },
            "investor_IR_doc": {
                "structure": ["회사 개요", "핵심 지표", "시장기회", "경쟁력", "투자 요청사항"],
                "tone": "전문적이고 설득력 있는",
                "output_language": "Korean",
                "description": "투자자 대상 IR 문서 작성"
            },
            "project_proposal": {
                "structure": ["프로젝트 개요", "배경 및 필요성", "목표 및 범위", "실행 계획", "예산 및 일정", "기대효과"],
                "tone": "전문적이고 체계적인",
                "output_language": "Korean",
                "description": "프로젝트 제안서 작성"
            },
            "gov_grant_proposal": {
                "structure": ["사업 개요", "정부 정책 연계성", "사업의 필요성", "실행 계획", "예산 계획", "기대효과"],
                "tone": "공식적이고 정책 지향적",
                "output_language": "Korean",
                "description": "정부 지원사업 제안서 작성"
            },
            "bidding_doc": {
                "structure": ["입찰 개요", "기술 제안", "가격 제안", "실행 계획", "품질 보증", "사후 관리"],
                "tone": "공식적이고 경쟁력 있는",
                "output_language": "Korean",
                "description": "입찰 문서 작성"
            },
            "PoC_plan": {
                "structure": ["개념증명 목표", "검증 방법", "실험 설계", "평가 기준", "일정 계획", "예상 결과"],
                "tone": "과학적이고 체계적인",
                "output_language": "Korean",
                "description": "개념증명(PoC) 계획서 작성"
            },
            "press_release": {
                "structure": ["헤드라인", "리드", "본문", "인용문", "회사 정보", "연락처"],
                "tone": "객관적이고 뉴스성 있는",
                "output_language": "Korean",
                "description": "보도자료 작성"
            },
            "marketing_copy": {
                "structure": ["헤드라인", "서브헤드라인", "본문", "CTA", "브랜드 정보"],
                "tone": "감성적이고 설득력 있는",
                "output_language": "Korean",
                "description": "마케팅 카피 작성"
            },
            "product_promo_material": {
                "structure": ["제품 개요", "주요 특징", "사용 시나리오", "장점", "연락처"],
                "tone": "친근하고 정보 제공적",
                "output_language": "Korean",
                "description": "제품 소개 자료 작성"
            },
            "customer_support": {
                "structure": ["공감 표현", "문제 인정", "해결 방안", "예방 조치", "추가 지원"],
                "tone": "공감적이고 도움이 되는",
                "output_language": "Korean",
                "description": "고객 응대 메시지 작성"
            },
            "faq_response": {
                "structure": ["질문 요약", "명확한 답변", "추가 설명", "관련 정보", "후속 조치"],
                "tone": "명확하고 도움이 되는",
                "output_language": "Korean",
                "description": "FAQ 답변 작성"
            },
            "collab_email": {
                "structure": ["인사", "협업 제안 배경", "구체적 제안", "기대효과", "다음 단계"],
                "tone": "전문적이고 협력적인",
                "output_language": "Korean",
                "description": "협업 제안 이메일 작성"
            },
            "self_intro": {
                "structure": ["인사", "주요 경력", "핵심 역량", "관심 분야", "연락처"],
                "tone": "자신감 있고 진정성 있는",
                "output_language": "Korean",
                "description": "자기소개서 작성"
            },
            "resume_writing": {
                "structure": ["개인 정보", "경력 요약", "주요 프로젝트", "기술 스택", "교육 및 자격"],
                "tone": "전문적이고 객관적인",
                "output_language": "Korean",
                "description": "이력서 작성"
            },
            "interview_prep": {
                "structure": ["자기소개", "주요 경험", "지원 동기", "강점 및 약점", "질문"],
                "tone": "자신감 있고 솔직한",
                "output_language": "Korean",
                "description": "면접 준비 자료 작성"
            },
            "strategy_report": {
                "structure": ["전략 개요", "현재 상황 분석", "전략 방향", "실행 계획", "기대효과"],
                "tone": "전략적이고 분석적인",
                "output_language": "Korean",
                "description": "전략 보고서 작성"
            },
            "market_analysis": {
                "structure": ["시장 개요", "시장 규모", "성장 동향", "주요 플레이어", "기회 요인"],
                "tone": "객관적이고 분석적인",
                "output_language": "Korean",
                "description": "시장 분석 보고서 작성"
            },
            "competitor_analysis": {
                "structure": ["경쟁 환경", "주요 경쟁사", "경쟁력 비교", "차별화 포인트", "전략적 시사점"],
                "tone": "객관적이고 전략적인",
                "output_language": "Korean",
                "description": "경쟁사 분석 보고서 작성"
            },
            "execution_plan": {
                "structure": ["실행 목표", "주요 활동", "담당자 및 역할", "일정 계획", "성과 지표"],
                "tone": "구체적이고 실행 가능한",
                "output_language": "Korean",
                "description": "실행 계획서 작성"
            },
            "biz_viability": {
                "structure": ["사업 개요", "시장 분석", "수익 모델", "재무 계획", "리스크 분석"],
                "tone": "객관적이고 분석적인",
                "output_language": "Korean",
                "description": "사업성 분석 보고서 작성"
            },
            "policy_recommendation": {
                "structure": ["정책 현황", "문제점 분석", "개선 방안", "기대효과", "실행 로드맵"],
                "tone": "정책적이고 논리적인",
                "output_language": "Korean",
                "description": "정책 제안서 작성"
            },
            "official_request": {
                "structure": ["요청 배경", "구체적 요청사항", "근거 및 필요성", "기대효과", "연락처"],
                "tone": "공식적이고 정중한",
                "output_language": "Korean",
                "description": "공식 요청서 작성"
            },
            "feature_spec": {
                "structure": ["기능 개요", "상세 요구사항", "사용자 시나리오", "기술적 고려사항", "테스트 계획"],
                "tone": "기술적이고 정확한",
                "output_language": "Korean",
                "description": "기능 정의서 작성"
            },
            "tech_spec": {
                "structure": ["기술 개요", "시스템 아키텍처", "기술 요구사항", "구현 방법", "품질 기준"],
                "tone": "기술적이고 전문적인",
                "output_language": "Korean",
                "description": "기술 명세서 작성"
            },
            "patent_draft": {
                "structure": ["발명의 개요", "기존 기술", "발명의 구성", "실시예", "청구범위"],
                "tone": "법적이고 정확한",
                "output_language": "Korean",
                "description": "특허 명세서 작성"
            },
            "meeting_summary": {
                "structure": ["회의 개요", "주요 논의사항", "결정사항", "액션 아이템", "다음 회의"],
                "tone": "객관적이고 요약적인",
                "output_language": "Korean",
                "description": "회의 요약서 작성"
            },
            "generic_email": {
                "structure": ["인사", "본문", "요청사항", "마무리", "서명"],
                "tone": "정중하고 명확한",
                "output_language": "Korean",
                "description": "일반 이메일 작성"
            },
            "summary_request": {
                "structure": ["요약 개요", "주요 내용", "핵심 포인트", "결론", "추가 정보"],
                "tone": "간결하고 명확한",
                "output_language": "Korean",
                "description": "요약문 작성"
            },
            "analytical_report": {
                "structure": ["분석 목적", "데이터 및 방법", "분석 결과", "해석", "결론 및 제언"],
                "tone": "객관적이고 분석적인",
                "output_language": "Korean",
                "description": "분석 보고서 작성"
            },
            "review_request": {
                "structure": ["검토 요청 배경", "검토 대상", "검토 관점", "기한", "연락처"],
                "tone": "정중하고 구체적인",
                "output_language": "Korean",
                "description": "검토 요청서 작성"
            }
        }

    def detect_purpose(self, user_input: str) -> Optional[str]:
        """
        ✅ 2. 의도 판단 및 템플릿 매칭 로직
        사용자 입력에서 목적 키워드를 찾아 해당하는 intent를 반환
        """
        user_input_lower = user_input.lower()
        
        for keyword, intent in self.purpose_keywords.items():
            if keyword.lower() in user_input_lower:
                logger.info(f"목적 키워드 감지: '{keyword}' → {intent}")
                return intent
        
        logger.info("명확한 목적 키워드를 찾을 수 없음")
        return None

    def match_template(self, purpose: str) -> Optional[Dict]:
        """
        목적에 따른 템플릿 구조 반환
        """
        template = self.template_structures.get(purpose)
        if template:
            logger.info(f"템플릿 매칭 성공: {purpose}")
            return template
        else:
            logger.warning(f"템플릿을 찾을 수 없음: {purpose}")
            return None

    def generate_template_instruction(self, purpose: str, user_input: str) -> str:
        """
        목적에 따른 표준화된 템플릿 지시사항 생성
        """
        template = self.match_template(purpose)
        if not template:
            return self.generate_fallback_instruction(user_input)
        
        structure_items = "\n".join([f"- {item}" for item in template["structure"]])
        
        return f"""📋 [Prompt Instruction Format]

User utterance: "{user_input}"
Intent: {purpose}
Reconstructed Purpose: {template['description']}
Instruction:
{structure_items}
- {template['tone']} 톤으로 작성
- Output must be in Korean

추가 지침:
- 각 섹션을 명확하게 구분하여 작성
- 구체적이고 실행 가능한 내용 포함
- 전문적이면서도 이해하기 쉽게 작성
- 필요시 예시나 데이터를 포함하여 설득력 향상"""

    def fallback_to_llm(self, user_input: str, history: List[Dict] = None) -> Dict:
        """
        ✅ 4. 목적 불명확 시 LLM 추론 + 사용자 보완 요청
        """
        # 대화 히스토리 포맷팅
        history_text = ""
        if history:
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in history[-5:]  # 최근 5개 메시지만 사용
            ])
        
        prompt = f"""
다음은 사용자의 발화입니다: "{user_input}"

이전 대화 내용:
{history_text if history_text else "대화 히스토리가 없습니다."}

위 정보를 기반으로 사용자의 발화 목적을 추론하고, 가장 적절한 템플릿 구조를 제안하세요.

분석 결과를 다음 형식으로 응답해주세요:

**추론된 목적**: [가장 적절한 목적 카테고리]
**신뢰도**: [0.0-1.0 사이의 값]
**추천 템플릿**: [템플릿 이름]
**추가 질문**: [목적 파악을 위한 구체적인 질문들]

만약 목적이 명확하지 않으면, 목적 파악을 위한 추가 질문을 생성하세요.
"""
        
        try:
            response = call_llm_api(prompt)
            return self.parse_llm_response(response)
        except Exception as e:
            logger.error(f"LLM 추론 중 오류 발생: {e}")
            return self.generate_fallback_instruction(user_input)

    def parse_llm_response(self, response: str) -> Dict:
        """
        LLM 응답을 파싱하여 구조화된 결과 반환
        """
        try:
            # 간단한 파싱 로직 (실제로는 더 정교한 파싱 필요)
            lines = response.split('\n')
            result = {
                "purpose": "general_inquiry",
                "confidence": 0.5,
                "template": "generic_email",
                "additional_questions": [],
                "instruction": self.generate_fallback_instruction("사용자 요청")
            }
            
            for line in lines:
                if "추론된 목적" in line:
                    result["purpose"] = line.split(":")[-1].strip()
                elif "신뢰도" in line:
                    try:
                        result["confidence"] = float(line.split(":")[-1].strip())
                    except:
                        pass
                elif "추천 템플릿" in line:
                    result["template"] = line.split(":")[-1].strip()
                elif "추가 질문" in line:
                    questions = line.split(":")[-1].strip()
                    result["additional_questions"] = [q.strip() for q in questions.split(",")]
            
            return result
        except Exception as e:
            logger.error(f"LLM 응답 파싱 중 오류: {e}")
            return {
                "purpose": "general_inquiry",
                "confidence": 0.0,
                "template": "generic_email",
                "additional_questions": ["어떤 종류의 문서를 작성하고 싶으신가요?"],
                "instruction": self.generate_fallback_instruction("사용자 요청")
            }

    def generate_fallback_instruction(self, user_input: str) -> str:
        """
        기본 fallback 지시사항 생성
        """
        return f"""📋 [Prompt Instruction Format]

User utterance: "{user_input}"
Intent: general_inquiry
Reconstructed Purpose: 사용자의 요청을 분석하여 가능한 목적을 추론하고 도움이 되는 응답 제공
Instruction:
- 사용자의 발화에서 핵심 키워드나 주제를 식별
- 가능한 목적이나 의도를 추론하여 맥락에 맞는 응답 생성
- 한국어로 친근하고 도움이 되는 톤으로 응답
- 필요시 명확화를 위한 후속 질문 제안
- 사용자가 추가 정보를 제공할 수 있도록 안내
- 진정성 있는 톤과 정보 제공적 스타일로 일반 대상에게 적합한 응답
- Output must be in Korean

추가 지침:
- 사용자의 요청이 모호한 경우, 가능한 해석들을 제시
- 구체적인 예시나 단계별 가이드 제공
- 사용자의 상황에 맞는 실용적인 조언 포함
- 필요시 추가 질문을 통해 더 정확한 도움을 제공할 수 있도록 안내"""

    def process_user_request(self, user_input: str, history: List[Dict] = None) -> Dict:
        """
        메인 처리 함수: 사용자 요청을 분석하고 적절한 템플릿 지시사항 생성
        """
        logger.info(f"사용자 요청 처리 시작: {user_input[:50]}...")
        
        # 1단계: 명확한 목적 키워드 검색
        detected_purpose = self.detect_purpose(user_input)
        
        if detected_purpose:
            # 명확한 목적이 있는 경우: 완전한 템플릿 매칭
            logger.info(f"명확한 목적 감지: {detected_purpose}")
            instruction = self.generate_template_instruction(detected_purpose, user_input)
            
            return {
                "intent": detected_purpose,
                "prompt_instruction": instruction,
                "confidence_score": 0.9,
                "method": "explicit_purpose_matching",
                "template_matched": True,
                "step": "Step 2: Template Matching",
                "additional_questions": []
            }
        else:
            # 목적이 불명확한 경우: LLM 기반 추론 + 보완 질문
            logger.info("목적이 불명확하여 LLM 기반 추론 수행")
            llm_result = self.fallback_to_llm(user_input, history)
            
            return {
                "intent": llm_result["purpose"],
                "prompt_instruction": llm_result["instruction"],
                "confidence_score": llm_result["confidence"],
                "method": "llm_purpose_inference",
                "template_matched": False,
                "step": "Step 3: Purpose Inference",
                "additional_questions": llm_result["additional_questions"]
            }

# 전역 인스턴스 생성
purpose_system = PurposeBasedTemplateSystem()

def get_purpose_based_template_system() -> PurposeBasedTemplateSystem:
    """
    목적 기반 템플릿 시스템 인스턴스 반환
    """
    return purpose_system 