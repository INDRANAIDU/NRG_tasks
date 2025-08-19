from fastapi import FastAPI
from routes import router  # Import the APIRouter from routes.py

app = FastAPI()
app.include_router(router)  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
