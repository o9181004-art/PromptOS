# fallback_manager.py

from llm_api import call_llm_openrouter
from domain_inference import domain_inference
from naming_dict import naming_dict
from keyword_classifier import keyword_classifier

class FallbackManager:
    """
    템플릿이 없을 때 LLM에게 직접 프롬프트를 생성하도록 하는 관리자
    """
    
    def __init__(self):
        self.system_prompt = """당신은 사용자의 요청에 맞는 고품질 프롬프트를 생성하는 전문가입니다.

사용자의 요청을 분석하여 다음과 같은 요소들을 포함한 완성된 프롬프트를 생성해주세요:

1. **명확한 목적**: 사용자가 원하는 작업의 목적
2. **구체적인 지시사항**: 어떻게 작업을 수행할지에 대한 상세한 가이드
3. **출력 형식**: 원하는 결과물의 형태나 구조
4. **제약 조건**: 특별히 고려해야 할 사항이나 제한사항
5. **어조와 스타일**: 적절한 톤과 작성 스타일

프롬프트는 다음 원칙을 따라야 합니다:
- 명확하고 구체적이어야 함
- 실행 가능한 지시사항을 포함해야 함
- 사용자의 의도를 정확히 반영해야 함
- 전문적이면서도 이해하기 쉬워야 함
- 명령형 문장으로 시작하고, 목적과 결과가 분명히 드러나게 구성

사용자의 요청에 맞는 완성된 프롬프트만 생성해주세요. 추가 설명이나 메타데이터는 포함하지 마세요."""

    def generate_prompt_with_llm(self, utterance: str, intent: str = None, domain: str = None, audience: str = None) -> str:
        """
        LLM을 사용하여 사용자 발화로부터 직접 프롬프트를 생성합니다.
        
        Args:
            utterance (str): 사용자 발화
            intent (str): 분류된 의도 (선택사항)
            domain (str): 추론된 도메인 (선택사항)
            audience (str): 대상 청중 (선택사항)
            
        Returns:
            str: LLM이 생성한 프롬프트
        """
        # 도메인 정보 추론
        inferred_domain, domain_confidence, domain_info = domain_inference.infer_domain(utterance)
        domain_context = domain_inference.get_domain_context(inferred_domain)
        
        # 고유명사 정보 추론
        entity = naming_dict.get_best_mapping(utterance)
        entity_context = {}
        if entity:
            entity_context = naming_dict.get_context_info(entity)
        
        # User 메시지 구성
        if intent and intent != "unknown":
            user_message = f"""사용자가 요청한 작업에 맞는 프롬프트를 생성해줘: '{utterance}'

분류된 의도: {intent}
추론된 도메인: {inferred_domain} (신뢰도: {domain_confidence:.2f})
대상 청중: {domain_context.get('audience', '일반 사용자')}
적합한 톤: {domain_context.get('tone', '중립적')}
중점 사항: {domain_context.get('focus', '일반적인 목적')}"""

            # 고유명사 정보가 있으면 추가
            if entity_context:
                user_message += f"""

고유명사 정보:
- 발견된 고유명사: {entity_context.get('name', 'N/A')}
- 설명: {entity_context.get('description', 'N/A')}
- 권장 의도: {entity_context.get('intent', 'N/A')}
- 권장 도메인: {entity_context.get('domain', 'N/A')}
- 대상 청중: {entity_context.get('target', 'N/A')}
- 권장 톤: {entity_context.get('tone', 'N/A')}"""

            user_message += """

명령형 문장으로 시작하고, 목적과 결과가 분명히 드러나게 구성해줘.
도메인 특성과 고유명사 정보를 고려하여 전문적이고 적절한 프롬프트를 생성해주세요."""
        else:
            user_message = f"""사용자가 요청한 작업에 맞는 프롬프트를 생성해줘: '{utterance}'

추론된 도메인: {inferred_domain} (신뢰도: {domain_confidence:.2f})
대상 청중: {domain_context.get('audience', '일반 사용자')}
적합한 톤: {domain_context.get('tone', '중립적')}
중점 사항: {domain_context.get('focus', '일반적인 목적')}"""

            # 고유명사 정보가 있으면 추가
            if entity_context:
                user_message += f"""

고유명사 정보:
- 발견된 고유명사: {entity_context.get('name', 'N/A')}
- 설명: {entity_context.get('description', 'N/A')}
- 권장 의도: {entity_context.get('intent', 'N/A')}
- 권장 도메인: {entity_context.get('domain', 'N/A')}
- 대상 청중: {entity_context.get('target', 'N/A')}
- 권장 톤: {entity_context.get('tone', 'N/A')}"""

            user_message += """

명령형 문장으로 시작하고, 목적과 결과가 분명히 드러나게 구성해줘.
도메인 특성과 고유명사 정보를 고려하여 전문적이고 적절한 프롬프트를 생성해주세요."""
        
        # 전체 프롬프트 구성
        full_prompt = f"{self.system_prompt}\n\n{user_message}"
        
        try:
            # LLM 호출
            generated_prompt = call_llm_openrouter(full_prompt)
            
            # 프롬프트 검증 및 수정
            validated_prompt = self._validate_and_fix_prompt(generated_prompt.strip())
            
            return validated_prompt
            
        except Exception as e:
            print(f"❌ LLM 프롬프트 생성 실패: {e}")
            return self._generate_fallback_prompt(utterance)
    
    def generate_helpful_message(self, utterance: str) -> str:
        """
        LLM 생성이 실패했을 때 사용자 친화적인 도움 메시지를 생성합니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            str: 도움 메시지
        """
        # fallback 키워드 제안 가져오기
        suggestions = keyword_classifier.get_fallback_suggestions(utterance)
        
        if suggestions:
            suggestion_text = ", ".join(suggestions[:3])  # 상위 3개만 표시
            return f"입력하신 내용을 이해하지 못했어요. '{suggestion_text}'와 같은 구체적 표현을 사용해보세요."
        else:
            return "입력하신 내용을 이해하지 못했어요. '사업계획서', '지원서', '제안서'와 같은 구체적 표현을 사용해보세요."
    
    def _validate_and_fix_prompt(self, prompt: str) -> str:
        """
        생성된 프롬프트를 검증하고 수정합니다.
        
        Args:
            prompt: 원본 프롬프트
            
        Returns:
            str: 검증 및 수정된 프롬프트
        """
        if not prompt or len(prompt.strip()) < 10:
            return self.generate_helpful_message("")
        
        # JSON 형식 검증 및 수정
        if "{" in prompt and "}" in prompt:
            try:
                # JSON 형식이 올바른지 확인
                import json
                # JSON 부분만 추출하여 검증
                start = prompt.find("{")
                end = prompt.rfind("}") + 1
                if start != -1 and end != 0:
                    json_part = prompt[start:end]
                    json.loads(json_part)  # JSON 검증
            except json.JSONDecodeError:
                # JSON 형식이 잘못된 경우 일반 텍스트로 변환
                prompt = prompt.replace("{", "").replace("}", "")
        
        # 플레이스홀더 검증 및 수정
        placeholders = ["{placeholder}", "{slot}", "{variable}", "{field}"]
        for placeholder in placeholders:
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, "N/A")
        
        # 마크다운 형식 검증
        if prompt.startswith("#") and not prompt.startswith("##"):
            prompt = "## " + prompt[1:]  # 단일 #을 ##으로 변경
        
        return prompt.strip()
    
    def _generate_fallback_prompt(self, utterance: str) -> str:
        """
        LLM 호출이 실패했을 때 사용하는 기본 프롬프트 생성
        """
        return f"""사용자가 요청한 작업에 맞는 프롬프트를 생성해줘: '{utterance}'

명령형 문장으로 시작하고, 목적과 결과가 분명히 드러나게 구성해줘."""

# 전역 인스턴스 생성
fallback_manager = FallbackManager() 