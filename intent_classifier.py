import re
from classify_intent import classify_intent as llm_classify_intent

def classify_intent(utterance: str) -> dict:
    """
    새로운 LLM 기반 의도 분류 시스템을 사용하여 의도를 분류합니다.
    
    Args:
        utterance (str): 분류할 사용자 발화
        
    Returns:
        dict: 분류된 의도 정보
    """
    utterance = utterance.lower().strip()

    result = {
        "intent": "unknown",
        "sub_intent": None,
        "domain": None,
        "audience": None
    }

    # LLM 기반 의도 분류
    llm_intent = llm_classify_intent(utterance)
    
    # 새로운 의도 매핑
    intent_mapping = {
        "사업계획서 작성": {
            "intent": "business_plan",
            "sub_intent": None,
            "domain": "business",
            "audience": "investors"
        },
        "이메일 작성": {
            "intent": "email",
            "sub_intent": None,
            "domain": "communication",
            "audience": "general"
        },
        "보고서 작성": {
            "intent": "report",
            "sub_intent": None,
            "domain": "business",
            "audience": "management"
        },
        "설명문 작성": {
            "intent": "explanation",
            "sub_intent": None,
            "domain": "education",
            "audience": "general"
        },
        "고객 응대": {
            "intent": "customer_service",
            "sub_intent": None,
            "domain": "service",
            "audience": "customers"
        },
        "홍보문구": {
            "intent": "marketing",
            "sub_intent": None,
            "domain": "marketing",
            "audience": "customers"
        },
        "계획 수립": {
            "intent": "planning",
            "sub_intent": None,
            "domain": "business",
            "audience": "management"
        },
        "요약 요청": {
            "intent": "summary",
            "sub_intent": None,
            "domain": "general",
            "audience": "general"
        }
    }
    
    if llm_intent in intent_mapping:
        result.update(intent_mapping[llm_intent])
    else:
        # 기존 키워드 기반 fallback
        result = _fallback_keyword_classification(utterance)
    
    return result

def _fallback_keyword_classification(utterance: str) -> dict:
    """
    키워드 기반 fallback 분류
    """
    result = {
        "intent": "unknown",
        "sub_intent": None,
        "domain": None,
        "audience": None
    }

    rules = [
        {
            "intent": "business_plan",
            "patterns": ["사업계획서", "비즈니스플랜", "창업", "스타트업"],
        },
        {
            "intent": "email",
            "patterns": ["이메일", "메일", "답장", "응답"],
        },
        {
            "intent": "report",
            "patterns": ["보고서", "리포트", "분석서"],
        },
        {
            "intent": "explanation",
            "patterns": ["설명", "안내", "가이드"],
        },
        {
            "intent": "customer_service",
            "patterns": ["고객", "클라이언트", "응대", "서비스"],
        },
        {
            "intent": "marketing",
            "patterns": ["홍보", "마케팅", "광고", "프로모션"],
        },
        {
            "intent": "planning",
            "patterns": ["계획", "전략", "로드맵"],
        },
        {
            "intent": "summary",
            "patterns": ["요약", "정리", "핵심"],
        }
    ]

    for rule in rules:
        for keyword in rule.get("patterns", []):
            if keyword in utterance:
                result["intent"] = rule["intent"]
                break

    return result

if __name__ == "__main__":
    print("=== 의도 분류 테스트 인터페이스 ===")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print()
    
    while True:
        try:
            user_input = input("사용자의 자연어 입력을 입력하세요: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("테스트를 종료합니다.")
                break
                
            if not user_input:
                print("입력이 비어있습니다. 다시 입력해주세요.")
                continue
                
            print(f"\n입력: {user_input}")
            predicted_intent = classify_intent(user_input)
            print(f"예측된 의도(intent): {predicted_intent}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n테스트를 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            print("다시 시도해주세요.")
