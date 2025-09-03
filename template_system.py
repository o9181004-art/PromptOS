"""
새로운 템플릿 시스템
간단하고 직관적인 딕셔너리 기반 템플릿 관리
"""

templates = {
    "사업계획서 작성": """사용자가 {utterance}를 작성하고자 합니다.

다음 구조에 따라 체계적으로 작성해주세요:

📌 사업 개요
- 비즈니스 모델과 핵심 가치 제안
- 사업의 목적과 비전

📊 시장 분석  
- 시장 현황과 규모
- 경쟁사 분석과 차별화 포인트

🍽️ 서비스 설명
- 핵심 제품/서비스 상세 설명
- 고객 가치와 혜택

📈 실행 계획
- 마케팅 전략과 운영 계획
- 재무 계획과 수익 모델

각 섹션은 명확한 제목과 함께 구체적이고 실용적인 내용으로 작성해주세요.""",

    "이메일 작성": """사용자가 {utterance}를 작성하고자 합니다.

다음 구조에 따라 전문적이고 정중한 톤으로 작성해주세요:

📧 이메일 제목
- 명확하고 간결한 제목

👋 인사말
- 적절한 경칭과 인사말

📝 본문 내용
- 핵심 메시지를 명확하게 전달
- 논리적이고 체계적인 구성

🙏 마무리
- 정중한 마무리 인사와 서명

전문적이면서도 친근한 톤을 유지해주세요.""",

    "보고서 작성": """사용자가 {utterance}를 작성하고자 합니다.

다음 구조에 따라 객관적이고 체계적으로 작성해주세요:

📋 보고서 개요
- 핵심 내용 요약과 목적

📊 주요 내용
- 상세한 분석과 데이터
- 객관적 사실과 근거

📈 분석 결과
- 결과 해석과 인사이트
- 데이터 기반 결론

💡 결론 및 제안
- 핵심 결론과 향후 방향
- 구체적인 제안사항

논리적이고 객관적인 톤으로 작성해주세요.""",

    "설명문 작성": """사용자가 {utterance}를 작성하고자 합니다.

다음 구조에 따라 이해하기 쉽고 명확하게 설명해주세요:

📖 개요 설명
- 기본 개념과 배경

🔍 상세 설명
- 구체적이고 자세한 내용
- 예시와 함께 설명

💡 핵심 포인트
- 중요한 점과 주의사항
- 실용적인 팁

📝 요약
- 핵심 내용 정리

비전문가도 이해할 수 있도록 쉽고 명확하게 작성해주세요.""",

    "고객 응대": """사용자가 {utterance}를 처리하고자 합니다.

다음 구조에 따라 친절하고 전문적으로 응답해주세요:

👋 인사말
- 정중하고 친근한 인사

📝 응답 내용
- 고객 문의에 대한 명확한 답변
- 구체적인 정보 제공

💡 해결 방안
- 실질적인 해결책 제시
- 추가 조치사항 안내

🙏 마무리
- 정중한 마무리와 추가 문의 안내

고객 중심적이고 해결책을 제시하는 톤으로 작성해주세요.""",

    "홍보문구": """사용자가 {utterance}를 작성하고자 합니다.

다음 구조에 따라 매력적이고 설득력 있게 작성해주세요:

🎯 핵심 메시지
- 브랜드/제품의 핵심 가치
- 타겟 고객에게 전달할 메시지

✨ 제품/서비스 특징
- 주요 특징과 장점
- 경쟁사 대비 차별화 포인트

📢 홍보 문구
- 매력적이고 기억에 남는 문구
- 행동 유도 요소 포함

💡 활용 방안
- 다양한 채널별 활용 방법
- 효과적인 전략 제안

창의적이고 설득력 있는 톤으로 작성해주세요.""",

    "계획 수립": """사용자가 {utterance}를 수립하고자 합니다.

다음 구조에 따라 구체적이고 실현 가능한 계획을 제시해주세요:

📋 계획 개요
- 목표와 범위 정의
- 전체적인 방향성

📅 세부 일정
- 단계별 일정과 마일스톤
- 우선순위와 의존관계

🎯 주요 목표
- 구체적이고 측정 가능한 목표
- 성과 지표 설정

📊 실행 방안
- 구체적인 실행 방법
- 필요한 리소스와 예산

실용적이고 실행 가능한 계획으로 작성해주세요.""",

    "요약 요청": """사용자가 {utterance}를 요약하고자 합니다.

다음 구조에 따라 핵심 내용을 간결하게 정리해주세요:

📝 원문 요약
- 핵심 내용의 간결한 요약
- 주요 포인트 정리

💡 주요 포인트
- 중요한 정보와 인사이트
- 핵심 결론

📊 분석 결과
- 요약 내용의 의미와 함의
- 추가 고려사항

간결하면서도 핵심을 놓치지 않도록 작성해주세요."""
}

