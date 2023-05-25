# fastapi main example

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def homepage(request: Request):
    return HTMLResponse(content={"message": "Hello, World!"})



if __name__ == "__main__":
    uvicorn.run(app, port=9000)
