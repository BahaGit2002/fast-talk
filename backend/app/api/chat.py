from fastapi import APIRouter


router = APIRouter(prefix="/chats", tags=["chats"])


router.post("")
async def create_chat():
	pass
