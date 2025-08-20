from fastapi import FastAPI
from routes import router
from database import engine, Base

app = FastAPI()
app.include_router(router)

# Create tables if not exist (optional if already in pgAdmin)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
