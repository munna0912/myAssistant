# app/services/stt.py
import os
import subprocess
from tempfile import NamedTemporaryFile
from fastapi import UploadFile

import whisper

# Load the 'base' model
model = whisper.load_model("base")

async def process_audio(audio: UploadFile) -> str:

   # process with a temp file
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(audio.file.read())
        audio_path = tmp_audio.name
    try:
        # generate the streaming response and return it
        result = model.transcribe(audio_path)
        return result["text"]
    finally:
        os.unlink(audio_path)
