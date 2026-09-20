# Resume Classifier and Organizer with n8n

End-to-End automated pipeline that receives CVs/Resumes via HTTP requests, classifies candidate profiles using a local Machine Learning model and automatically organizes files into category-specific storage destinations using n8n running inside Docker.

## Environment Setup

**Container:**

```bash
docker compose up -d
```

```bash
docker compose down
```

```bash
docker compose down -v
```

**Requirements:**

```bash
pip install --upgrade pip && pip install fastapi uvicorn python-multipart httpx pypdf transformers torch jupyterlab && pip install --upgrade jupyter
```

```bash
uvicorn main:app --reload
```
