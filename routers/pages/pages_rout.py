from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
from starlette.responses import RedirectResponse, JSONResponse

from config import CONFIG
from crud.AdminCRUD import CRUDAdmin
from crud.TelegramMessageCRUD import CRUDTelegramMessage
from models import User
from schemas.TelegramMessageSchemas import TelegramMessageSchema

router = APIRouter(
    prefix='/pages',
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory='./templates')


@router.get("/stats", name="stats")
async def get_stats(request: Request):
    stats_data = {"data": [12, 10, 7, 55]}  # Пример данных
    return templates.TemplateResponse("stat.html", {"request": request, "stats": stats_data})


@router.get("/form", response_class=HTMLResponse, name="form")
async def get_form(request: Request):
    return templates.TemplateResponse('test.html', context={'request': request})


@router.post("/send_message/")
async def send_message(message: str = Form(...)):
    telegram_bot_token = CONFIG.BOT.TOKEN
    getAdmin = await CRUDAdmin.get_all()
    for admin in getAdmin:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {
            'chat_id': admin.admin_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        await CRUDTelegramMessage.add(message=TelegramMessageSchema(countMessageAdmin=1))
        async with httpx.AsyncClient() as client:
            await client.post(url, data=payload)

    # return RedirectResponse("/admin/mailing")

