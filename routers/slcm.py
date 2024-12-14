from fastapi import APIRouter, Response, Request

from internal import betterslcm
from schemas import Credentials

app = APIRouter()


@app.post("/login")
async def login(creds: Credentials, response: Response):
    res = betterslcm.login(creds.username, creds.password)
    if not res:
        return False

    cookie, asp_net_cookie = res[0], res[1]

    response.set_cookie(key="cookie", value=cookie)
    response.set_cookie(key="asp_net_cookie", value=asp_net_cookie)
    return {"message": "logged in"}


@app.post("/attendance")
async def attendance(request: Request):
    cookie = request.cookies.get("cookie")
    asp_net_cookie = request.cookies.get("asp_net_cookie")

    return betterslcm.get_attendance(cookie, asp_net_cookie)


@app.post("/cgpa")
async def cgpa(request: Request):
    cookie = request.cookies.get("cookie")
    asp_net_cookie = request.cookies.get("asp_net_cookie")

    return betterslcm.get_cgpa(cookie, asp_net_cookie)


@app.post("/grades")
async def grades(request: Request, semester: int):
    cookie = request.cookies.get("cookie")
    asp_net_cookie = request.cookies.get("asp_net_cookie")

    return betterslcm.get_grades(cookie, asp_net_cookie, semester)


@app.post("/internal_marks")
async def internal_marks(request: Request, semester: int):
    cookie = request.cookies.get("cookie")
    asp_net_cookie = request.cookies.get("asp_net_cookie")

    return betterslcm.get_grades(cookie, asp_net_cookie, semester)
