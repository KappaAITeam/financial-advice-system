from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from dotenv import load_dotenv
from base64 import b64decode
from pathlib import Path
import os
import io


load_dotenv('.env')
openai = OpenAI()
chat_history = []

app = FastAPI()
templates = Jinja2Templates("templates")


OUTPUT_DIR = Path("./audio_output")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("frontend.html", {"request": request, "audio_url": None, "transcript": None})


# @app.post('/', response_class=Request):
    
@app.post("/voice-to-voice/", response_class=HTMLResponse)
async def voice_to_voice(request: Request, audio: UploadFile):
    """
    Endpoint to receive audio from the user, transcribe it, generate an AI audio response,
    and return it for auto-play on the frontend.
    """
    try:
        #Transcribes the uploaded audio
        audio_content = await audio.read()
        transcription = openai.audio.transcriptions.create(
            file=(audio.filename, audio_content),
            model="whisper-1"
        )
        user_text = transcription.text
        chat_history.append({"role": "user", "content": user_text})

        # AI response for both text and audio
        system_prompt = """
            You are a helpful stock and forex adviser that helps people to choose the right stock to invest in.
            Let your answers be concise. If you don't know the answer, say 'I don't know'.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
        response = openai.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "onyx", "format": "wav"},
            messages=messages
        )

        #Decodes and saves the audio response
        audio_data = b64decode(response.choices[0].message.audio.data)
        audio_filename = OUTPUT_DIR / f"response_{len(chat_history)}.wav"
        with open(audio_filename, "wb") as f:
            f.write(audio_data)

        
        audio_transcript = response.choices[0].message.audio.transcript
        chat_history.append({"role": "assistant", "content": audio_transcript})

        # Returning a file to the frontend
        audio_url = f"/audio_output/{audio_filename.name}"
        return templates.TemplateResponse(
            "frontend.html",
            {
                'request': request,
                'audio_url': audio_url,
                "transcript": audio_transcript
                
            }
        
         ) #FileResponse(
        #     path=audio_filename,
        #     media_type="audio/wav",
        #     headers={"Content-Disposition": "inline"} 
        # )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get('/audio_output/{filename}')
async def get_audio(filename):
    audio_path = OUTPUT_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(
            path=audio_path,
            media_type="audio/wav",
            headers={"Content-Disposition": "inline"} 
        )
# without saving to disk
@app.post("/voice-to-voice-stream/")
async def voice_to_voice_stream(audio: UploadFile):
    try:
        #Transcription...
        audio_content = await audio.read()
        transcription = openai.audio.transcriptions.create(
            file=(audio.filename, audio_content),
            model="whisper-1"
        )
        user_text = transcription.text
        chat_history.append({"role": "user", "content": user_text})

        # AI response
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text}
        ]
        response = openai.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "onyx", "format": "wav"},
            messages=messages
        )

        # Direct audio streaming
        audio_data = b64decode(response.choices[0].message.audio.data)
        audio_transcript = response.choices[0].message.audio.transcript
        chat_history.append({"role": "assistant", "content": audio_transcript})

        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)