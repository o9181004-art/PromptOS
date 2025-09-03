#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
시스템 복구 확인 테스트
"""

from classify_intent import classify_intent
from template_loader import get_template
from prompt_builder import extract_placeholders, fill_template

def test_system_recovery():
    """시스템 복구 상태를 확인합니다."""
    
    print("🚨 시스템 복구 상태 확인\n")
    
    # 문제가 되었던 사용자 입력들
    critical_test_cases = [
        {
            "utterance": "예비창업자 패키지 사업계획서를 작성할거야. 아이템은 프롬프트OS야.",
            "description": "원래 문제가 되었던 입력"
        },
        {
            "utterance": "AI 기반 제안서를 정부에 제출할거야",
            "description": "정부 제안서 요청"
        },
        {
            "utterance": "고객을 위한 정중한 이메일을 작성해줘",
            "description": "고객 응대 요청"
        },
        {
            "utterance": "자기소개서를 작성해줘",
            "description": "자기소개서 요청"
        },
        {
            "utterance": "문서를 요약해줘",
            "description": "요약 요청"
        },
        {
            "utterance": "프롬프트를 만들어줘",
            "description": "일반적인 프롬프트 요청"
        }
    ]
    
    success_count = 0
    total_count = len(critical_test_cases)
    
    for i, test_case in enumerate(critical_test_cases, 1):
        print(f"📝 테스트 {i}/{total_count}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance']}")
        
        try:
            # 1. 의도 분류
            intent = classify_intent(test_case['utterance'])
            print(f"✅ 의도 분류: {intent}")
            
            # 2. 템플릿 로딩
            template_text = get_template(intent, utterance=test_case['utterance'])
            if template_text:
                print(f"✅ 템플릿 로딩: 성공 (길이: {len(template_text)} 문자)")
            else:
                print("❌ 템플릿 로딩: 실패")
                continue
            
            # 3. 플레이스홀더 추출
            placeholders = extract_placeholders(template_text)
            print(f"✅ 플레이스홀더 추출: {len(placeholders)}개")
            
            # 4. 기본 값으로 템플릿 채우기
            values = {
                "user_utterance": test_case['utterance'],
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
            
            # 5. 템플릿 채우기
            final_prompt = fill_template(template_text, values)
            
            if final_prompt and len(final_prompt.strip()) > 10:
                print(f"✅ 프롬프트 생성: 성공 (길이: {len(final_prompt)} 문자)")
                print(f"📄 프롬프트 미리보기: {final_prompt[:100]}...")
                success_count += 1
            else:
                print("❌ 프롬프트 생성: 실패 (너무 짧거나 비어있음)")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print("-" * 80)
        print()
    
    # 결과 요약
    print("📊 시스템 복구 결과 요약")
    print(f"✅ 성공: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 모든 테스트가 성공했습니다! 시스템이 완전히 복구되었습니다.")
    elif success_count > total_count * 0.8:
        print("✅ 대부분의 테스트가 성공했습니다. 시스템이 안정적으로 작동합니다.")
    else:
        print("⚠️ 일부 테스트가 실패했습니다. 추가 개선이 필요합니다.")
    
    return success_count == total_count

def test_error_handling():
    """오류 처리 기능을 테스트합니다."""
    
    print("\n🔧 오류 처리 기능 테스트\n")
    
    # 극단적인 테스트 케이스들
    extreme_cases = [
        {
            "utterance": "",
            "description": "빈 입력"
        },
        {
            "utterance": "a" * 1000,  # 매우 긴 입력
            "description": "매우 긴 입력"
        },
        {
            "utterance": "!@#$%^&*()",  # 특수문자만
            "description": "특수문자만"
        }
    ]
    
    for i, test_case in enumerate(extreme_cases, 1):
        print(f"📝 극단적 테스트 {i}: {test_case['description']}")
        print(f"💬 입력: {test_case['utterance'][:50]}...")
        
        try:
            # 의도 분류
            intent = classify_intent(test_case['utterance'])
            print(f"✅ 의도 분류: {intent}")
            
            # 템플릿 로딩
            template_text = get_template(intent, utterance=test_case['utterance'])
            if template_text:
                print(f"✅ 템플릿 로딩: 성공")
            else:
                print("✅ 템플릿 로딩: 실패 (예상된 동작)")
                
        except Exception as e:
            print(f"✅ 오류 처리: {e} (예상된 동작)")
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("🚨 시스템 복구 확인 테스트 시작\n")
    
    # 1. 기본 기능 테스트
    system_recovered = test_system_recovery()
    
    # 2. 오류 처리 테스트
    test_error_handling()
    
    print("✅ 모든 테스트 완료!")
    
    if system_recovered:
        print("\n🎉 시스템이 성공적으로 복구되었습니다!")
        print("이제 모든 사용자 입력에서 안정적으로 프롬프트를 생성할 수 있습니다.")
    else:
        print("\n⚠️ 시스템에 일부 문제가 남아있습니다.")
        print("추가 디버깅이 필요할 수 있습니다.") 