from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="NMCK System", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    print(f"✅ Статические файлы из: {static_dir}")
else:
    print(f"❌ Директория {static_dir} не найдена")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "nmck-system", "version": "1.0.0"}

# Простой API для тестирования
@app.get("/api/test")
async def test():
    return {"message": "API работает", "system": "NMCK Search"}

@app.get("/api/session")
async def create_session():
    import uuid
    return {"id": str(uuid.uuid4()), "created_at": "2026-01-20T14:00:00"}

@app.get("/api/tasks")
async def list_tasks():
    return []

@app.post("/api/tasks/direct")
async def create_task():
    import uuid
    return {"id": str(uuid.uuid4()), "status": "PENDING", "message": "Task created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
