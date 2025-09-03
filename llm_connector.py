import os
import requests
import json
from typing import Optional

def call_llm_openrouter(prompt: str, model: str = "openai/gpt-3.5-turbo") -> str:
    """
    OpenRouter API를 사용하여 LLM을 호출합니다.
    
    Args:
        prompt (str): LLM에 전달할 프롬프트
        model (str): 사용할 모델명 (기본값: openai/gpt-3.5-turbo)
        
    Returns:
        str: LLM 응답
    """
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://promptos.app",
        "X-Title": "PromptOS"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")
        return "unknown"
    except (KeyError, IndexError) as e:
        print(f"응답 파싱 오류: {e}")
        return "unknown"
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return "unknown" 