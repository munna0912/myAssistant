# app/routers/ml.py
from fastapi import APIRouter, UploadFile, File, Form
from services import stt, llm, tts

router = APIRouter()

@router.post("/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    # Save and process the audio using the STT service
    transcription = await stt.process_audio(audio)
    return {"transcription": transcription}

@router.post("/llm-chat")
def llm_chat(prompt: str = Form(...)):
    # Query the local LLM (Ollama) using the provided prompt
    response = llm.query(prompt)
    return {"response": response}

@router.post("/tts")
def text_to_speech(text: str = Form(...)):
    # Convert text to speech using the TTS service
    tts.speak(text)
    return {"status": "Spoken"}
