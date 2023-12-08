from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

# from models import Message
from models.engine import ASYNC_ENGINE

router = APIRouter(
    prefix='/chat',
    tags=['Чат']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_base: bool):
        # if add_to_base:
        #     await self.add_message(message=message)

        for connection in self.active_connections:
            await connection.send_text(message)

    # @staticmethod
    # async def add_message(message: str):
    #     async with AsyncSession(bind=ASYNC_ENGINE) as session:
    #         query = insert(Message).values(message=message)
    #         await session.execute(query)
    #         await session.commit()


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int | str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Пользователь #{client_id}: {data}", add_to_base=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь #{client_id} покинул чат", add_to_base=False)