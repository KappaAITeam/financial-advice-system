from fastapi import APIRouter, WebSocket
from src.services.voice_to_voice_websocket import transcribe_audio, get_groq_response, stream_tts
from src.utils.logger import logger

router = APIRouter()


@router.websocket("/ws/voice")
async def websocket_voice(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")

    while True:
        try:
            # Receive audio chunk as bytes
            audio_chunk = await websocket.receive_bytes()
            logger.info("Received audio chunk")

            # Convert speech to text (ensure function handles bytes correctly)
            user_text = transcribe_audio(audio_chunk)

            if user_text.strip():
                # Send AI response as text first
                ai_response = await get_groq_response(user_text)

                logger.info(f"Sent AI response: {ai_response}")

                # Stream the TTS response (ensure it returns bytes)
                async for audio_chunk in stream_tts(ai_response):
                    await websocket.send_bytes(audio_chunk)

                logger.info("Sent streamed TTS response")

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            break
