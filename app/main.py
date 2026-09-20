from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import httpx

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

# URL del Webhook de n8n
N8N_WEBHOOK_URL = (
    "http://http://192.168.1.38:5678/webhook-test/a80b5f9a-3b41-44f7-a6d3-153c3082c3a6"
)


@app.get("/")
async def serve_index():
    return FileResponse("index.html")


@app.post("/postular")
async def postular(vacancy_id: str = Form(...), cv: UploadFile = File(...)):
    # 1. Leer el contenido del archivo cargado
    file_content = await cv.read()

    # 2. Guardar opcionalmente en local
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{cv.filename}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 3. Preparar los datos multipart para reenviar a n8n
    files = {
        "cv": (cv.filename, file_content, cv.content_type or "application/octet-stream")
    }
    data = {"vacancy_id": vacancy_id}

    # 4. Enviar la petición POST asíncrona a n8n
    async with httpx.AsyncClient() as client:
        try:
            n8n_response = await client.post(N8N_WEBHOOK_URL, data=data, files=files)
            n8n_response.raise_for_status()
            n8n_result = n8n_response.json()
        except httpx.HTTPError as exc:
            return {"status": "error", "detail": f"Error al enviar a n8n: {str(exc)}"}

    return {
        "status": "success",
        "vacancy_id": vacancy_id,
        "filename": cv.filename,
        "n8n_response": n8n_result,
    }
