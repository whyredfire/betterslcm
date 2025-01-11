from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from routers import slcm

app = FastAPI()


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content=jsonable_encoder(exc.detail)
    )


@app.get("/")
async def redirect():
    return RedirectResponse("https://github.com/whyredfire/betterslcm")


@app.get("/status")
async def status():
    return {"message": "OK"}


app.include_router(slcm.app)
