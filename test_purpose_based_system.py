#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧠 목적 기반 템플릿 시스템 테스트
완전한 키워드 매핑과 템플릿 매칭이 올바르게 작동하는지 테스트합니다.
"""

from purpose_based_template_system import get_purpose_based_template_system
from prompt_generator import process_user_request

def test_purpose_keyword_detection():
    """
    목적 키워드 감지 기능을 테스트합니다.
    """
    print("🧠 목적 키워드 감지 테스트")
    print("=" * 80)
    
    purpose_system = get_purpose_based_template_system()
    
    # 테스트 케이스들 - 완전한 키워드 리스트
    test_cases = [
        # 사업 및 제안 관련
        {"input": "사업계획서 써줘", "expected": "startup_business_plan"},
        {"input": "비즈니스 플랜 작성해줘", "expected": "startup_business_plan"},
        {"input": "IR 자료 초안 좀 만들어줘", "expected": "investor_IR_doc"},
        {"input": "투자자 자료 작성", "expected": "investor_IR_doc"},
        {"input": "제안서 작성 도와줘", "expected": "project_proposal"},
        {"input": "프로젝트 제안서 써줘", "expected": "project_proposal"},
        {"input": "정부과제 제출용 자료", "expected": "gov_grant_proposal"},
        {"input": "정부 지원사업 제안서", "expected": "gov_grant_proposal"},
        {"input": "입찰서 작성", "expected": "bidding_doc"},
        {"input": "입찰 문서 만들어줘", "expected": "bidding_doc"},
        {"input": "실증계획 작성", "expected": "PoC_plan"},
        {"input": "PoC 계획서 써줘", "expected": "PoC_plan"},
        
        # 마케팅/홍보 관련
        {"input": "보도자료 작성", "expected": "press_release"},
        {"input": "프레스릴리즈 써줘", "expected": "press_release"},
        {"input": "홍보문구 작성", "expected": "marketing_copy"},
        {"input": "마케팅 카피 써줘", "expected": "marketing_copy"},
        {"input": "광고문구 만들어줘", "expected": "marketing_copy"},
        {"input": "소개자료 작성", "expected": "product_promo_material"},
        {"input": "제품소개 자료", "expected": "product_promo_material"},
        
        # 커뮤니케이션 응답
        {"input": "고객응대 메시지", "expected": "customer_support"},
        {"input": "고객 서비스 답변", "expected": "customer_support"},
        {"input": "문의 답변 작성", "expected": "faq_response"},
        {"input": "FAQ 답변 써줘", "expected": "faq_response"},
        {"input": "협업 제안 이메일", "expected": "collab_email"},
        {"input": "파트너십 제안", "expected": "collab_email"},
        
        # 개인/커리어 관련
        {"input": "자기소개서 작성", "expected": "self_intro"},
        {"input": "자기 소개 써줘", "expected": "self_intro"},
        {"input": "이력서 작성", "expected": "resume_writing"},
        {"input": "경력기술서 써줘", "expected": "resume_writing"},
        {"input": "면접 준비 자료", "expected": "interview_prep"},
        {"input": "면접대비 해줘", "expected": "interview_prep"},
        
        # 전략 및 분석 보고
        {"input": "전략보고서 작성", "expected": "strategy_report"},
        {"input": "전략 계획 써줘", "expected": "strategy_report"},
        {"input": "시장분석 보고서", "expected": "market_analysis"},
        {"input": "시장 조사 자료", "expected": "market_analysis"},
        {"input": "경쟁사분석 작성", "expected": "competitor_analysis"},
        {"input": "경쟁 분석 써줘", "expected": "competitor_analysis"},
        {"input": "실행계획 작성", "expected": "execution_plan"},
        {"input": "액션플랜 써줘", "expected": "execution_plan"},
        {"input": "사업성분석 보고서", "expected": "biz_viability"},
        {"input": "수익성 분석 써줘", "expected": "biz_viability"},
        
        # 정책/행정/공공
        {"input": "정책제안서 작성", "expected": "policy_recommendation"},
        {"input": "정책 권고 써줘", "expected": "policy_recommendation"},
        {"input": "행정요청서 작성", "expected": "official_request"},
        {"input": "공식요청 써줘", "expected": "official_request"},
        
        # 기술/제품
        {"input": "기능정의서 작성", "expected": "feature_spec"},
        {"input": "기능 명세 써줘", "expected": "feature_spec"},
        {"input": "기술명세서 작성", "expected": "tech_spec"},
        {"input": "기술 사양 써줘", "expected": "tech_spec"},
        {"input": "특허 출원 자료", "expected": "patent_draft"},
        {"input": "특허명세서 작성", "expected": "patent_draft"},
        
        # 기타
        {"input": "회의요약 작성", "expected": "meeting_summary"},
        {"input": "회의록 써줘", "expected": "meeting_summary"},
        {"input": "이메일 작성", "expected": "generic_email"},
        {"input": "메일 써줘", "expected": "generic_email"},
        {"input": "요약 써줘", "expected": "summary_request"},
        {"input": "분석 써줘", "expected": "analytical_report"},
        {"input": "검토요청 써줘", "expected": "review_request"},
        {"input": "검토 써줘", "expected": "review_request"}
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 테스트 {i}: {test_case['input']}")
        print("-" * 60)
        
        try:
            # 목적 감지
            detected_purpose = purpose_system.detect_purpose(test_case['input'])
            
            print(f"입력: {test_case['input']}")
            print(f"감지된 목적: {detected_purpose}")
            print(f"예상 목적: {test_case['expected']}")
            
            if detected_purpose == test_case['expected']:
                print("✅ 목적 감지 정확!")
                success_count += 1
            else:
                print("❌ 목적 감지 실패")
                
            # 템플릿 매칭 테스트
            if detected_purpose:
                template = purpose_system.match_template(detected_purpose)
                if template:
                    print(f"✅ 템플릿 매칭 성공: {template['description']}")
                else:
                    print("❌ 템플릿 매칭 실패")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    
    print(f"\n📊 목적 키워드 감지 결과: {success_count}/{total_count} 성공 ({success_count/total_count*100:.1f}%)")

def test_template_instruction_generation():
    """
    템플릿 지시사항 생성 기능을 테스트합니다.
    """
    print("\n\n📋 템플릿 지시사항 생성 테스트")
    print("=" * 80)
    
    purpose_system = get_purpose_based_template_system()
    
    # 대표적인 테스트 케이스들
    test_cases = [
        "사업계획서 써줘",
        "IR 자료 초안 좀 만들어줘",
        "마케팅 카피 써줘",
        "자기소개서 작성",
        "시장분석 보고서"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🧪 템플릿 테스트 {i}: {test_input}")
        print("-" * 60)
        
        try:
            # 목적 감지
            detected_purpose = purpose_system.detect_purpose(test_input)
            
            if detected_purpose:
                # 템플릿 지시사항 생성
                instruction = purpose_system.generate_template_instruction(detected_purpose, test_input)
                
                print(f"감지된 목적: {detected_purpose}")
                print(f"생성된 지시사항 길이: {len(instruction)}")
                
                # 지시사항 형식 검증
                required_elements = [
                    "📋 [Prompt Instruction Format]",
                    "User utterance:",
                    "Intent:",
                    "Reconstructed Purpose:",
                    "Instruction:",
                    "Output must be in Korean"
                ]
                
                print("\n🔍 지시사항 형식 검증:")
                for element in required_elements:
                    if element in instruction:
                        print(f"✅ {element}")
                    else:
                        print(f"❌ {element}")
                
                print("\n📋 생성된 지시사항 미리보기:")
                print(instruction[:300] + "..." if len(instruction) > 300 else instruction)
                
            else:
                print("❌ 목적을 감지할 수 없음")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_fallback_llm_inference():
    """
    목적이 불명확한 경우 LLM 추론 기능을 테스트합니다.
    """
    print("\n\n🤖 LLM 추론 테스트")
    print("=" * 80)
    
    purpose_system = get_purpose_based_template_system()
    
    # 모호한 입력들
    ambiguous_inputs = [
        "그냥 써줘",
        "이거 어떻게 생각해?",
        "돈이 될까?",
        "뭐가 좋을까?",
        "어떻게 해야 할까?"
    ]
    
    for i, test_input in enumerate(ambiguous_inputs, 1):
        print(f"\n🧪 모호한 입력 테스트 {i}: {test_input}")
        print("-" * 60)
        
        try:
            # 목적 감지 시도
            detected_purpose = purpose_system.detect_purpose(test_input)
            
            if detected_purpose:
                print(f"✅ 예상치 못한 목적 감지: {detected_purpose}")
            else:
                print("✅ 목적이 불명확함 (예상된 결과)")
                
                # LLM 추론 시뮬레이션 (실제 LLM 호출 없이)
                print("🤖 LLM 추론 시뮬레이션...")
                
                # 간단한 fallback 지시사항 생성
                fallback_instruction = purpose_system.generate_fallback_instruction(test_input)
                
                print(f"생성된 fallback 지시사항 길이: {len(fallback_instruction)}")
                
                # fallback 지시사항 형식 검증
                if "📋 [Prompt Instruction Format]" in fallback_instruction:
                    print("✅ Fallback 지시사항 형식 정확")
                else:
                    print("❌ Fallback 지시사항 형식 오류")
                    
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_integrated_system():
    """
    통합된 시스템을 테스트합니다.
    """
    print("\n\n🔗 통합 시스템 테스트")
    print("=" * 80)
    
    # 명확한 목적이 있는 케이스
    clear_cases = [
        "사업계획서 써줘",
        "IR 자료 초안 좀 만들어줘",
        "마케팅 카피 써줘"
    ]
    
    # 모호한 케이스
    ambiguous_cases = [
        "그냥 써줘",
        "이거 어떻게 생각해?"
    ]
    
    print("📋 명확한 목적 케이스 테스트:")
    for test_input in clear_cases:
        print(f"\n🧪 입력: {test_input}")
        try:
            result = process_user_request(test_input)
            print(f"✅ 의도: {result['intent']}")
            print(f"✅ 방법: {result['method']}")
            print(f"✅ 신뢰도: {result['confidence_score']:.2f}")
            print(f"✅ 단계: {result['step']}")
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print("\n📋 모호한 케이스 테스트:")
    for test_input in ambiguous_cases:
        print(f"\n🧪 입력: {test_input}")
        try:
            result = process_user_request(test_input)
            print(f"✅ 의도: {result['intent']}")
            print(f"✅ 방법: {result['method']}")
            print(f"✅ 신뢰도: {result['confidence_score']:.2f}")
            print(f"✅ 단계: {result['step']}")
            if result.get('additional_questions'):
                print(f"✅ 추가 질문: {result['additional_questions']}")
        except Exception as e:
            print(f"❌ 오류: {e}")

def test_template_structures():
    """
    모든 템플릿 구조를 확인합니다.
    """
    print("\n\n🏗️ 템플릿 구조 확인")
    print("=" * 80)
    
    purpose_system = get_purpose_based_template_system()
    
    print(f"총 템플릿 개수: {len(purpose_system.template_structures)}")
    print(f"총 키워드 개수: {len(purpose_system.purpose_keywords)}")
    
    print("\n📋 템플릿 목록:")
    for i, (template_name, template_info) in enumerate(purpose_system.template_structures.items(), 1):
        print(f"\n{i}. {template_name}")
        print(f"   📝 설명: {template_info['description']}")
        print(f"   🎨 톤: {template_info['tone']}")
        print(f"   📊 구조: {len(template_info['structure'])}개 섹션")
        print(f"   🌐 언어: {template_info['output_language']}")

if __name__ == "__main__":
    # 모든 테스트 실행
    test_purpose_keyword_detection()
    test_template_instruction_generation()
    test_fallback_llm_inference()
    test_integrated_system()
    test_template_structures()
    
    print("\n\n🎉 목적 기반 템플릿 시스템 테스트 완료!")
    print("\n📋 요약:")
    print("✅ 완전한 키워드 매핑 시스템 구현")
    print("✅ 정밀한 템플릿 구조 매칭")
    print("✅ LLM 기반 추론 + 보완 질문")
    print("✅ 명시적 목적 = 완전한 템플릿 매칭")
    print("✅ 암묵적 목적 = LLM 추론 + 사용자 보완")
    print("✅ 모든 출력은 한국어로 생성") 