"""Main entrypoint for the app."""
import logging
import aiofiles
import os
import pickle
import openai

from pathlib import Path
from typing import Annotated, Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from fastapi.templating import Jinja2Templates
from langchain.vectorstores import VectorStore
import requests

from callback import QuestionGenCallbackHandler, StreamingLLMCallbackHandler
from query_data import get_chain
from schemas import ChatResponse

from domain.query import query_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
vectorstore: Optional[VectorStore] = None


@app.on_event("startup")
async def startup_event():
    logging.info("loading vectorstore")
    if not Path("vectorstore.pkl").exists():
        raise ValueError("vectorstore.pkl does not exist, please run ingest.py first")
    with open("vectorstore.pkl", "rb") as f:
        global vectorstore
        vectorstore = pickle.load(f)


app.include_router(query_router.router)


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcriptions")
async def transcriptions(audioData: UploadFile,model: Annotated[str, Form()]):
    UPLOAD_DIRECTORY = "./whisper/"
    audio_file_path = os.path.join(UPLOAD_DIRECTORY, audioData.filename)

    async with aiofiles.open(audio_file_path, 'wb+') as out_file:
        content = await audioData.read()  # async read
        await out_file.write(content)  # async write

    audio_file= open(audio_file_path, "rb")

    transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription

@app.post("/tts")
async def tts(text: Annotated[str, Form()]):
    OUTPUT_FILE = "./tts/speech.mp3"
    CHUNK_SIZE = 1024
    elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ["ELEVENLABS_VOICE_ID"]
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {
    "Accept": "application/json",
    "xi-api-key": elevenlabs_api_key
    }
    headers["Content-Type"] = "application/json"

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost":0 
        }
    }

    response = requests.post(tts_url, json=data, headers=headers, stream=True)

    with open(OUTPUT_FILE, 'wb+') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return FileResponse(OUTPUT_FILE, media_type="audio/mp3")



@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    question_handler = QuestionGenCallbackHandler(websocket)
    stream_handler = StreamingLLMCallbackHandler(websocket)
    chat_history = []
    qa_chain = await get_chain(vectorstore, question_handler, stream_handler)
    # Use the below line instead of the above line to enable tracing
    # Ensure `langchain-server` is running
    # qa_chain = get_chain(vectorstore, question_handler, stream_handler, tracing=True)

    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()
            resp = ChatResponse(sender="you", message=question, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            result = await qa_chain.acall({"question": question, "chat_history": chat_history})
            chat_history.append((question, result["answer"]))

            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
