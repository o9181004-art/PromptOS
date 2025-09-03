# config.py
"""
PromptOS 설정 관리 모듈

이 파일은 LLM API 키와 기본 설정을 관리합니다.
API 키는 .env 파일에서 로드되며, 보안을 위해 직접 코드에 하드코딩하지 않습니다.

.env 파일 예시:
OPENROUTER_API_KEY = "sk-xxxxx"
GROQ_API_KEY = "gsk-xxxxx"
TOGETHER_API_KEY = "tga-xxxxx"
DEFAULT_LLM_PROVIDER = "openrouter"
DEFAULT_LLM_MODEL = "meta-llama/llama-3-8b-instruct"
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    애플리케이션 설정 관리
    """
    
    def __init__(self):
        # LLM 제공업체 설정
        self.default_llm_provider = os.getenv('DEFAULT_LLM_PROVIDER', 'openrouter')
        self.default_llm_model = os.getenv('DEFAULT_LLM_MODEL', 'meta-llama/llama-3-8b-instruct')
        
        # API 키 설정 (보안을 위해 .env 파일에서 로드)
        # OpenRouter API 키: https://openrouter.ai/
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        # Groq API 키: https://console.groq.com/
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        # Together AI API 키: https://together.ai/
        self.together_api_key = os.getenv('TOGETHER_API_KEY')
        
        # 모델별 기본 설정
        self.model_configs = {
            "openrouter": {
                "default_model": "meta-llama/llama-3-8b-instruct",
                "available_models": [
                    "meta-llama/llama-3-8b-instruct",
                    "meta-llama/llama-3-70b-instruct",
                    "anthropic/claude-3-haiku",
                    "anthropic/claude-3-sonnet",
                    "openai/gpt-4o-mini",
                    "openai/gpt-4o"
                ]
            },
            "groq": {
                "default_model": "llama3-8b-8192",
                "available_models": [
                    "llama3-8b-8192",
                    "llama3-70b-8192",
                    "mixtral-8x7b-32768",
                    "gemma2-9b-it"
                ]
            },
            "together": {
                "default_model": "meta-llama/Llama-3-8b-chat-hf",
                "available_models": [
                    "meta-llama/Llama-3-8b-chat-hf",
                    "meta-llama/Llama-3-70b-chat-hf",
                    "microsoft/DialoGPT-medium",
                    "google/flan-t5-xxl"
                ]
            }
        }
    
    def get_default_provider(self) -> str:
        """기본 LLM 제공업체를 반환합니다."""
        return self.default_llm_provider
    
    def get_default_model(self, provider: str = None) -> str:
        """기본 모델을 반환합니다."""
        provider = provider or self.default_llm_provider
        return self.model_configs.get(provider, {}).get("default_model", self.default_llm_model)
    
    def get_available_models(self, provider: str) -> list:
        """지정된 제공업체의 사용 가능한 모델 목록을 반환합니다."""
        return self.model_configs.get(provider, {}).get("available_models", [])
    
    def is_provider_available(self, provider: str) -> bool:
        """지정된 제공업체가 사용 가능한지 확인합니다."""
        if provider == "openrouter":
            return bool(self.openrouter_api_key)
        elif provider == "groq":
            return bool(self.groq_api_key)
        elif provider == "together":
            return bool(self.together_api_key)
        return False
    
    def get_available_providers(self) -> Dict[str, bool]:
        """사용 가능한 모든 제공업체 목록을 반환합니다."""
        return {
            "openrouter": self.is_provider_available("openrouter"),
            "groq": self.is_provider_available("groq"),
            "together": self.is_provider_available("together")
        }
    
    def set_default_provider(self, provider: str):
        """기본 제공업체를 설정합니다."""
        if provider in ["openrouter", "groq", "together"]:
            self.default_llm_provider = provider
        else:
            raise ValueError(f"지원하지 않는 제공업체입니다: {provider}")
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """API 키 유효성을 검증합니다."""
        validation_results = {}
        
        # OpenRouter API 키 검증
        if self.openrouter_api_key:
            if self.openrouter_api_key.startswith("sk-"):
                validation_results["openrouter"] = True
            else:
                validation_results["openrouter"] = False
        else:
            validation_results["openrouter"] = False
        
        # Groq API 키 검증
        if self.groq_api_key:
            if self.groq_api_key.startswith("gsk_"):
                validation_results["groq"] = True
            else:
                validation_results["groq"] = False
        else:
            validation_results["groq"] = False
        
        # Together AI API 키 검증
        if self.together_api_key:
            if self.together_api_key.startswith("tga_"):
                validation_results["together"] = True
            else:
                validation_results["together"] = False
        else:
            validation_results["together"] = False
        
        return validation_results
    
    def get_api_key_info(self) -> Dict[str, str]:
        """API 키 정보를 반환합니다 (보안을 위해 마스킹 처리)."""
        info = {}
        
        if self.openrouter_api_key:
            info["openrouter"] = f"{self.openrouter_api_key[:8]}...{self.openrouter_api_key[-4:]}"
        else:
            info["openrouter"] = "Not set"
        
        if self.groq_api_key:
            info["groq"] = f"{self.groq_api_key[:8]}...{self.groq_api_key[-4:]}"
        else:
            info["groq"] = "Not set"
        
        if self.together_api_key:
            info["together"] = f"{self.together_api_key[:8]}...{self.together_api_key[-4:]}"
        else:
            info["together"] = "Not set"
        
        return info

# 전역 설정 인스턴스
config = Config() 