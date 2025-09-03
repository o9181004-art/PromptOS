# llm_api.py

import os
import requests
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from config import config

load_dotenv()

class LLMClient:
    """
    여러 LLM 제공업체를 지원하는 통합 클라이언트
    """
    
    def __init__(self):
        # API 키 로드
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.together_api_key = os.getenv('TOGETHER_API_KEY')
        
        # 기본 설정 (config에서 가져오기)
        self.default_provider = config.get_default_provider()
        self.default_model = config.get_default_model()
    
    def call_openrouter(self, prompt: str, model: str = None) -> str:
        """
        OpenRouter API를 호출합니다.
        
        Args:
            prompt (str): 프롬프트
            model (str): 모델명 (기본값: meta-llama/llama-3-8b-instruct)
            
        Returns:
            str: LLM 응답
        """
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY가 설정되지 않았습니다.")
        
        model = model or self.default_model
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"❌ OpenRouter API 호출 실패: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"❌ OpenRouter 응답 파싱 실패: {str(e)}"
    
    def call_groq(self, prompt: str, model: str = "llama3-8b-8192") -> str:
        """
        Groq API를 호출합니다.
        
        Args:
            prompt (str): 프롬프트
            model (str): 모델명 (기본값: llama3-8b-8192)
            
        Returns:
            str: LLM 응답
        """
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY가 설정되지 않았습니다.")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"❌ Groq API 호출 실패: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"❌ Groq 응답 파싱 실패: {str(e)}"
    
    def call_together(self, prompt: str, model: str = "meta-llama/Llama-3-8b-chat-hf") -> str:
        """
        Together AI API를 호출합니다.
        
        Args:
            prompt (str): 프롬프트
            model (str): 모델명 (기본값: meta-llama/Llama-3-8b-chat-hf)
            
        Returns:
            str: LLM 응답
        """
        if not self.together_api_key:
            raise ValueError("TOGETHER_API_KEY가 설정되지 않았습니다.")
        
        url = "https://api.together.xyz/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"❌ Together AI API 호출 실패: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"❌ Together AI 응답 파싱 실패: {str(e)}"
    
    def call_llm(self, prompt: str, provider: str = None, model: str = None) -> str:
        """
        지정된 제공업체의 LLM을 호출합니다.
        
        Args:
            prompt (str): 프롬프트
            provider (str): 제공업체 (openrouter, groq, together)
            model (str): 모델명
            
        Returns:
            str: LLM 응답
        """
        provider = provider or self.default_provider
        
        if provider == "openrouter":
            return self.call_openrouter(prompt, model)
        elif provider == "groq":
            return self.call_groq(prompt, model)
        elif provider == "together":
            return self.call_together(prompt, model)
        else:
            raise ValueError(f"지원하지 않는 제공업체입니다: {provider}")
    
    def set_default_provider(self, provider: str):
        """기본 제공업체를 설정합니다."""
        if provider in ["openrouter", "groq", "together"]:
            self.default_provider = provider
        else:
            raise ValueError(f"지원하지 않는 제공업체입니다: {provider}")
    
    def get_available_providers(self) -> Dict[str, bool]:
        """사용 가능한 제공업체 목록을 반환합니다."""
        return {
            "openrouter": bool(self.openrouter_api_key),
            "groq": bool(self.groq_api_key),
            "together": bool(self.together_api_key)
        }

# 전역 인스턴스 생성
llm_client = LLMClient()

# 기존 호환성을 위한 함수들
def call_llm_openrouter(prompt: str, model: str = "meta-llama/llama-3-8b-instruct") -> str:
    """OpenRouter API 호출 (기존 호환성)"""
    return llm_client.call_openrouter(prompt, model)

def call_llm_groq(prompt: str, model: str = "llama3-8b-8192") -> str:
    """Groq API 호출"""
    return llm_client.call_groq(prompt, model)

def call_llm_together(prompt: str, model: str = "meta-llama/Llama-3-8b-chat-hf") -> str:
    """Together AI API 호출"""
    return llm_client.call_together(prompt, model)

def call_llm(prompt: str, provider: str = None, model: str = None) -> str:
    """통합 LLM 호출 함수"""
    return llm_client.call_llm(prompt, provider, model) 