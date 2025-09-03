#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
템플릿 파일 존재 여부 확인 테스트
"""

import os
from template_mapper import TemplateMapper

def test_template_files():
    """템플릿 파일 존재 여부를 확인합니다."""
    print("=== 템플릿 파일 존재 여부 확인 ===")
    
    mapper = TemplateMapper()
    
    print(f"\n총 {len(mapper.intent_template_mapping)}개의 intent에 대해 {sum(len(v) for v in mapper.intent_template_mapping.values())}개의 템플릿이 매핑되었습니다.")
    
    missing_files = []
    total_files = 0
    
    for intent, file_list in mapper.intent_template_mapping.items():
        print(f"\n[{intent}]:")
        for file in file_list:
            total_files += 1
            file_path = os.path.join("templates", file)
            if os.path.exists(file_path):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (누락)")
                missing_files.append(file)
    
    print(f"\n=== 요약 ===")
    print(f"총 파일 수: {total_files}")
    print(f"존재하는 파일: {total_files - len(missing_files)}")
    print(f"누락된 파일: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  누락된 파일 목록:")
        for file in missing_files:
            print(f"  - {file}")
    else:
        print(f"\n✅ 모든 템플릿 파일이 정상적으로 존재합니다!")

if __name__ == "__main__":
    test_template_files() 