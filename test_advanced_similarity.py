#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
고급 유사도 분류 및 고유명사 기반 매핑 시스템 테스트
"""

from classify_intent import classify_intent
from naming_dict import naming_dict
from fallback_manager import fallback_manager

def test_naming_dict():
    """고유명사 사전을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS에 대한 제안서를 작성해줘",
            "expected_name": "프롬프트OS",
            "expected_intent": "startup_pitch",
            "description": "기술 플랫폼"
        },
        {
            "utterance": "ChatGPT를 활용한 교육 자료를 만들어줘",
            "expected_name": "ChatGPT",
            "expected_intent": "education_content",
            "description": "AI 모델"
        },
        {
            "utterance": "스마트시티 정책 분석을 해줘",
            "expected_name": "스마트시티",
            "expected_intent": "policy_brief",
            "description": "정부 정책"
        },
        {
            "utterance": "메타버스 플랫폼 소개서를 작성해줘",
            "expected_name": "메타버스",
            "expected_intent": "startup_pitch",
            "description": "기술 플랫폼"
        },
        {
            "utterance": "핀테크 투자 제안서를 작성해줘",
            "expected_name": "핀테크",
            "expected_intent": "startup_pitch",
            "description": "금융 기술"
        },
        {
            "utterance": "구글 서비스 마케팅 콘텐츠를 작성해줘",
            "expected_name": "구글",
            "expected_intent": "marketing_copy",
            "description": "기업 서비스"
        },
        {
            "utterance": "테슬라 전기차 소개서를 작성해줘",
            "expected_name": "테슬라",
            "expected_intent": "startup_pitch",
            "description": "기업 제품"
        },
        {
            "utterance": "코로나19 대응 정책을 분석해줘",
            "expected_name": "코로나19",
            "expected_intent": "policy_brief",
            "description": "정책 이슈"
        }
    ]
    
    print("🧪 고유명사 사전 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 고유명사: {test_case['expected_name']}")
        print(f"🎯 예상 Intent: {test_case['expected_intent']}")
        
        # 고유명사 찾기
        entity = naming_dict.get_best_mapping(test_case['utterance'])
        
        if entity:
            print(f"✅ 고유명사 발견: {entity['name']}")
            print(f"   설명: {entity['description']}")
            print(f"   Intent: {entity['intent']}")
            print(f"   도메인: {entity['domain']}")
            print(f"   대상: {entity['target']}")
            print(f"   톤: {entity['tone']}")
            
            if entity['name'] == test_case['expected_name']:
                print("🎉 고유명사 정확히 매칭!")
            else:
                print(f"⚠️ 고유명사 불일치: {entity['name']}")
            
            if entity['intent'] == test_case['expected_intent']:
                print("🎉 Intent 정확히 매칭!")
            else:
                print(f"⚠️ Intent 불일치: {entity['intent']}")
        else:
            print("❌ 고유명사를 찾을 수 없음")
        
        print("-" * 60)
        print()

