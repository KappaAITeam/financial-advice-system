from src.utils.logger import logger
from vosk import Model, KaldiRecognizer
from TTS.api import TTS
import json
import os
import asyncio
from groq import AsyncGroq
from src.config import config

# Load configurations
GROQ_API_KEY = config.GROQ_API_KEY
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

VOSK_MODEL_PATH = "models/vosk-model-en-us-0.22"

if not os.path.exists(VOSK_MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {VOSK_MODEL_PATH}")

vosk_model = Model(VOSK_MODEL_PATH)

# Load Coqui TTS Model (VITS-based)
tts_model = TTS("tts_models/en/ljspeech/vits", progress_bar=False).to("cpu")


def transcribe_audio(audio_chunk):
    """Transcribes audio using Vosk with a fallback mechanism"""
    recognizer = KaldiRecognizer(vosk_model, 16000)

    if recognizer.AcceptWaveform(audio_chunk):
        result = json.loads(recognizer.Result())
        transcript = result.get("text", "").strip()
        if not transcript:
            return "Sorry, I didn't catch that. Can you repeat?"
        logger.info(f"Transcribed: {transcript}")
        return transcript

    # Handle partial results (helps with short phrases)
    partial_result = json.loads(recognizer.PartialResult())
    return partial_result.get("partial", "")


async def get_groq_response(user_text):
    """Fetch AI-generated response from Groq's LLM with better accuracy"""
    try:
        response = await groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a professional stock market advisor. Your primary role is to provide accurate, up-to-date financial insights based on factual data. Avoid speculation, misinformation, or making investment decisions for the user. Provide well-researched responses with clear explanations."},
                {"role": "user", "content": user_text}
            ]
        )
        ai_response = response.choices[0].message.content
        logger.info(f"Groq AI Response: {ai_response}")
        return ai_response
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return "I couldn't process your request right now."


async def stream_tts(text):
    """Stream text-to-speech (TTS) output asynchronously"""
    output_wav = "temp_output.wav"

    # Generate speech and save to file
    tts_model.tts_to_file(text=text, file_path=output_wav)

    # Read file in chunks and stream
    with open(output_wav, "rb") as audio_file:
        while chunk := audio_file.read(1024):  # Stream 1KB at a time
            yield chunk
            await asyncio.sleep(0)
