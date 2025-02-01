# app/services/stt.py
import os
import subprocess
from tempfile import NamedTemporaryFile
from fastapi import UploadFile

import whisper

# Load the 'base' model
model = whisper.load_model("base")

async def process_audio(audio: UploadFile) -> str:
   # process the audio stream with the Whisper model
    with NamedTemporaryFile(delete=False, suffix=".webm") as tmp_audio:
        tmp_audio.write(audio.file.read())
        audio_path = tmp_audio.name
    try:
        result = whisper.transcribe(model, audio_path)
        return result["text"]
    finally:
        os.unlink(audio_path)
