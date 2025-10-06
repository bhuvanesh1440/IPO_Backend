from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware # <--- NEW IMPORT
from .ipo_operations import ipo_ops

app = FastAPI(title="IPO OPS API")

# --- CORS Configuration ---
# 1. Define the origins that are allowed to access your API
#    Your frontend is running on http://localhost:5173
origins = [
    "http://localhost:5173", # <-- Allow your React/Vite frontend
    "http://127.0.0.1:5173", # <-- Sometimes browsers use 127.0.0.1 instead of localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # List of allowed origins
    allow_credentials=True,            # Allow cookies/authorization headers
    allow_methods=["*"],               # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],               # Allow all headers
)
# --------------------------


@app.post("/operations")
async def reconcile(exchange_file: UploadFile = File(...), psp_file: UploadFile = File(...)):
    exchange_data = await exchange_file.read()
    psp_data = await psp_file.read()
    result = ipo_ops(exchange_data, psp_data)
    return result

@app.get("/")
async def root():
    return {"message": "IPO OPS API is running!"}