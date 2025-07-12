from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
from edge_tts import Communicate
import shutil
import tempfile
import asyncio
import uuid
import os

app = FastAPI()
model = WhisperModel("base", device="cuda", compute_type="float16")

AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Save uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        shutil.copyfileobj(audio.file, temp_audio)
        temp_path = temp_audio.name

    # Transcribe
    segments, _ = model.transcribe(temp_path)
    transcript = " ".join([seg.text for seg in segments])

    # Generate TTS
    tts = Communicate(transcript, "en-US-AriaNeural")
    stream = tts.stream()

    uid = str(uuid.uuid4())
    output_path = f"{AUDIO_DIR}/{uid}.mp3"
    with open(output_path, "wb") as f:
        async for chunk in stream:
            if chunk["type"] == "audio":
                f.write(chunk["data"])

    return {
        "transcript": transcript,
        "audio_url": f"/audio/{uid}"
    }

@app.get("/audio/{uid}")
def get_audio(uid: str):
    file_path = os.path.join(AUDIO_DIR, f"{uid}.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}, 404

app.mount("/", StaticFiles(directory="static", html=True), name="static")

