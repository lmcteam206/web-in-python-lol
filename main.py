from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API working 🎉"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"hello": name}
