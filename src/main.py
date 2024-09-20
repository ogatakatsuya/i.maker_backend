from fastapi import APIRouter, FastAPI

app = FastAPI()



@app.get("/")
def hello():
    return {"Hello": "World"}