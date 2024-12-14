from fastapi import FastAPI

from routers import slcm

app = FastAPI()


@app.get("/status")
async def status():
    return {"message": "OK"}


app.include_router(slcm.app)
