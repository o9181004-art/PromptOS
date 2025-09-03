/**
 * PromptOS UI JavaScript
 * Python 백엔드와 연동하는 프론트엔드 로직
 */

class PromptOSUI {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupKeyboardShortcuts();
    }

    initializeElements() {
        // DOM 요소들 초기화
        this.mainInput = document.querySelector('.main-input');
        this.primaryBtn = document.querySelector('.primary-btn');
        this.secondaryBtn = document.querySelector('.secondary-btn');
        this.resultSection = document.getElementById('result');
        this.resultContent = this.resultSection.querySelector('.result-content');
        this.exampleTags = document.querySelectorAll('.example-tag');
        this.featureItems = document.querySelectorAll('.feature-item');
    }

    bindEvents() {
        // 입력 필드 포커스 효과
        this.mainInput.addEventListener('focus', () => this.handleInputFocus());
        this.mainInput.addEventListener('blur', () => this.handleInputBlur());

        // 버튼 클릭 이벤트
        this.primaryBtn.addEventListener('click', () => this.clearInput());
        this.secondaryBtn.addEventListener('click', () => this.generatePrompt());

        // 모든 버튼 클릭 효과
        document.querySelectorAll('.action-btn').forEach(button => {
            button.addEventListener('click', (e) => this.handleButtonClick(e));
        });

        // 예시 태그 클릭 이벤트
        this.exampleTags.forEach(tag => {
            tag.addEventListener('click', (e) => this.handleExampleTagClick(e));
        });

        // 기능 아이템 호버 효과
        this.featureItems.forEach(item => {
            const icon = item.querySelector('.feature-icon');
            item.addEventListener('mouseenter', () => {
                icon.style.transform = 'rotate(10deg) scale(1.1)';
            });
            item.addEventListener('mouseleave', () => {
                icon.style.transform = 'rotate(0deg) scale(1)';
            });
        });
    }

    setupKeyboardShortcuts() {
        // 키보드 단축키 설정
        document.addEventListener('keydown', (e) => {
            // Ctrl + Enter: 프롬프트 생성
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.generatePrompt();
            }
            
            // Ctrl + Shift + C: 입력창 초기화
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                this.clearInput();
            }
        });
    }

    handleInputFocus() {
        this.mainInput.parentElement.style.transform = 'scale(1.01)';
    }

    handleInputBlur() {
        this.mainInput.parentElement.style.transform = 'scale(1)';
    }

    handleButtonClick(event) {
        // 버튼 클릭 애니메이션 효과
        event.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            event.target.style.transform = '';
        }, 150);
    }

    async clearInput() {
        const currentValue = this.mainInput.value.trim();
        
        // 입력값이 있을 때만 확인 메시지 표시
        if (currentValue && !confirm('입력한 내용이 삭제됩니다. 계속하시겠습니까?')) {
            return;
        }
        
        // 입력창 초기화
        this.mainInput.value = '';
        
        // 부드러운 애니메이션 효과
        this.mainInput.style.opacity = '0.5';
        this.mainInput.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            this.mainInput.style.opacity = '1';
            this.mainInput.style.transform = 'scale(1)';
            this.mainInput.focus();
        }, 200);
        
        // 결과 영역 숨기기
        this.hideResult();
        
        // 성공 피드백 (버튼 색상 변경)
        this.primaryBtn.style.background = 'linear-gradient(135deg, #4ecdc4, #44a08d)';
        setTimeout(() => {
            this.primaryBtn.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
        }, 1000);

        // Python 백엔드에 초기화 요청 (선택사항)
        try {
            await this.callClearAPI();
        } catch (error) {
            console.log('초기화 API 호출 실패:', error);
        }
    }

    async generatePrompt() {
        const userInput = this.mainInput.value.trim();
        
        if (!userInput) {
            alert('먼저 작업 내용을 입력해주세요.');
            this.mainInput.focus();
            return;
        }

        // 로딩 상태 표시
        this.showLoadingState();

        try {
            // Python 백엔드 API 호출
            const result = await this.callPromptAPI(userInput);
            
            if (result.success) {
                this.showResult(result.prompt, result.intent, result.method);
            } else {
                this.showError(result.error || '프롬프트 생성에 실패했습니다.');
            }
        } catch (error) {
            console.error('프롬프트 생성 오류:', error);
            this.showError('서버 연결에 실패했습니다. 다시 시도해주세요.');
        }
    }

    async callPromptAPI(userInput) {
        // Streamlit 백엔드 API 호출
        try {
            const response = await fetch('/_stcore/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'generate_prompt',
                    user_input: userInput
                })
            });

            if (response.ok) {
                return await response.json();
            } else {
                throw new Error('API 호출 실패');
            }
        } catch (error) {
            // API 호출 실패 시 모의 응답 (개발용)
            console.log('API 호출 실패, 모의 응답 사용:', error);
            return this.getMockResponse(userInput);
        }
    }

    async callClearAPI() {
        // 입력 초기화 API 호출 (선택사항)
        try {
            const response = await fetch('/_stcore/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'clear_input'
                })
            });
            return response.ok;
        } catch (error) {
            console.log('초기화 API 호출 실패:', error);
            return false;
        }
    }

    getMockResponse(userInput) {
        // 개발용 모의 응답
        const mockPrompts = {
            '마케팅': `🎯 마케팅 카피 생성 프롬프트

당신은 창의적이고 설득력 있는 마케팅 카피라이터입니다. 다음 요구사항에 따라 매력적인 마케팅 카피를 작성해주세요:

📋 요구사항:
${userInput}

✨ 작성 가이드:
- 고객의 페인포인트를 정확히 파악
- 감정적 연결을 통한 설득력 있는 메시지
- 명확한 행동 유도 (CTA)
- 브랜드 톤앤매너 유지
- 간결하고 임팩트 있는 문장

📝 출력 형식:
1. 헤드라인 (주목을 끄는 제목)
2. 서브헤드라인 (부제목)
3. 본문 (설명 및 혜택)
4. CTA (행동 유도 문구)
5. 태그라인 (브랜드 슬로건)

위 가이드라인에 따라 매력적이고 효과적인 마케팅 카피를 작성해주세요.`,

            '기술': `🔧 기술 문서 작성 프롬프트

당신은 명확하고 체계적인 기술 문서 작성 전문가입니다. 다음 요구사항에 따라 전문적인 기술 문서를 작성해주세요:

📋 요구사항:
${userInput}

✨ 작성 가이드:
- 논리적 구조와 명확한 흐름
- 기술적 정확성과 전문성
- 독자 수준에 맞는 설명
- 시각적 요소 활용 제안
- 실용적이고 실행 가능한 내용

📝 출력 형식:
1. 개요 및 목적
2. 주요 개념 설명
3. 단계별 가이드
4. 주의사항 및 팁
5. 참고 자료 및 추가 정보

위 가이드라인에 따라 체계적이고 유용한 기술 문서를 작성해주세요.`,

            'default': `🚀 프롬프트 생성

다음 요구사항에 따라 최적화된 프롬프트를 생성해주세요:

📋 요구사항:
${userInput}

✨ 프롬프트 구성 요소:
- 명확한 목적과 역할 정의
- 구체적인 출력 형식 지정
- 품질 기준 및 제약사항
- 예시나 참고사항 포함
- 단계별 지시사항

📝 출력 형식:
1. 역할 및 목적 정의
2. 구체적인 작업 지시
3. 출력 형식 및 구조
4. 품질 기준 및 제약사항
5. 추가 참고사항

위 요구사항에 맞는 효과적이고 구체적인 프롬프트를 작성해주세요.`
        };

        // 입력 내용에 따른 프롬프트 선택
        let promptType = 'default';
        if (userInput.includes('마케팅') || userInput.includes('카피') || userInput.includes('광고')) {
            promptType = '마케팅';
        } else if (userInput.includes('기술') || userInput.includes('문서') || userInput.includes('매뉴얼')) {
            promptType = '기술';
        }

        return {
            success: true,
            prompt: mockPrompts[promptType],
            intent: promptType,
            method: 'mock_response'
        };
    }

    showLoadingState() {
        this.resultSection.classList.add('show');
        this.resultContent.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <span>프롬프트를 생성하고 있습니다...</span>
            </div>
        `;
    }

    showResult(prompt, intent, method) {
        this.resultSection.classList.add('show');
        this.resultContent.innerHTML = `
            <div style="margin-bottom: 15px;">
                <strong>생성된 프롬프트:</strong>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                ${prompt.replace(/\n/g, '<br>')}
            </div>
            <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6);">
                의도: ${intent} | 방법: ${method}
            </div>
            <button onclick="promptosUI.copyToClipboard()" style="margin-top: 10px; background: rgba(255, 255, 255, 0.1); border: none; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
                📋 클립보드에 복사
            </button>
        `;
    }

    showError(message) {
        this.resultSection.classList.add('show');
        this.resultContent.innerHTML = `
            <div style="color: #ff6b6b; margin-bottom: 10px;">
                <strong>❌ 오류가 발생했습니다</strong>
            </div>
            <div style="color: rgba(255, 255, 255, 0.8);">
                ${message}
            </div>
        `;
    }

    hideResult() {
        this.resultSection.classList.remove('show');
    }

    copyToClipboard() {
        const promptText = this.resultContent.textContent;
        navigator.clipboard.writeText(promptText).then(() => {
            this.showSuccessFeedback();
        }).catch(err => {
            console.error('클립보드 복사 실패:', err);
            alert('클립보드 복사에 실패했습니다.');
        });
    }

    showSuccessFeedback() {
        const copyBtn = this.resultContent.querySelector('button');
        if (copyBtn) {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✅ 복사 완료!';
            copyBtn.style.background = 'rgba(78, 205, 196, 0.3)';
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.background = 'rgba(255, 255, 255, 0.1)';
            }, 2000);
        }
    }

    handleExampleTagClick(event) {
        const tagText = event.target.textContent;
        const currentValue = this.mainInput.value;
        const newValue = currentValue ? 
            `${currentValue}\n\n${tagText}에 대한 프롬프트를 만들어주세요.` : 
            `${tagText}에 대한 프롬프트를 만들어주세요.`;
        
        this.mainInput.value = newValue;
        this.mainInput.focus();
        
        // 태그 클릭 효과
        event.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            event.target.style.transform = 'scale(1)';
        }, 150);
    }
}

// DOM 로드 완료 후 초기화
document.addEventListener('DOMContentLoaded', () => {
    window.promptosUI = new PromptOSUI();
    console.log('✅ PromptOS UI 초기화 완료');
}); 