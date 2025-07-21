from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
from edge_tts import Communicate
from model_interface import prompts, llms
from contextlib import asynccontextmanager
import shutil
import tempfile
import asyncio
import uuid
import os
import sys

# def sync_stream_tts(text, voice="en-US-AriaNeural"):
#     tts = Communicate(text, voice)
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

#     async def fetch_chunks():
#         chunks = []
#         async for chunk in tts.stream():
#             if chunk["type"] == "audio":
#                 chunks.append(chunk["data"])
#         return chunks

#     return loop.run_until_complete(fetch_chunks())

model = WhisperModel("base", device="cpu", compute_type="int8")

AUDIO_DIR = "whisper_test/generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

prompt_maker = prompts.Prompt()

llm = llms.Llama_3p1_8B_Instruct_4BitQuantized()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Waiting for LLM to be loaded on the GPU ...")
    status = llm.load()

    if status != llms.ModelStatus.READY:
        print("\nFailed to load model before timeout")
        llm.unload()
        raise RuntimeError("Failed to load LLM")

    print("\nLLM loaded on the GPU!")
    yield # app shall now serve requests

    print("Unloading LLM ...")
    llm.unload()

app = FastAPI(lifespan=lifespan)

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Save uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        shutil.copyfileobj(audio.file, temp_audio)
        temp_path = temp_audio.name

    # Transcribe
    segments, _ = model.transcribe(temp_path)
    transcript = " ".join([seg.text for seg in segments])

    print("Detected Text: ")
    print(transcript)

    # prompt = prompt_maker.get_step_gen_conv_prompt(
    #     transcript, False, "ConvModel.v1.SystemTestMinor"
    # )

    tools_str = llm.get_tool_integrator().get_tool_prompt()
    prompt = prompt_maker.get_cot_conv_prompt(transcript, False, tools=tools_str)

    # response = llm.call([prompt], reflection=True)[0]
    # response = prompt_maker.filter_llama_tokens(response)
    print("Sending prompt to LLM")
    response_tokens: list[str] = []
    
    for token in llm.call_stream([prompt]):
        response_tokens.append(str(token))
        print(token, end="", flush=True)


    # response_tokens: list[str] = await asyncio.get_event_loop().run_in_executor(None, run_llm_stream)
    print("Past the generator block")
    print(response_tokens)
    response = "".join(response_tokens)
    response_no_llama = prompt_maker.filter_llama_tokens(response)
    response_no_llama_no_md = prompt_maker.filter_markdown(response_no_llama)

    # Generate TTS
    tts = Communicate(response_no_llama_no_md, "en-US-AriaNeural")
    stream = tts.stream()

    uid = str(uuid.uuid4())
    output_path = f"{AUDIO_DIR}/{uid}.mp3"
    with open(output_path, "wb") as f:
        async for chunk in stream:
            if chunk["type"] == "audio":
                f.write(chunk["data"])

    return {
        "transcript": response,
        "audio_url": f"/audio/{uid}"
    }

@app.get("/audio/{uid}")
def get_audio(uid: str):
    file_path = os.path.join(AUDIO_DIR, f"{uid}.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}, 404

app.mount("/", StaticFiles(directory="whisper_test/static", html=True), name="static")

