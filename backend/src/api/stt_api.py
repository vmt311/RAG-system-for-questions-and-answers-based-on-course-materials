from fastapi import APIRouter, File, UploadFile
import whisper
import tempfile

router = APIRouter()
model = whisper.load_model("small")

@router.post("")
async def speech_to_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    result = model.transcribe(tmp_path, language='ru')
    print(result["text"])
    return {"text": result["text"]}
