#!/usr/bin/env python3
"""
API 키 설정 확인 및 테스트 스크립트
"""

import os
import requests
from dotenv import load_dotenv

def test_api_keys():
    """API 키 설정을 확인하고 테스트합니다."""
    
    print("🔑 API 키 설정 확인 중...")
    
    # .env 파일 로드
    load_dotenv()
    
    # API 키 확인
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    together_key = os.getenv("TOGETHER_API_KEY")
    
    print(f"OpenRouter API 키: {'✅ 설정됨' if openrouter_key else '❌ 설정되지 않음'}")
    print(f"Groq API 키: {'✅ 설정됨' if groq_key else '❌ 설정되지 않음'}")
    print(f"Together AI API 키: {'✅ 설정됨' if together_key else '❌ 설정되지 않음'}")
    
    # OpenRouter API 테스트
    if openrouter_key:
        print("\n🧪 OpenRouter API 테스트 중...")
        try:
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
            
            # 모델 목록 가져오기
            response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ OpenRouter API 연결 성공!")
                models = response.json().get("data", [])
                print(f"   사용 가능한 모델 수: {len(models)}")
            else:
                print(f"❌ OpenRouter API 연결 실패: {response.status_code}")
                print(f"   응답: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ OpenRouter API 테스트 중 오류: {e}")
    else:
        print("\n⚠️ OpenRouter API 키가 설정되지 않았습니다.")
        print("   .env 파일에 OPENROUTER_API_KEY를 설정해주세요.")
    
    # Groq API 테스트
    if groq_key:
        print("\n🧪 Groq API 테스트 중...")
        try:
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            
            # 간단한 테스트 요청
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Groq API 연결 성공!")
            else:
                print(f"❌ Groq API 연결 실패: {response.status_code}")
                print(f"   응답: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Groq API 테스트 중 오류: {e}")
    
    # Together AI API 테스트
    if together_key:
        print("\n🧪 Together AI API 테스트 중...")
        try:
            headers = {
                "Authorization": f"Bearer {together_key}",
                "Content-Type": "application/json"
            }
            
            # 간단한 테스트 요청
            payload = {
                "model": "meta-llama/Llama-3-8b-chat-hf",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                "https://api.together.xyz/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Together AI API 연결 성공!")
            else:
                print(f"❌ Together AI API 연결 실패: {response.status_code}")
                print(f"   응답: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Together AI API 테스트 중 오류: {e}")
    
    print("\n" + "="*50)
    print("📝 API 키 설정 방법:")
    print("1. 프로젝트 루트에 .env 파일을 생성하세요")
    print("2. 다음 내용을 추가하세요:")
    print("   OPENROUTER_API_KEY=your_api_key_here")
    print("3. https://openrouter.ai/ 에서 API 키를 발급받으세요")
    print("="*50)

if __name__ == "__main__":
    test_api_keys() 