# PromptOS

PromptOS는 KT 믿음 2.0 모델 안에서 동작하는 프롬프트 엔진 모듈입니다.  
사용자가 입력한 문장을 최적화된 프롬프트로 변환하여, 모델이 더 정확한 결과를 낼 수 있도록 지원합니다.

---

## 주요 기능
- 단순 입력 → 구조화된 프롬프트 변환
- 템플릿 기반 자동화
- MVP 단계: 회의록 요약, 보고서 작성 등 기본 시연 가능

---

## 실행 방법
```bash
git clone https://github.com/o9181004-art/PromptOS.git
cd PromptOS
pip install -r requirements.txt
streamlit run app.py


사용 예시

입력
회의록 요약해줘

변환된 프롬프트
"회의록을 분석해 핵심 요약 3줄과 담당자별 Action Item을 표로 정리하세요."

출력 예시
회의 요약: …
Action Item: …