from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .bot.kakao_handler import KakaoHandler
from .core.config import get_settings
from .db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()
settings = get_settings()

# Database setup
engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kakao handler setup
kakao_handler = KakaoHandler()

@app.post("/webhook")
async def kakao_webhook(request: Request):
    try:
        body = await request.json()
        user_id = body.get("userRequest", {}).get("user", {}).get("id")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found")
        
        # 포스트백 데이터 처리
        if "action" in body:
            response = kakao_handler.handle_postback(user_id, body["action"])
        else:
            # 기본 응답
            response = kakao_handler.create_basic_card(
                title="코레일 예매 도우미",
                description="원하시는 메뉴를 선택해주세요.",
                buttons=[
                    {
                        "action": "block",
                        "label": "계정 등록/변경",
                        "messageText": "계정 등록/변경",
                        "blockId": "account_registration_block"
                    },
                    {
                        "action": "block",
                        "label": "기차표 예매",
                        "messageText": "기차표 예매",
                        "blockId": "ticket_booking_block"
                    },
                    {
                        "action": "block",
                        "label": "매크로 상태 확인",
                        "messageText": "매크로 상태 확인",
                        "blockId": "macro_status_block"
                    }
                ]
            )
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
