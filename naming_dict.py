#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
고유명사 기반 자동 매핑 시스템
"""

from typing import Dict, List, Optional, Tuple
import re

class NamingDictionary:
    """
    고유명사 기반 자동 매핑 시스템
    """
    
    def __init__(self):
        """초기화"""
        # 고유명사 사전 (이름 → 매핑 정보)
        self.naming_dict = {
            # 기술/플랫폼 관련
            "프롬프트OS": {
                "description": "프롬프트 기반 운영체제 또는 프롬프트 관리 시스템",
                "intent": "startup_pitch",
                "domain": "technology",
                "target": "기술 전문가, 개발자, 투자자",
                "tone": "혁신적이고 기술적",
                "keywords": ["프롬프트", "운영체제", "관리", "시스템", "AI", "자동화"],
                "related_intents": ["education_content", "marketing_copy", "grant_proposal"]
            },
            "ChatGPT": {
                "description": "OpenAI의 대화형 인공지능 모델",
                "intent": "education_content",
                "domain": "ai",
                "target": "AI 전문가, 교육자, 일반 사용자",
                "tone": "전문적이고 접근하기 쉬운",
                "keywords": ["AI", "챗봇", "대화", "인공지능", "자연어처리", "생성AI"],
                "related_intents": ["marketing_copy", "startup_pitch", "grant_proposal"]
            },
            "스마트시티": {
                "description": "ICT 기술을 활용한 지능형 도시",
                "intent": "policy_brief",
                "domain": "government",
                "target": "정부 관계자, 정책 입안자, 도시 계획가",
                "tone": "공식적이고 신뢰할 수 있는",
                "keywords": ["도시", "정책", "ICT", "지능형", "인프라", "디지털"],
                "related_intents": ["grant_proposal", "startup_pitch"]
            },
            "메타버스": {
                "description": "가상과 현실이 융합된 3차원 가상세계",
                "intent": "startup_pitch",
                "domain": "technology",
                "target": "기술 전문가, 투자자, 일반 사용자",
                "tone": "혁신적이고 미래지향적",
                "keywords": ["가상현실", "VR", "AR", "3D", "플랫폼", "소셜"],
                "related_intents": ["marketing_copy", "education_content"]
            },
            "핀테크": {
                "description": "금융과 기술의 결합",
                "intent": "startup_pitch",
                "domain": "finance",
                "target": "금융 전문가, 투자자, 스타트업",
                "tone": "전문적이고 신뢰할 수 있는",
                "keywords": ["금융", "기술", "결제", "뱅킹", "투자", "블록체인"],
                "related_intents": ["grant_proposal", "marketing_copy"]
            },
            "바이오": {
                "description": "생명공학 기술",
                "intent": "grant_proposal",
                "domain": "healthcare",
                "target": "의료진, 연구자, 투자자",
                "tone": "전문적이고 신뢰할 수 있는",
                "keywords": ["생명공학", "의료", "제약", "유전체", "진단", "치료"],
                "related_intents": ["startup_pitch", "education_content"]
            },
            
            # 기업/서비스 관련
            "구글": {
                "description": "글로벌 기술 기업",
                "intent": "marketing_copy",
                "domain": "technology",
                "target": "일반 사용자, 기업 고객",
                "tone": "친근하고 신뢰할 수 있는",
                "keywords": ["검색", "기술", "AI", "클라우드", "광고"],
                "related_intents": ["startup_pitch", "education_content"]
            },
            "애플": {
                "description": "혁신적인 하드웨어/소프트웨어 기업",
                "intent": "marketing_copy",
                "domain": "technology",
                "target": "일반 사용자, 프리미엄 고객",
                "tone": "프리미엄하고 세련된",
                "keywords": ["하드웨어", "소프트웨어", "디자인", "프리미엄", "생태계"],
                "related_intents": ["startup_pitch", "education_content"]
            },
            "테슬라": {
                "description": "전기차 및 에너지 솔루션 기업",
                "intent": "startup_pitch",
                "domain": "technology",
                "target": "투자자, 환경 보호자, 자동차 애호가",
                "tone": "혁신적이고 환경 친화적",
                "keywords": ["전기차", "에너지", "자율주행", "환경", "혁신"],
                "related_intents": ["marketing_copy", "grant_proposal"]
            },
            
            # 교육/플랫폼 관련
            "유튜브": {
                "description": "동영상 공유 및 스트리밍 플랫폼",
                "intent": "marketing_copy",
                "domain": "technology",
                "target": "콘텐츠 크리에이터, 일반 사용자",
                "tone": "창의적이고 친근한",
                "keywords": ["동영상", "콘텐츠", "스트리밍", "크리에이터", "광고"],
                "related_intents": ["education_content", "startup_pitch"]
            },
            "넷플릭스": {
                "description": "스트리밍 엔터테인먼트 플랫폼",
                "intent": "marketing_copy",
                "domain": "technology",
                "target": "일반 사용자, 엔터테인먼트 애호가",
                "tone": "엔터테인먼트적이고 매력적인",
                "keywords": ["스트리밍", "엔터테인먼트", "드라마", "영화", "콘텐츠"],
                "related_intents": ["startup_pitch", "education_content"]
            },
            
            # 정책/기관 관련
            "코로나19": {
                "description": "COVID-19 팬데믹",
                "intent": "policy_brief",
                "domain": "healthcare",
                "target": "정책 입안자, 의료진, 일반 시민",
                "tone": "신중하고 정보 제공적",
                "keywords": ["감염병", "의료", "정책", "예방", "백신", "사회적 거리두기"],
                "related_intents": ["grant_proposal", "education_content"]
            },
            "탄소중립": {
                "description": "탄소 배출량과 흡수량의 균형",
                "intent": "policy_brief",
                "domain": "environment",
                "target": "정책 입안자, 기업, 일반 시민",
                "tone": "환경 친화적이고 지속가능한",
                "keywords": ["환경", "탄소", "기후변화", "친환경", "에너지", "지속가능"],
                "related_intents": ["grant_proposal", "startup_pitch"]
            }
        }
        
        # 고유명사 패턴 매칭을 위한 정규표현식
        self.name_patterns = {
            r"프롬프트OS": "프롬프트OS",
            r"ChatGPT": "ChatGPT",
            r"스마트시티": "스마트시티",
            r"메타버스": "메타버스",
            r"핀테크": "핀테크",
            r"바이오": "바이오",
            r"구글": "구글",
            r"애플": "애플",
            r"테슬라": "테슬라",
            r"유튜브": "유튜브",
            r"넷플릭스": "넷플릭스",
            r"코로나19": "코로나19",
            r"탄소중립": "탄소중립"
        }
    
    def find_named_entities(self, utterance: str) -> List[Dict]:
        """
        발화에서 고유명사를 찾습니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            List[Dict]: 찾은 고유명사들의 정보 리스트
        """
        found_entities = []
        
        for pattern, name in self.name_patterns.items():
            if re.search(pattern, utterance, re.IGNORECASE):
                if name in self.naming_dict:
                    entity_info = self.naming_dict[name].copy()
                    entity_info['name'] = name
                    entity_info['pattern'] = pattern
                    found_entities.append(entity_info)
        
        return found_entities
    
    def get_best_mapping(self, utterance: str) -> Optional[Dict]:
        """
        발화에서 가장 적합한 고유명사 매핑을 찾습니다.
        
        Args:
            utterance: 사용자 발화
            
        Returns:
            Optional[Dict]: 가장 적합한 매핑 정보
        """
        entities = self.find_named_entities(utterance)
        
        if not entities:
            return None
        
        # 여러 고유명사가 있는 경우 우선순위 결정
        if len(entities) > 1:
            # 키워드 매칭 점수로 우선순위 결정
            best_entity = max(entities, key=lambda x: self._calculate_keyword_score(utterance, x))
            return best_entity
        
        return entities[0]
    
    def _calculate_keyword_score(self, utterance: str, entity: Dict) -> float:
        """키워드 매칭 점수를 계산합니다."""
        score = 0
        utterance_lower = utterance.lower()
        
        for keyword in entity.get('keywords', []):
            if keyword.lower() in utterance_lower:
                score += len(keyword) / 10.0
        
        return score
    
    def enhance_intent_classification(self, utterance: str, original_intent: str) -> Tuple[str, float, Dict]:
        """
        고유명사 정보를 활용하여 intent 분류를 개선합니다.
        
        Args:
            utterance: 사용자 발화
            original_intent: 원래 분류된 intent
            
        Returns:
            Tuple[str, float, Dict]: (개선된 intent, 신뢰도, 추가 정보)
        """
        # 고유명사 찾기
        entity = self.get_best_mapping(utterance)
        
        if not entity:
            return original_intent, 0.5, {}
        
        # 고유명사 기반 intent 제안
        suggested_intent = entity['intent']
        
        # 원래 intent가 unknown이거나 고유명사와 관련이 없으면 고유명사 기반 intent 사용
        if original_intent == "unknown" or original_intent not in entity['related_intents']:
            return suggested_intent, 0.9, {
                'entity': entity,
                'reason': f"고유명사 '{entity['name']}' 기반 분류"
            }
        
        # 원래 intent가 고유명사와 관련이 있으면 신뢰도 증가
        return original_intent, 0.8, {
            'entity': entity,
            'reason': f"고유명사 '{entity['name']}'과 일치하는 분류"
        }
    
    def get_context_info(self, entity: Dict) -> Dict:
        """
        고유명사 기반 컨텍스트 정보를 반환합니다.
        
        Args:
            entity: 고유명사 정보
            
        Returns:
            Dict: 컨텍스트 정보
        """
        return {
            'intent': entity['intent'],
            'domain': entity['domain'],
            'target': entity['target'],
            'tone': entity['tone'],
            'description': entity['description'],
            'related_intents': entity['related_intents']
        }
    
    def add_named_entity(self, name: str, mapping_info: Dict):
        """
        새로운 고유명사를 사전에 추가합니다.
        
        Args:
            name: 고유명사
            mapping_info: 매핑 정보
        """
        self.naming_dict[name] = mapping_info
        
        # 패턴도 추가
        pattern = re.escape(name)
        self.name_patterns[pattern] = name
    
    def search_similar_names(self, query: str) -> List[Dict]:
        """
        유사한 고유명사를 검색합니다.
        
        Args:
            query: 검색 쿼리
            
        Returns:
            List[Dict]: 유사한 고유명사들의 정보
        """
        similar_names = []
        query_lower = query.lower()
        
        for name, info in self.naming_dict.items():
            # 이름에 쿼리가 포함되거나, 키워드에 쿼리가 포함되는 경우
            if (query_lower in name.lower() or 
                any(query_lower in keyword.lower() for keyword in info.get('keywords', []))):
                similar_info = info.copy()
                similar_info['name'] = name
                similar_names.append(similar_info)
        
        return similar_names

# 전역 인스턴스 생성
naming_dict = NamingDictionary() 