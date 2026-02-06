import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from core.network_model import NetworkAdapterModel
from core.ping_model import PingModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

adapter_service = NetworkAdapterModel()
ping_service = PingModel()

@app.get("/adapters")
def get_adapters():
    return adapter_service.get_all_adapters()

@app.websocket("/ws/ping")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    targets = [
        "1.1.1.1",
        "1.0.0.1",
        "8.8.8.8",
        "8.8.4.4",
        "9.9.9.9",
        "149.112.112.112",
        "208.67.222.222",
        "208.67.220.220",
        "4.2.2.1",
        "4.2.2.2",
        "64.6.64.6",
        "91.239.100.100",
        "84.200.69.80",
        "185.228.168.9",
        "76.76.2.0",
        "8.26.56.26",
        "1.1.1.2",
        "1.1.1.3",
        "216.146.35.35",
        "156.154.70.1"
    ]

    try:
        while True:
            results = await ping_service.ping_many(targets)
            await websocket.send_json(results)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Socket closed: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)