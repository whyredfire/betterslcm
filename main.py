from fastapi import FastAPI

from routers import slcm

app = FastAPI()


@app.get("/")
async def status():
    return {"message": "OK"}


app.include_router(slcm.app)