def test_advanced_similarity_classification():
    """고급 유사도 분류를 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS 기술 소개서를 작성해줘",
            "expected_intent": "startup_pitch",
            "description": "고유명사 기반 분류"
        },
        {
            "utterance": "ChatGPT 활용 가이드를 만들어줘",
            "expected_intent": "education_content",
            "description": "AI 관련 고유명사"
        },
        {
            "utterance": "스마트시티 정책 제안서를 작성해줘",
            "expected_intent": "policy_brief",
            "description": "정부 정책 고유명사"
        },
        {
            "utterance": "메타버스 플랫폼 마케팅 콘텐츠를 작성해줘",
            "expected_intent": "startup_pitch",
            "description": "기술 플랫폼 고유명사"
        },
        {
            "utterance": "핀테크 투자 피칭을 작성해줘",
            "expected_intent": "startup_pitch",
            "description": "금융 기술 고유명사"
        },
        {
            "utterance": "구글 서비스 소개서를 작성해줘",
            "expected_intent": "marketing_copy",
            "description": "기업 서비스 고유명사"
        },
        {
            "utterance": "테슬라 전기차 마케팅을 해줘",
            "expected_intent": "startup_pitch",
            "description": "기업 제품 고유명사"
        },
        {
            "utterance": "코로나19 대응 방안을 제시해줘",
            "expected_intent": "policy_brief",
            "description": "정책 이슈 고유명사"
        },
        {
            "utterance": "탄소중립 정책을 분석해줘",
            "expected_intent": "policy_brief",
            "description": "환경 정책 고유명사"
        },
        {
            "utterance": "유튜브 콘텐츠 마케팅을 해줘",
            "expected_intent": "marketing_copy",
            "description": "플랫폼 서비스 고유명사"
        }
    ]
    
    print("🧪 고급 유사도 분류 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        print(f"🎯 예상 Intent: {test_case['expected_intent']}")
        
        # Intent 분류 (고급 유사도 기반)
        intent = classify_intent(test_case['utterance'])
        print(f"✅ 분류된 Intent: {intent}")
        
        if intent == test_case['expected_intent']:
            print("🎉 정확히 분류됨!")
        else:
            print(f"⚠️ 예상과 다름: {intent}")
        
        print("-" * 60)
        print()

def test_enhanced_fallback_generation():
    """향상된 fallback 생성을 테스트합니다."""
    
    test_cases = [
        {
            "utterance": "프롬프트OS 플랫폼 소개서를 작성해줘",
            "description": "고유명사가 포함된 요청"
        },
        {
            "utterance": "ChatGPT 활용 교육 자료를 만들어줘",
            "description": "AI 관련 고유명사"
        },
        {
            "utterance": "스마트시티 정책 분석을 해줘",
            "description": "정부 정책 고유명사"
        },
        {
            "utterance": "메타버스 플랫폼 마케팅을 해줘",
            "description": "기술 플랫폼 고유명사"
        },
        {
            "utterance": "핀테크 투자 제안서를 작성해줘",
            "description": "금융 기술 고유명사"
        }
    ]
    
    print("🧪 향상된 Fallback 생성 테스트 시작\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 테스트 케이스 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        # Intent 분류
        intent = classify_intent(test_case['utterance'])
        print(f"🎯 분류된 Intent: {intent}")
        
        # 고유명사 정보 확인
        entity = naming_dict.get_best_mapping(test_case['utterance'])
        if entity:
            print(f"📋 발견된 고유명사: {entity['name']}")
            print(f"   권장 Intent: {entity['intent']}")
            print(f"   도메인: {entity['domain']}")
            print(f"   대상: {entity['target']}")
        
        # 향상된 fallback 생성
        try:
            enhanced_prompt = fallback_manager.generate_prompt_with_llm(
                test_case['utterance'], intent
            )
            print(f"✅ 향상된 프롬프트 생성 성공 (길이: {len(enhanced_prompt)} 문자)")
            print(f"📄 프롬프트 미리보기: {enhanced_prompt[:300]}...")
        except Exception as e:
            print(f"❌ 프롬프트 생성 실패: {e}")
        
        print("-" * 60)
        print()

def test_naming_dict_search():
    """고유명사 검색 기능을 테스트합니다."""
    
    search_queries = [
        "프롬프트",
        "AI",
        "정부",
        "금융",
        "기술",
        "교육",
        "의료",
        "환경"
    ]
    
    print("🧪 고유명사 검색 테스트 시작\n")
    
    for query in search_queries:
        print(f"🔍 검색 쿼리: '{query}'")
        
        # 유사한 고유명사 검색
        similar_names = naming_dict.search_similar_names(query)
        
        if similar_names:
            print(f"✅ {len(similar_names)}개의 유사한 고유명사 발견:")
            for i, name_info in enumerate(similar_names, 1):
                print(f"  {i}. {name_info['name']} - {name_info['description']}")
                print(f"     Intent: {name_info['intent']}, 도메인: {name_info['domain']}")
        else:
            print("❌ 유사한 고유명사를 찾을 수 없음")
        
        print("-" * 40)
        print()

if __name__ == "__main__":
    print("🚀 고급 유사도 분류 및 고유명사 기반 매핑 시스템 테스트\n")
    
    # 1. 고유명사 사전 테스트
    test_naming_dict()
    
    # 2. 고급 유사도 분류 테스트
    test_advanced_similarity_classification()
    
    # 3. 향상된 fallback 생성 테스트
    test_enhanced_fallback_generation()
    
    # 4. 고유명사 검색 테스트
    test_naming_dict_search()
    
    print("✅ 모든 테스트 완료!") 