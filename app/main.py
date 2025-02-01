# app/main.py
from fastapi import FastAPI
from routers import ui, ml

app = FastAPI(title="Voice Assistant")

# Include routers with proper prefixes
app.include_router(ui.router, prefix="/ui", tags=["UI"])
app.include_router(ml.router, prefix="/ml", tags=["ML"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
