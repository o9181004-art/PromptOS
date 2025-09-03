// 입력 필드 포커스 효과
const mainInput = document.querySelector('.main-input');
mainInput.addEventListener('focus', function() {
    this.parentElement.style.transform = 'scale(1.01)';
});

mainInput.addEventListener('blur', function() {
    this.parentElement.style.transform = 'scale(1)';
});

// 버튼 클릭 효과 및 기능
const buttons = document.querySelectorAll('.action-btn');
const primaryBtn = document.querySelector('.primary-btn');
const secondaryBtn = document.querySelector('.secondary-btn');

// 모든 버튼 클릭 효과
buttons.forEach(button => {
    button.addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});

// 새로 메시지 보기 (리셋) 기능
primaryBtn.addEventListener('click', function() {
    // 확인 메시지 (선택사항)
    if (mainInput.value.trim() && !confirm('입력한 내용이 삭제됩니다. 계속하시겠습니까?')) {
        return;
    }
    
    // 입력창 초기화
    mainInput.value = '';
    
    // 부드러운 애니메이션 효과
    mainInput.style.opacity = '0.5';
    mainInput.style.transform = 'scale(0.98)';
    
    setTimeout(() => {
        mainInput.style.opacity = '1';
        mainInput.style.transform = 'scale(1)';
        mainInput.focus();
    }, 200);
    
    // 성공 피드백 (버튼 색상 변경)
    this.style.background = 'linear-gradient(135deg, #4ecdc4, #44a08d)';
    setTimeout(() => {
        this.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
    }, 1000);
});

// 프롬프트 생성하기 기능 (기본 동작)
secondaryBtn.addEventListener('click', function() {
    const userInput = mainInput.value.trim();
    if (!userInput) {
        alert('먼저 작업 내용을 입력해주세요.');
        mainInput.focus();
        return;
    }
    
    // 여기에 실제 프롬프트 생성 로직 추가 예정
    console.log('프롬프트 생성 요청:', userInput);
    alert('프롬프트 생성 기능은 곧 추가될 예정입니다!');
});

// 기능 아이템 호버 시 아이콘 회전
const featureItems = document.querySelectorAll('.feature-item');
featureItems.forEach(item => {
    const icon = item.querySelector('.feature-icon');
    item.addEventListener('mouseenter', () => {
        icon.style.transform = 'rotate(10deg) scale(1.1)';
    });
    item.addEventListener('mouseleave', () => {
        icon.style.transform = 'rotate(0deg) scale(1)';
    });
});

// 예시 태그 클릭 시 입력창에 추가
const exampleTags = document.querySelectorAll('.example-tag');
exampleTags.forEach(tag => {
    tag.addEventListener('click', function() {
        const tagText = this.textContent;
        const currentValue = mainInput.value;
        const newValue = currentValue ? `${currentValue}\n\n${tagText}에 대한 프롬프트를 만들어주세요.` : `${tagText}에 대한 프롬프트를 만들어주세요.`;
        mainInput.value = newValue;
        mainInput.focus();
    });
}); 