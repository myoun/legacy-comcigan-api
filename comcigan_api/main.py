from fastapi import FastAPI
from comcigan_api.routes import school

app = FastAPI()

app.include_router(school.router)

@app.get("/")
async def index():
    return "Comcigan Api Index Page"
