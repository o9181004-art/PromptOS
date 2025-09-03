import os
from template_mapper import template_mapper
from intent_similarity_classifier import similarity_classifier
from template_matcher import template_matcher
from keyword_classifier import keyword_classifier

def get_template(template_key: str, base_dir="templates", fallback="unknown", utterance: str = "") -> str:
    """
    템플릿 키에 따라 파일을 찾습니다. 중첩된 폴더가 있을 경우를 지원.
    예외적으로 self_intro 같은 키는 하위 폴더가 아님을 인지하여 처리.
    """
    # 직접 경로 확인
    direct_path = os.path.join(base_dir, f"{template_key}.txt")
    if os.path.isfile(direct_path):
        with open(direct_path, "r", encoding="utf-8") as f:
            return f.read()

    # 계층적 경로 시도 (proposal_ai_ai → templates/proposal/ai/ai.txt)
    relative_path = template_key.replace("_", os.sep) + ".txt"
    nested_path = os.path.join(base_dir, relative_path)
    if os.path.isfile(nested_path):
        with open(nested_path, "r", encoding="utf-8") as f:
            return f.read()

    # intent가 unknown인 경우 템플릿 이름 매칭 시도
    if template_key == "unknown" and utterance:
        print("🔍 unknown intent: 템플릿 이름 매칭 시도...")
        
        # 1단계: 템플릿 이름 기반 매칭
        matched_template = template_matcher.match_template_by_name(utterance, threshold=0.6)
        if matched_template:
            print(f"✅ 템플릿 이름 매칭 성공: {matched_template}")
            return _load_template_file(matched_template, base_dir)
        
        # 2단계: 유사도 기반 템플릿 매칭
        print("🔍 템플릿 이름 매칭 실패, 유사도 기반 매칭 시도...")
        template_content = _get_template_by_similarity(utterance, base_dir)
        
        if template_content:
            return template_content
        
        # 3단계: fallback 키워드 기반 템플릿 선택
        print("🔍 유사도 기반 매칭 실패, fallback 키워드 기반 템플릿 선택...")
        fallback_intent, fallback_confidence = keyword_classifier.classify_fallback_keywords(utterance)
        
        if fallback_confidence > 0.3:
            print(f"✅ fallback 키워드 기반 템플릿 선택: {fallback_intent}")
            # fallback intent에 맞는 템플릿 찾기
            fallback_template = _get_fallback_template_by_intent(fallback_intent, base_dir)
            if fallback_template:
                return fallback_template
        
        # 4단계: 기본 unknown 템플릿 사용
        print("🔍 모든 매칭 실패, 기본 unknown 템플릿 사용...")
        return _load_template_file("unknown.txt", base_dir)
    
    # 일반적인 fallback
    fallback_path = os.path.join(base_dir, f"{fallback}.txt")
    if os.path.isfile(fallback_path):
        with open(fallback_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""

def _get_fallback_template_by_intent(intent: str, base_dir: str) -> str:
    """
    fallback intent에 맞는 템플릿을 찾습니다.
    
    Args:
        intent: fallback intent
        base_dir: 기본 디렉토리
        
    Returns:
        str: 찾은 템플릿 내용 또는 빈 문자열
    """
    # intent별 템플릿 매핑
    intent_template_mapping = {
        "business_plan": [
            "business_plan.txt",
            "proposal/ai/ai.txt",
            "proposal/ai/government.txt",
            "proposal/ai/private.txt", 
            "proposal/climate.txt"
        ],
        "general_request": [
            "unknown.txt",
            "summary.txt",
            "self_intro.txt"
        ]
    }
    
    templates = intent_template_mapping.get(intent, ["unknown.txt"])
    
    for template_name in templates:
        template_content = _load_template_file(template_name, base_dir)
        if template_content:
            print(f"✅ fallback 템플릿 로딩 성공: {template_name}")
            return template_content
    
    return ""

def _get_template_by_similarity(utterance: str, base_dir: str) -> str:
    """
    유사도 기반으로 템플릿을 찾습니다.
    
    Args:
        utterance: 사용자 발화
        base_dir: 템플릿 기본 디렉토리
        
    Returns:
        str: 찾은 템플릿 내용 또는 빈 문자열
    """
    try:
        # 유사한 intent들의 템플릿들 찾기
        similar_templates = template_mapper.get_similar_intent_templates(utterance, top_k=3)
        
        print(f"🔍 유사한 intent 템플릿들: {similar_templates}")
        
        # 각 템플릿을 시도해보기
        for intent, similarity, template_name in similar_templates:
            print(f"📋 시도 중: {intent} (유사도: {similarity:.3f}) → {template_name}")
            
            # 템플릿 파일 로드 시도
            template_content = _load_template_file(template_name, base_dir)
            if template_content:
                print(f"✅ 유사도 기반 템플릿 찾음: {template_name} (유사도: {similarity:.3f})")
                return template_content
        
        # 유사한 템플릿도 없으면 fallback 템플릿 사용
        print("❌ 유사한 템플릿을 찾을 수 없음. Fallback 템플릿 사용...")
        fallback_template = template_mapper.get_fallback_template(utterance)
        return _load_template_file(fallback_template, base_dir)
        
    except Exception as e:
        print(f"❌ 유사도 기반 템플릿 검색 실패: {e}")
        return ""

def _load_template_file(template_name: str, base_dir: str) -> str:
    """
    템플릿 파일을 로드합니다.
    
    Args:
        template_name: 템플릿 파일명
        base_dir: 기본 디렉토리
        
    Returns:
        str: 템플릿 내용 또는 빈 문자열
    """
    # 직접 경로 확인
    direct_path = os.path.join(base_dir, template_name)
    if os.path.isfile(direct_path):
        with open(direct_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # .txt 확장자 추가 시도
    txt_path = os.path.join(base_dir, f"{template_name}.txt")
    if os.path.isfile(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    
    return ""