def get_template(intent: str) -> str:
    """
    의도에 따른 템플릿을 반환합니다.
    
    Args:
        intent (str): 의도 분류 결과
        
    Returns:
        str: 해당 의도의 템플릿 또는 기본 템플릿
    """
    return templates.get(intent, "사용자의 요청을 이해하지 못했지만, 다음과 같은 요청을 기반으로 기본 응답을 생성합니다: {utterance}")

def fill_template(template: str, utterance: str) -> str:
    """
    템플릿의 플레이스홀더를 실제 값으로 채웁니다.
    
    Args:
        template (str): 템플릿 문자열
        utterance (str): 사용자 발화
        
    Returns:
        str: 채워진 템플릿
    """
    try:
        return template.format(utterance=utterance)
    except Exception as e:
        print(f"템플릿 채우기 오류: {e}")
        return f"사용자 요청에 대한 응답을 생성합니다: {utterance}"

def build_prompt(intent: str, utterance: str, conditions: dict = None) -> str:
    """
    의도와 사용자 발화를 기반으로 프롬프트를 생성합니다.
    
    Args:
        intent (str): 의도 분류 결과
        utterance (str): 사용자 발화
        conditions (dict): 추가 조건 (선택사항)
        
    Returns:
        str: 생성된 프롬프트
    """
    try:
        # 프롬프트 정리: 따옴표 정규화 및 공백 제거
        cleaned_utterance = utterance.replace(""", "\"").replace(""", "\"").strip()
        
        template = get_template(intent)
        if "{utterance}" in template:
            return template.format(utterance=cleaned_utterance)
        else:
            return template
    except Exception as e:
        return f"⚠️ 입력을 이해하지 못했습니다. 사용자의 입력: {utterance}"

