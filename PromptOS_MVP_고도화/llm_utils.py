# llm_utils.py
import os
import requests

def classify_intent_llm(utterance, model="meta-llama/llama-3-8b-instruct"):
    import os
    import requests

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    system_msg = (
        "You are a helpful AI that classifies user instructions into one of the following intents:\n"
        "- summary\n"
        "- self_intro\n"
        "- customer_reply\n\n"
        "Respond ONLY with one of these intent names. Do not add explanations."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": utterance}
        ]
    }

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        result = res.json()["choices"][0]["message"]["content"].strip().lower()
        # 방어적 처리: 의도 외 값이 오면 unknown으로
        if result in ["summary", "self_intro", "customer_reply"]:
            return result
        else:
            return "unknown"
    else:
        return "unknown"

