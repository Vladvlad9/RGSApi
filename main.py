import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from admin.Authentication import authentication_backend
from admin.views import UserAdmin, AdminAdmin, TelegramMessageAdmin, DialogAdmin
from config import CONFIG
from models.engine import ASYNC_ENGINE
from fastapi.templating import Jinja2Templates
from routers.pages.pages_rout import router as pages_routers
from sqladmin import Admin
from starlette.applications import Starlette

WEBHOOK_PATH = f"/bot/{CONFIG.BOT.TOKEN}"
WEBHOOK_URL = f"{CONFIG.BOT.NGROK_TUNEL_URL}{WEBHOOK_PATH}"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app_star = Starlette()

admin = Admin(app=app, engine=ASYNC_ENGINE, templates_dir="templates", authentication_backend=authentication_backend)
admin.title = "Панель администратора"

app.include_router(pages_routers)

# admin.add_view(ReportView)
admin.add_view(UserAdmin)
admin.add_view(AdminAdmin)
admin.add_view(DialogAdmin)
admin.add_view(TelegramMessageAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    pass


@app.get("/")
async def root(request: Request):
    return RedirectResponse("/admin")


@app.get("/hello/{name}")
async def say_hello(name: str):
    # await bot.send_message(chat_id=381252111, text=f'{name}')
    return {"message": f"Hello {name}"}


origins = [
    "https://vladvlad9.github.io/pageTest.io/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type',
                   'Access-Control-Allow-Headers', 'Set-Cookie', 'Authorization', 'Access-Control-Allow-Origin']

)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
