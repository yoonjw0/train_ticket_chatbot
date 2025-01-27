from typing import Dict, Any, Optional
from fastapi import HTTPException
import json
import requests
from ..core.config import get_settings

settings = get_settings()

class KakaoHandler:
    def __init__(self):
        self.api_key = settings.KAKAO_API_KEY
        self.channel_id = settings.KAKAO_CHANNEL_ID
    
    def create_basic_card(self, title: str, description: str, buttons: list) -> Dict[str, Any]:
        """기본 카드 템플릿 생성"""
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "basicCard": {
                        "title": title,
                        "description": description,
                        "buttons": buttons
                    }
                }]
            }
        }
    
    def create_carousel(self, items: list) -> Dict[str, Any]:
        """캐러셀 템플릿 생성"""
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "carousel": {
                        "type": "basicCard",
                        "items": items
                    }
                }]
            }
        }
    
    def create_quick_replies(self, items: list) -> Dict[str, Any]:
        """퀵리플라이 버튼 생성"""
        return {
            "version": "2.0",
            "template": {
                "quickReplies": items
            }
        }

    def send_message(self, user_id: str, message: Dict[str, Any]) -> bool:
        """카카오톡 메시지 발송"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"https://kapi.kakao.com/v1/api/talk/channels/{self.channel_id}/message",
                headers=headers,
                json={
                    "user_id": user_id,
                    "message": json.dumps(message)
                }
            )
            response.raise_for_status()
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def handle_postback(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """포스트백 데이터 처리"""
        action = data.get("action")
        
        if action == "register_account":
            return self.show_account_registration(user_id)
        elif action == "book_ticket":
            return self.show_station_selection(user_id)
        elif action == "check_macro":
            return self.show_macro_status(user_id)
        
        raise HTTPException(status_code=400, detail="Invalid action")
    
    def show_account_registration(self, user_id: str) -> Dict[str, Any]:
        """계정 등록 화면 표시"""
        buttons = [
            {
                "action": "block",
                "label": "새 계정 등록",
                "messageText": "새 계정 등록",
                "blockId": "account_registration_block"
            },
            {
                "action": "block",
                "label": "취소",
                "messageText": "취소",
                "blockId": "main_menu_block"
            }
        ]
        
        return self.create_basic_card(
            title="코레일 계정 등록",
            description="안전한 계정 등록을 위해 아래 버튼을 선택해주세요.",
            buttons=buttons
        )
    
    def show_station_selection(self, user_id: str) -> Dict[str, Any]:
        """역 선택 화면 표시"""
        # 자주 가는 역 목록은 DB에서 조회
        quick_replies = [
            {"action": "block", "label": "서울", "messageText": "서울", "blockId": "station_select_block"},
            {"action": "block", "label": "용산", "messageText": "용산", "blockId": "station_select_block"},
            {"action": "block", "label": "대전", "messageText": "대전", "blockId": "station_select_block"},
        ]
        
        return self.create_quick_replies(quick_replies)
    
    def show_macro_status(self, user_id: str) -> Dict[str, Any]:
        """매크로 상태 화면 표시"""
        # DB에서 사용자의 매크로 작업 조회
        return self.create_basic_card(
            title="매크로 상태",
            description="현재 실행 중인 매크로가 없습니다.",
            buttons=[{
                "action": "block",
                "label": "돌아가기",
                "messageText": "돌아가기",
                "blockId": "main_menu_block"
            }]
        )
