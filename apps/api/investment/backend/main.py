import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
# import FinanceDataReader as fdr

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # do something when the server starts
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # do something when the server shuts down
    pass
@app.get("/")
async def homepage(request: Request):
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)