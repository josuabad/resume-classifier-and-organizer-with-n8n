## Environment Setup

**Container:**

```bash
docker compose up -d
```

```bash
docker compose down
```

<!-- ```bash
docker compose down -v
``` -->

**Requirements:**

```bash
pip install --upgrade pip && pip install fastapi uvicorn python-multipart pypdf transformers torch jupyterlab && pip install --upgrade jupyter
```

```bash
pip freeze > requirements.txt
```

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```
