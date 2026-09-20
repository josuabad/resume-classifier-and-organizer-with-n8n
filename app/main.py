from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Servir archivos estáticos (CSS y JS) desde la carpeta raíz
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("index.html")


@app.post("/postular")
async def postular(vacancy_id: str = Form(...), cv: UploadFile = File(...)):
    # Crear carpeta 'uploads' si no existe y guardar el CV enviado
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{cv.filename}"

    with open(file_path, "wb") as f:
        content = await cv.read()
        f.write(content)

    return {"status": "success", "vacancy_id": vacancy_id, "filename": cv.filename}
