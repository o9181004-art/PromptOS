import re
import os
from prompt_generator import generate_followup_question

# 템플릿 파일 로딩 디렉토리
TEMPLATE_DIR = "templates"

def extract_placeholders(template):
    """
    템플릿에서 {placeholder} 형태의 키워드를 추출합니다.
    """
    return re.findall(r"{(.*?)}", template)

def prompt_missing_values(placeholders):
    """
    누락된 placeholder 항목에 대해 GPT가 질문을 생성하고, 사용자 입력을 받아 반환합니다.
    """
    values = {}
    for ph in placeholders:
        try:
            question = generate_followup_question(ph)
        except Exception:
            question = f"💬 '{ph}' 값을 입력해주세요."
        print(f"❓ {question}")
        user_input = input("📝 입력: ").strip()
        values[ph] = user_input
    return values

def fill_template(template, values):
    """
    입력받은 값들을 템플릿에 삽입하여 최종 프롬프트를 완성합니다.
    """
    try:
        return template.format(**values)
    except KeyError as e:
        missing_key = e.args[0]
        return f"⚠️ Missing value for: {missing_key}"

def get_template(intent):
    """
    템플릿 디렉토리에서 intent에 해당하는 텍스트 파일을 불러옵니다.
    예: intent가 'summary'이면 'templates/summary.txt'를 로드
    """
    filename = os.path.join(TEMPLATE_DIR, f"{intent}.txt")
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return None
