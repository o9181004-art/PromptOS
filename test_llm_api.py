#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM API 통합 기능 테스트 스크립트
"""

from llm_api import llm_client, call_llm, call_llm_openrouter, call_llm_groq, call_llm_together
from config import config

def test_llm_providers():
    """다양한 LLM 제공업체를 테스트합니다."""
    
    test_prompt = "안녕하세요! 간단한 자기소개를 해주세요."
    
    print("🧪 LLM API 통합 기능 테스트 시작\n")
    
    # 1. 사용 가능한 제공업체 확인
    print("📋 사용 가능한 제공업체:")
    available_providers = config.get_available_providers()
    for provider, available in available_providers.items():
        status = "✅" if available else "❌"
        print(f"  {status} {provider}")
    print()
    
    # 2. 기본 제공업체 확인
    default_provider = config.get_default_provider()
    print(f"🎯 기본 제공업체: {default_provider}")
    print()
    
    # 3. 각 제공업체별 테스트
    providers_to_test = ["openrouter", "groq", "together"]
    
    for provider in providers_to_test:
        if not config.is_provider_available(provider):
            print(f"⚠️ {provider} API 키가 설정되지 않아 건너뜁니다.")
            continue
            
        print(f"🔄 {provider} 테스트 중...")
        
        try:
            # 개별 함수 테스트
            if provider == "openrouter":
                response = call_llm_openrouter(test_prompt)
            elif provider == "groq":
                response = call_llm_groq(test_prompt)
            elif provider == "together":
                response = call_llm_together(test_prompt)
            
            print(f"✅ {provider} 응답 (첫 100자): {response[:100]}...")
            
        except Exception as e:
            print(f"❌ {provider} 테스트 실패: {e}")
        
        print("-" * 50)
    
    # 4. 통합 함수 테스트
    print("🔄 통합 call_llm() 함수 테스트...")
    try:
        response = call_llm(test_prompt)
        print(f"✅ 통합 함수 응답 (첫 100자): {response[:100]}...")
    except Exception as e:
        print(f"❌ 통합 함수 테스트 실패: {e}")
    
    print("\n✅ 모든 테스트 완료!")

def test_model_configs():
    """모델 설정을 테스트합니다."""
    
    print("\n🔧 모델 설정 테스트\n")
    
    for provider in ["openrouter", "groq", "together"]:
        print(f"📋 {provider} 사용 가능한 모델:")
        models = config.get_available_models(provider)
        for model in models:
            print(f"  - {model}")
        
        default_model = config.get_default_model(provider)
        print(f"  🎯 기본 모델: {default_model}")
        print()

if __name__ == "__main__":
    test_llm_providers()
    test_model_configs() 