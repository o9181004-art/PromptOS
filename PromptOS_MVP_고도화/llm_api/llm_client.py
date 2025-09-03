# llm_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def call_llm_openrouter(system_prompt, user_prompt, model="meta-llama/llama-3-8b-instruct"):
    """
    OpenRouter LLM 호출 함수.
    system_prompt와 user_prompt 두 메시지를 구성하여 요청합니다.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ API 호출 실패: {response.status_code} - {response.text}"
