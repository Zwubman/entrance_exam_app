from fastapi import FastAPI
from app.router import user
from app.config.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/", tags=['Health Routers'])
def health():
    return "The server is live..."


app.include_router(user.router)