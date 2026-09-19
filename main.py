from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Elankadhir's First API is Live!"}