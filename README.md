# 🤖 EXA Chat - EXAONE 3.5 32B 챗봇

Together AI API를 사용하여 LG AI Research의 **EXAONE 3.5 32B Instruct** 모델과 대화할 수 있는 웹 기반 챗봇입니다.

## ✨ 주요 기능

- 🧠 **EXAONE 3.5 32B Instruct** 모델 사용
- 🌐 **웹 기반 인터페이스** - 브라우저에서 바로 사용
- 🔄 **대화 기록 관리** - 최근 대화 맥락 유지
- 🌍 **한국어 최적화** - 한국어 질문과 답변에 특화
- 🚀 **클라우드 배포 가능** - Together AI API 사용으로 어디서든 배포 가능

## 🛠️ 기술 스택

- **Backend**: Python Flask
- **AI Model**: EXAONE 3.5 32B Instruct (via Together AI API)
- **Frontend**: HTML, CSS, JavaScript
- **Dependencies**: Flask, Requests, Python-dotenv

## 📋 필요 사항

- Python 3.7+
- Together AI API 키 ([Together AI](https://together.ai)에서 발급)

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/djyalu/exa-chat.git
cd exa-chat
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env` 파일을 생성하고 Together AI API 키를 입력하세요:

```env
TOGETHER_API_KEY=your-together-ai-api-key-here
```

### 4. 애플리케이션 실행
```bash
python app.py
```

### 5. 웹 브라우저에서 접속
브라우저에서 `http://localhost:5000`으로 접속하여 챗봇을 사용하세요!

## 🌐 배포

### 클라우드 플랫폼 배포 가능
Together AI API를 사용하므로 다음 플랫폼에서 쉽게 배포할 수 있습니다:
- **Heroku**
- **Railway**
- **Vercel**
- **AWS EC2**
- **Google Cloud Run**
- **Azure Container Apps**

### 환경변수 설정
배포 시 플랫폼의 환경변수 설정에서 `TOGETHER_API_KEY`를 추가하세요.

## 🔧 API 엔드포인트

- `GET /` - 메인 페이지
- `POST /chat` - 채팅 메시지 전송
- `POST /clear` - 대화 기록 초기화  
- `GET /history` - 대화 기록 조회

## 📁 프로젝트 구조

```
exa-chat/
├── app.py              # Flask 애플리케이션 메인 파일
├── requirements.txt    # Python 의존성
├── .env               # 환경변수 (Git에서 제외됨)
├── .gitignore         # Git 제외 파일 목록
├── README.md          # 프로젝트 설명
└── templates/         # HTML 템플릿
    └── index.html     # 메인 웹 페이지
```

## 🤝 기여

이슈나 개선사항이 있으시면 GitHub Issues를 통해 알려주세요!

## 📄 라이선스

MIT License

## 🙏 감사의 말

- [LG AI Research](https://www.lgresearch.ai/) - EXAONE 모델 개발
- [Together AI](https://together.ai/) - API 서비스 제공 