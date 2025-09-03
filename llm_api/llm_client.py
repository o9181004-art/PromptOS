# llm_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def call_llm_openrouter(prompt, model="meta-llama/llama-3-8b-instruct"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ API 호출 실패: {response.status_code} - {response.text}"
