from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import slcm

app = FastAPI()


@app.get("/")
async def redirect():
    return RedirectResponse("https://github.com/whyredfire/betterslcm")


@app.get("/status")
async def status():
    return {"message": "OK"}


app.include_router(slcm.app)
