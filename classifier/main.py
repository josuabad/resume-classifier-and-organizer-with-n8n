import io
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pypdf import PdfReader
from transformers import pipeline

app = FastAPI(title="ML Content Classifier API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

print(f"Cargando pipeline Zero-Shot desde: {MODEL_PATH}...")

try:
    # La pipeline carga internamente el modelo y el tokenizador desde la carpeta 'model'
    classifier = pipeline(
        "zero-shot-classification", model=MODEL_PATH, tokenizer=MODEL_PATH
    )
    print("Modelo cargado con éxito.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

labels = ["suitable", "possibly-suitable", "not-suitable"]


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    vacancy_id: str = Form(...),
):
    try:
        # 1. Leer archivo PDF
        pdf_bytes = await file.read()
        filename = file.filename

        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="El archivo subido está vacío.")

        # 2. Extraer texto
        extracted_text = ""
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        extracted_text = extracted_text.strip()
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer texto legible del archivo PDF.",
            )

        # 3. Construir secuencia e Inferencia Zero-Shot
        vacancy_description = search_vacancy(vacancy_id)
        if not vacancy_description:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró la vacante con ID: {vacancy_id}",
            )
        sequence_to_classify = (
            f"Vacancy: {vacancy_description}\n\nResume content:\n{extracted_text}"
        )

        # Truncation=True evita errores cuando el CV excede el tamaño máximo del modelo
        result = classifier(
            sequence_to_classify,
            candidate_labels=labels,
            truncation=True,
            hypothesis_template="This candidate is {} for the job position.",  # Ayuda al modelo a entender el contexto
        )

        print(type(result))
        print(f"Resultado de clasificación: {result}")

        # 4. Respuesta estructurada para n8n
        return {
            "vacancy_id": vacancy_id,
            "filename": filename,
            "categoria": result["labels"][0],  # La etiqueta con mayor puntuación
            "confidence": round(
                result["scores"][0], 4
            ),  # Score de confianza (ej. 0.9234)
            "character_count": len(extracted_text),
            "status": "success",
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el archivo PDF: {str(e)}"
        )


def read_vacancies():
    import json

    vacancies_file = os.path.join(BASE_DIR, "data", "vacancies.json")
    try:
        with open(vacancies_file, "r", encoding="utf-8") as f:
            vacancies = json.load(f)
        return vacancies
    except Exception as e:
        print(f"Error al leer el archivo de vacantes: {e}")
        return []


def search_vacancy(vacancy_id):
    vacancies: list = read_vacancies()
    for vacancy in vacancies:
        vacancy: dict
        if vacancy.get("id") == vacancy_id:
            return vacancy.get("description")
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
