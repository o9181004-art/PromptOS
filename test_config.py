#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Config 설정 테스트 스크립트
"""

from config import config

def test_config():
    """Config 설정을 테스트합니다."""
    
    print("🧪 Config 설정 테스트 시작\n")
    
    # 1. 기본 설정 확인
    print("📋 기본 설정:")
    print(f"  기본 제공업체: {config.get_default_provider()}")
    print(f"  기본 모델: {config.get_default_model()}")
    print()
    
    # 2. 사용 가능한 제공업체 확인
    print("🔑 사용 가능한 제공업체:")
    available_providers = config.get_available_providers()
    for provider, available in available_providers.items():
        status = "✅" if available else "❌"
        print(f"  {status} {provider}")
    print()
    
    # 3. API 키 정보 확인 (마스킹 처리)
    print("🔐 API 키 정보 (마스킹 처리):")
    api_key_info = config.get_api_key_info()
    for provider, info in api_key_info.items():
        print(f"  {provider}: {info}")
    print()
    
    # 4. API 키 유효성 검증
    print("✅ API 키 유효성 검증:")
    validation_results = config.validate_api_keys()
    for provider, is_valid in validation_results.items():
        status = "✅" if is_valid else "❌"
        print(f"  {status} {provider}")
    print()
    
    # 5. 각 제공업체별 사용 가능한 모델 확인
    print("🤖 사용 가능한 모델:")
    for provider in ["openrouter", "groq", "together"]:
        models = config.get_available_models(provider)
        print(f"  {provider}:")
        for model in models:
            print(f"    - {model}")
        print()
    
    # 6. 제공업체 변경 테스트
    print("🔄 제공업체 변경 테스트:")
    current_provider = config.get_default_provider()
    print(f"  현재 기본 제공업체: {current_provider}")
    
    # 다른 제공업체로 변경 시도
    for provider in ["groq", "together", "openrouter"]:
        if provider != current_provider:
            try:
                config.set_default_provider(provider)
                print(f"  ✅ {provider}로 변경 성공")
                break
            except ValueError as e:
                print(f"  ❌ {provider}로 변경 실패: {e}")
    
    # 원래 제공업체로 복원
    config.set_default_provider(current_provider)
    print(f"  🔄 원래 제공업체({current_provider})로 복원")
    print()
    
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    test_config() 