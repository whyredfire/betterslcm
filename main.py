from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def status():
    return {"message": "OK"}
