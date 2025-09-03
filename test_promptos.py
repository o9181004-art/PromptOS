import pandas as pd
from intent_classifier import classify_intent
from prompt_generator import extract_conditions
from prompt_builder import get_template, extract_placeholders, fill_template

# 테스트용 발화 파일 경로
csv_path = "promptos_utterance_examples_100.csv"  # 같은 폴더에 둘 경우
df = pd.read_csv(csv_path)

results = []

for _, row in df.iterrows():
    utterance = row["utterance"]
    result = {"utterance": utterance}

    # 의도 분류
    intent = classify_intent(utterance)
    result["intent"] = intent

    # 템플릿 로딩
    template = get_template(intent)
    result["template_found"] = "✅" if template else "❌"

    # 조건 추출
    conditions = extract_conditions(utterance)
    result.update(conditions)

    # placeholder 처리
    if template:
        placeholders = extract_placeholders(template)
        values = {**conditions}
        missing = [ph for ph in placeholders if ph not in values]
        result["placeholders_filled"] = "✅" if not missing else f"❌ ({', '.join(missing)})"
    else:
        result["placeholders_filled"] = "-"

    results.append(result)

# 결과 저장
df_result = pd.DataFrame(results)
df_result.to_csv("promptos_test_result_100.csv", index=False, encoding="utf-8-sig")
print("✅ 테스트 완료: promptos_test_result_100.csv 저장됨")
