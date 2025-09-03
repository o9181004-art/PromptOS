# ✅ Cursor Instruction Template System

## 📋 개요

Cursor Instruction Template System은 목적 기반 프롬프트 템플릿 시스템으로, 사용자의 의도를 정확히 파악하고 적절한 템플릿을 자동으로 선택하여 고품질의 프롬프트를 생성합니다.

## 🎯 주요 특징

### 1. **명시적 의도 vs 암묵적 의도 구분**
- **명시적 의도**: 키워드 기반 정확한 매칭 (신뢰도 0.8+)
- **암묵적 의도**: LLM 기반 추론 + 후속 질문 (신뢰도 0.3-0.7)

### 2. **다단계 분류 시스템**
1. **키워드 매칭** (가장 높은 우선순위)
2. **템플릿 유사도 매칭**
3. **LLM 기반 추론**
4. **Fallback 처리**

### 3. **신뢰도 기반 처리**
- **높은 신뢰도 (≥0.8)**: 명시적 템플릿 사용
- **중간 신뢰도 (0.5-0.8)**: 템플릿 + 추가 지시사항
- **낮은 신뢰도 (<0.5)**: Fallback + 후속 질문

## 🏗️ 시스템 구조

```
cursor_instruction_template_config.py  # 템플릿 설정
cursor_instruction_system.py           # 핵심 시스템
cursor_instruction_adapter.py          # 기존 시스템 연동
```

## 📁 파일 설명

### 1. `cursor_instruction_template_config.py`
템플릿과 설정을 정의하는 설정 파일

```python
TEMPLATES_BY_INTENT = {
    "biz_plan": {
        "title": "사업계획서 구성 템플릿",
        "description": "아이디어 또는 예비창업자의 발화를 기반으로 한 사업계획서 자동 생성 템플릿입니다.",
        "template": "다음 기준에 따라 사업계획서를 작성해주세요:\n\n📌 사업 개요\n- 비즈니스 모델과 핵심 가치 제안\n...",
        "output_language": "ko"
    },
    # ... 더 많은 템플릿들
}
```

### 2. `cursor_instruction_system.py`
핵심 분류 및 처리 로직

```python
class CursorInstructionSystem:
    def classify_intent(self, user_input: str) -> Tuple[str, float, str]:
        # 1. 명시적 의도 매칭
        # 2. 템플릿 기반 유사도 매칭
        # 3. LLM 기반 추론
        # 4. Fallback
```

### 3. `cursor_instruction_adapter.py`
기존 PromptOS 시스템과의 호환성 제공

```python
class CursorInstructionAdapter:
    def process_utterance(self, utterance: str, chat_history: Optional[list] = None) -> Dict[str, Any]:
        # 기존 시스템과 호환되는 인터페이스
```

## 🎯 지원하는 의도 (Intents)

| 의도 | 키워드 | 설명 |
|------|--------|------|
| `biz_plan` | 사업계획서, 비즈니스, 창업, 사업, 계획서 | 사업계획서 작성 |
| `ir_draft` | IR, 투자자, 투자, 펀딩, 자금조달 | 투자자용 IR 문서 |
| `marketing_copy` | 마케팅, 카피, 홍보, 광고, 프로모션 | 마케팅 카피 작성 |
| `self_intro` | 자기소개서, 소개, 이력서, 면접, 지원서 | 자기소개서 작성 |
| `customer_reply` | 고객, 응대, 문의, 답변, 상담 | 고객 응대 메시지 |
| `collab_email` | 협업, 제안, 이메일, 파트너십, 함께 | 협업 제안 이메일 |
| `proposal` | 제안서, 제안, 기획서, 안건, 계획 | 제안서 작성 |
| `meeting_summary` | 회의, 요약, 회의록, 논의, 결정 | 회의 요약서 |
| `summary` | 요약, 정리, 핵심, 요점, 간단히 | 일반 요약문 |
| `code_run` | 코드, 프로그램, 실행, 개발, 디버깅 | 코드 실행 및 분석 |

## 🚀 사용 방법

### 1. 기본 사용법

```python
from cursor_instruction_system import cursor_system

# 사용자 입력 처리
result = cursor_system.process_user_input("사업계획서 써줘")

print(f"의도: {result['intent']}")
print(f"신뢰도: {result['confidence']:.2f}")
print(f"프롬프트: {result['prompt']}")
```

### 2. 어댑터 사용법 (기존 시스템 연동)

```python
from cursor_instruction_adapter import cursor_adapter

# 기존 시스템과 호환되는 인터페이스
result = cursor_adapter.process_utterance("마케팅 카피 써줘")

print(f"처리 방식: {result['processing_type']}")
print(f"템플릿 사용: {result['should_use_template']}")
```

### 3. 간단한 프롬프트 생성

```python
from cursor_instruction_adapter import get_cursor_prompt

prompt = get_cursor_prompt("면접용 자기소개서 작성 도와줘")
print(prompt)
```

## 📊 테스트 결과

### 포괄 테스트 결과 (12개 케이스)

- **✅ 높은 신뢰도 (≥0.8)**: 9개 (75%)
- **⚠️ 중간 신뢰도 (0.5-0.8)**: 1개 (8%)
- **❓ 낮은 신뢰도 (<0.5)**: 2개 (17%)

### 분류 방법별 통계

- **explicit_keyword_matching**: 9개 (75%)
- **llm_inference**: 3개 (25%)

## 🔧 설정 및 커스터마이징

### 1. 신뢰도 임계값 조정

```python
# cursor_instruction_template_config.py
CONFIDENCE_THRESHOLDS = {
    "high_confidence": 0.6,    # 높은 신뢰도 임계값
    "medium_confidence": 0.4,  # 중간 신뢰도 임계값
    "low_confidence": 0.3,     # 낮은 신뢰도 임계값
    "fallback_threshold": 0.2  # Fallback 임계값
}
```

### 2. 새로운 템플릿 추가

```python
# cursor_instruction_template_config.py
TEMPLATES_BY_INTENT["new_intent"] = {
    "title": "새로운 템플릿",
    "description": "새로운 템플릿 설명",
    "template": "템플릿 내용...",
    "output_language": "ko"
}

# cursor_instruction_system.py
def _build_intent_keywords(self):
    keywords = {
        # ... 기존 키워드들
        "new_intent": ["키워드1", "키워드2", "키워드3"]
    }
```

## 🎯 장점

### 1. **정확한 의도 분류**
- 키워드 기반 명시적 매칭으로 높은 정확도
- 다단계 분류 시스템으로 안정성 확보

### 2. **유연한 처리**
- 신뢰도에 따른 차별화된 처리
- Fallback 시스템으로 모든 케이스 커버

### 3. **기존 시스템 호환성**
- 어댑터 패턴으로 기존 시스템과 무缝 연동
- 점진적 도입 가능

### 4. **확장성**
- 새로운 템플릿 쉽게 추가 가능
- 설정 기반 커스터마이징

## 🔮 향후 개선 계획

1. **LLM 통합**: 실제 LLM API 연동으로 추론 정확도 향상
2. **컨텍스트 인식**: 대화 히스토리를 활용한 더 정확한 분류
3. **학습 기능**: 사용자 피드백을 통한 시스템 개선
4. **다국어 지원**: 영어, 일본어 등 추가 언어 지원

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

---

**✅ Cursor Instruction Template System** - 목적 기반 프롬프트 생성의 새로운 패러다임 