def run_final_llm_response(prompt_text: str, model: str = "openai/gpt-3.5-turbo") -> str:
    """
    생성된 프롬프트를 OpenRouter API로 전송하여 LLM 응답을 받아옵니다.
    
    Args:
        prompt_text (str): 생성된 프롬프트 텍스트
        model (str): 사용할 LLM 모델 (기본값: gpt-3.5-turbo)
        
    Returns:
        str: LLM 응답 텍스트 또는 오류 메시지
    """
    import os
    import requests
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    def make_llm_call(prompt: str, is_retry: bool = False) -> str:
        """실제 LLM API 호출을 수행하는 내부 함수"""
        try:
            # API 키 확인
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if not api_key:
                return "❌ OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다."
            
            # API 요청 헤더
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://promptos.app",
                "X-Title": "PromptOS"
            }
            
            # API 요청 페이로드
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # 디버깅을 위한 로그
            logger.info(f"OpenRouter API 호출 시작 (재시도: {is_retry})")
            logger.info(f"모델: {model}")
            logger.info(f"프롬프트 길이: {len(prompt)}")
            logger.info(f"프롬프트 내용: {prompt[:200]}...")
            
            # API 호출
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions", 
                headers=headers, 
                json=payload,
                timeout=30
            )
            
            # 응답 확인
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    response_content = result['choices'][0]['message']['content'].strip()
                    logger.info(f"LLM 응답 성공 (길이: {len(response_content)})")
                    return response_content
                else:
                    logger.error("LLM 응답 형식이 올바르지 않음")
                    return "❌ LLM 응답 형식이 올바르지 않습니다."
            else:
                logger.error(f"API 호출 실패: {response.status_code} - {response.text}")
                return f"❌ API 호출 실패: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            logger.error("API 호출 시간 초과")
            return "❌ API 호출 시간 초과 (30초)"
        except requests.exceptions.RequestException as e:
            logger.error(f"네트워크 오류: {str(e)}")
            return f"❌ 네트워크 오류: {str(e)}"
        except json.JSONDecodeError:
            logger.error("API 응답 JSON 파싱 실패")
            return "❌ API 응답을 JSON으로 파싱할 수 없습니다."
        except Exception as e:
            logger.error(f"예상치 못한 오류: {str(e)}")
            return f"❌ 예상치 못한 오류: {str(e)}"
    
    # 첫 번째 시도
    logger.info("LLM 응답 생성 시작")
    response = make_llm_call(prompt_text, is_retry=False)
    
    # Fallback 로직: 응답이 이해할 수 없다는 내용이면 재시도
    if response and any(keyword in response.lower() for keyword in [
        "cannot understand", "don't understand", "not clear", "unclear",
        "이해할 수 없", "명확하지 않", "알 수 없", "❌", "오류", "AI가 요청을 이해하지 못했습니다"
    ]):
        logger.info("LLM이 요청을 이해하지 못함. 구조화된 Fallback 프롬프트로 재시도 중...")
        
        # 구조화된 Fallback 프롬프트 정의
        fallback_prompts = {
            "사업계획서 작성": """정부 심사관에게 제출할 예비창업자 패키지용 사업계획서를 항목별로 작성해주세요.

다음 항목을 포함하여 격식 있는 한글 보고서 형식으로 작성해주세요:

📌 사업 개요
- 비즈니스 모델과 핵심 가치 제안
- 사업의 목적과 비전

📊 시장 분석  
- 시장 현황과 규모
- 경쟁사 분석과 차별화 포인트

🍽️ 서비스 설명
- 핵심 제품/서비스 상세 설명
- 고객 가치와 혜택

📈 실행 계획
- 마케팅 전략과 운영 계획
- 재무 계획과 수익 모델

💡 기대 효과
- 사업 성공 시 기대되는 효과
- 사회적/경제적 기여도

각 섹션은 명확한 제목과 함께 구체적이고 실용적인 내용으로 작성해주세요.""",
            
            "이메일 작성": """정중하고 전문적인 이메일을 작성해주세요.

다음 구조에 따라 격식 있는 한글 이메일 형식으로 작성해주세요:

📧 이메일 제목
- 명확하고 간결한 제목

👋 인사말
- 적절한 경칭과 인사말

📝 본문 내용
- 핵심 메시지를 명확하게 전달
- 논리적이고 체계적인 구성

🙏 마무리
- 정중한 마무리 인사와 서명

전문적이면서도 친근한 톤을 유지해주세요.""",
            
            "보고서 작성": """구조적이고 객관적인 보고서를 작성해주세요.

다음 구조에 따라 격식 있는 한글 보고서 형식으로 작성해주세요:

📋 보고서 개요
- 핵심 내용 요약과 목적

📊 주요 내용
- 상세한 분석과 데이터
- 객관적 사실과 근거

📈 분석 결과
- 결과 해석과 인사이트
- 데이터 기반 결론

💡 결론 및 제안
- 핵심 결론과 향후 방향
- 구체적인 제안사항

논리적이고 객관적인 톤으로 작성해주세요.""",
            
            "설명문 작성": """비전문가가 이해할 수 있도록 간단하고 명확하게 설명해주세요.

다음 구조에 따라 격식 있는 한글 설명문 형식으로 작성해주세요:

📖 개요 설명
- 기본 개념과 배경

🔍 상세 설명
- 구체적이고 자세한 내용
- 예시와 함께 설명

💡 핵심 포인트
- 중요한 점과 주의사항
- 실용적인 팁

📝 요약
- 핵심 내용 정리

비전문가도 이해할 수 있도록 쉽고 명확하게 작성해주세요.""",
            
            "고객 응대": """고객의 문의에 친절하고 신속하게 응답해주세요.

다음 구조에 따라 격식 있는 한글 응답 형식으로 작성해주세요:

👋 인사말
- 정중하고 친근한 인사

📝 응답 내용
- 고객 문의에 대한 명확한 답변
- 구체적인 정보 제공

💡 해결 방안
- 실질적인 해결책 제시
- 추가 조치사항 안내

🙏 마무리
- 정중한 마무리와 추가 문의 안내

고객 중심적이고 해결책을 제시하는 톤으로 작성해주세요.""",
            
            "홍보문구": """매력적인 홍보 문구를 작성해주세요.

다음 구조에 따라 격식 있는 한글 홍보문 형식으로 작성해주세요:

🎯 핵심 메시지
- 브랜드/제품의 핵심 가치
- 타겟 고객에게 전달할 메시지

✨ 제품/서비스 특징
- 주요 특징과 장점
- 경쟁사 대비 차별화 포인트

📢 홍보 문구
- 매력적이고 기억에 남는 문구
- 행동 유도 요소 포함

💡 활용 방안
- 다양한 채널별 활용 방법
- 효과적인 전략 제안

창의적이고 설득력 있는 톤으로 작성해주세요.""",
            
            "계획 수립": """실현 가능한 계획을 수립해주세요.

다음 구조에 따라 격식 있는 한글 계획서 형식으로 작성해주세요:

📋 계획 개요
- 목표와 범위 정의
- 전체적인 방향성

📅 세부 일정
- 단계별 일정과 마일스톤
- 우선순위와 의존관계

🎯 주요 목표
- 구체적이고 측정 가능한 목표
- 성과 지표 설정

📊 실행 방안
- 구체적인 실행 방법
- 필요한 리소스와 예산

실용적이고 실행 가능한 계획으로 작성해주세요.""",
            
            "요약 요청": """핵심 내용을 간결하게 요약해주세요.

다음 구조에 따라 격식 있는 한글 요약문 형식으로 작성해주세요:

📝 원문 요약
- 핵심 내용의 간결한 요약
- 주요 포인트 정리

💡 주요 포인트
- 중요한 정보와 인사이트
- 핵심 결론

📊 분석 결과
- 요약 내용의 의미와 함의
- 추가 고려사항

간결하면서도 핵심을 놓치지 않도록 작성해주세요.""",
            
            "default": """사용자 요청에 대한 명확하고 구체적인 응답을 제공해주세요.

요청사항:
1. 사용자의 요청을 정확히 이해하고 적절한 응답을 제공하세요
2. 구체적이고 실용적인 내용으로 작성하세요
3. 한국어로 응답하세요
4. 구조화된 형태로 작성하세요
5. 격식 있는 한글 문서 형식으로 작성하세요"""
        }
        
        # 의도에 따른 fallback 프롬프트 선택
        intent_keywords = {
            "사업계획서": "사업계획서 작성",
            "이메일": "이메일 작성", 
            "보고서": "보고서 작성",
            "설명": "설명문 작성",
            "고객": "고객 응대",
            "홍보": "홍보문구",
            "계획": "계획 수립",
            "요약": "요약 요청"
        }
        
        fallback_prompt = fallback_prompts["default"]
        for keyword, intent in intent_keywords.items():
            if keyword in prompt_text:
                fallback_prompt = fallback_prompts.get(intent, fallback_prompts["default"])
                break
        
        logger.info(f"구조화된 Fallback 프롬프트 사용: {fallback_prompt[:100]}...")
        response = make_llm_call(fallback_prompt, is_retry=True)
        logger.info("LLM 구조화된 Fallback 재시도 완료")
    
    return response 