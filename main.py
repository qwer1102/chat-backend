from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 테스트용 기본 엔드포인트 추가
@app.get("/")
async def get_root():
    return HTMLResponse("<h1>FastAPI WebSocket 서버 실행 중!</h1>")

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 받은 메시지: {data}")
            for client in clients:
                await client.send_text(data)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        clients.remove(websocket)
