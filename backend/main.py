import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.chat_routes import router

# Khởi tạo FastAPI app
app = FastAPI()

# Cấu hình CORS đơn giản
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thêm router
app.include_router(router, prefix="/api")

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint works!"}

# Mount frontend static files
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# Nếu chạy trực tiếp
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
