# Train Ticket Chatbot

카카오톡 채널을 통해 코레일 기차표를 예매하고 관리하는 챗봇 서비스입니다.

## 주요 기능

- 코레일 계정 관리
- 기차표 예매
- 매진된 기차표 자동 예매 (매크로)
- 예매 현황 조회

## 기술 스택

- Python 3.8+
- FastAPI
- SQLAlchemy
- Redis
- Kakao Channel API
- Korail2 API

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yoonjw0/train_ticket_chatbot.git
cd train_ticket_chatbot
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp app/.env.example app/.env
# .env 파일을 편집하여 필요한 설정값 입력
```

5. 서버 실행
```bash
uvicorn app.main:app --reload
```

## 환경 변수 설정

- `KAKAO_CHANNEL_ID`: 카카오톡 채널 ID
- `KAKAO_API_KEY`: 카카오톡 API 키
- `KAKAO_CHANNEL_SECRET`: 카카오톡 채널 시크릿
- `DATABASE_URL`: 데이터베이스 URL
- `REDIS_URL`: Redis 서버 URL
- `ENCRYPTION_KEY`: 암호화 키
