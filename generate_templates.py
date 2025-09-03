#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
템플릿 파일 자동 생성 스크립트
13개의 intent에 대해 각각 8개의 템플릿 파일을 생성합니다.
"""

import os
import re

def create_template_content(intent: str, index: int) -> str:
    """템플릿 파일 내용을 생성합니다."""
    return f"""[Template] This is template {index} for intent `{intent}`. Please fill in {{placeholder1}} and {{placeholder2}}.

사용자 요청: {{user_utterance}}
의도: {{intent}}
도메인: {{domain}}
톤: {{tone}}
시제: {{tense}}
대상: {{audience}}

추가 정보:
- {{additional_info_1}}
- {{additional_info_2}}
- {{additional_info_3}}

프롬프트 생성 지침:
1. {{instruction_1}}
2. {{instruction_2}}
3. {{instruction_3}}

출력 형식:
{{output_format}}

예시:
{{example_output}}
"""

def generate_templates():
    """모든 intent에 대해 템플릿 파일을 생성합니다."""
    
    intents = [
        "business_plan", "marketing_copy", "summary", "self_intro",
        "proposal_ai", "proposal_ai_government", "proposal_ai_private",
        "proposal_climate", "grant_proposal", "customer_reply",
        "customer_reply_apology", "summary_meeting", "general_request"
    ]
    
    templates_dir = "templates"
    
    # templates 디렉토리가 없으면 생성
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"✅ {templates_dir} 디렉토리를 생성했습니다.")
    
    total_files = 0
    
    for intent in intents:
        # intent별 하위 디렉토리 생성
        intent_dir = os.path.join(templates_dir, intent)
        if not os.path.exists(intent_dir):
            os.makedirs(intent_dir)
            print(f"✅ {intent} 디렉토리를 생성했습니다.")
        
        # 8개의 템플릿 파일 생성
        for index in range(1, 9):
            filename = f"{intent}_{index}.txt"
            filepath = os.path.join(intent_dir, filename)
            
            # 파일이 이미 존재하는지 확인
            if os.path.exists(filepath):
                print(f"⚠️  {filepath} 이미 존재합니다. 건너뜁니다.")
                continue
            
            # 템플릿 내용 생성
            content = create_template_content(intent, index)
            
            # 파일 작성
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {filepath} 생성 완료")
                total_files += 1
            except Exception as e:
                print(f"❌ {filepath} 생성 실패: {e}")
    
    print(f"\n🎉 템플릿 생성 완료!")
    print(f"📊 총 생성된 파일 수: {total_files}")
    print(f"📁 생성된 intent 수: {len(intents)}")
    print(f"📄 intent당 평균 파일 수: {total_files / len(intents):.1f}")

def verify_templates():
    """생성된 템플릿 파일들을 검증합니다."""
    print("\n🔍 템플릿 파일 검증 중...")
    
    intents = [
        "business_plan", "marketing_copy", "summary", "self_intro",
        "proposal_ai", "proposal_ai_government", "proposal_ai_private",
        "proposal_climate", "grant_proposal", "customer_reply",
        "customer_reply_apology", "summary_meeting", "general_request"
    ]
    
    total_files = 0
    missing_files = []
    
    for intent in intents:
        intent_dir = os.path.join("templates", intent)
        if not os.path.exists(intent_dir):
            print(f"❌ {intent} 디렉토리가 없습니다.")
            continue
        
        for index in range(1, 9):
            filename = f"{intent}_{index}.txt"
            filepath = os.path.join(intent_dir, filename)
            
            if os.path.exists(filepath):
                total_files += 1
                # 파일 크기 확인
                file_size = os.path.getsize(filepath)
                if file_size < 100:  # 100바이트 미만이면 의심스러움
                    print(f"⚠️  {filepath} 파일이 너무 작습니다 ({file_size} bytes)")
            else:
                missing_files.append(filepath)
    
    print(f"✅ 검증 완료!")
    print(f"📊 총 파일 수: {total_files}")
    print(f"❌ 누락된 파일 수: {len(missing_files)}")
    
    if missing_files:
        print("누락된 파일들:")
        for file in missing_files[:5]:  # 처음 5개만 표시
            print(f"  - {file}")
        if len(missing_files) > 5:
            print(f"  ... 및 {len(missing_files) - 5}개 더")

if __name__ == "__main__":
    print("🚀 템플릿 파일 자동 생성 시작...")
    print("=" * 50)
    
    generate_templates()
    verify_templates()
    
    print("\n" + "=" * 50)
    print("✨ 모든 작업이 완료되었습니다!") 