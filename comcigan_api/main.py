from fastapi import FastAPI
from comcigan_api.routes import school
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(school.router)

@app.get("/")
async def index():
    return "Comcigan Api Index Page"
