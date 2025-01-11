from bs4 import BeautifulSoup
from fastapi import APIRouter, Response, Request, HTTPException
from roman import toRoman
import requests

from schemas import Credentials


LOGIN_URL = "https://mujslcm.jaipur.manipal.edu"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}


def format_cookies(request):
    return {
        "__RequestVerificationToken": request.cookies.get("verification_token"),
        "ASP.NET_SessionId": request.cookies.get("session_id"),
    }


app = APIRouter()


@app.post("/login")
async def login(creds: Credentials, response: Response):

    _res = requests.get(LOGIN_URL, headers=HEADERS, allow_redirects=False, timeout=5)
    soup = BeautifulSoup(_res.content, "html.parser")

    _token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
    _cookies = _res.headers.get("Set-Cookie").split(";")[0]
    cookie = _cookies.split("=")[1]

    cookies = {"__RequestVerificationToken": cookie}
    payload = {
        "__RequestVerificationToken": _token,
        "EmailFor": "@muj.manipal.edu",
        "LoginFor": "2",
        "UserName": creds.username,
        "Password": creds.password,
    }

    res = requests.post(
        url=LOGIN_URL,
        data=payload,
        headers=HEADERS,
        cookies=cookies,
        allow_redirects=False,
    )

    if not res.headers.get("Set-Cookie"):
        raise HTTPException(status_code=401, detail={"message": "invalid credentials"})

    session_id = res.headers.get("Set-Cookie").split(";")[0].split("=")[1]

    response.set_cookie(key="verification_token", value=cookie)
    response.set_cookie(key="session_id", value=session_id)
    return {"message": "logged in"}


@app.get("/logout")
async def logout(request: Request, response: Response):

    if not (
        request.cookies.get("verification_token") or request.cookies.get("session_id")
    ):
        raise HTTPException(status_code=200, detail={"message": "user not logged in"})

    requests.post(
        url=f"{LOGIN_URL}/Home/Logout", headers=HEADERS, cookies=format_cookies(request)
    )

    response.delete_cookie("verification_token")
    response.delete_cookie("session_id")

    return {"message": "user logged out"}


@app.get("/attendance")
async def attendance(request: Request):
    response = requests.post(
        url=f"{LOGIN_URL}/Student/Academic/GetAttendanceSummaryList",
        data={"StudentCode": ""},
        headers=HEADERS,
        cookies=format_cookies(request),
    )

    try:
        return response.json()["AttendanceSummaryList"]
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=401, detail={"message": "unauthorized"})


@app.get("/cgpa")
async def cgpa(request: Request):
    response = requests.post(
        url=f"{LOGIN_URL}/Student/Academic/GetCGPAGPAForFaculty",
        data={"Enrollment": "", "AcademicYear": "", "ProgramCode": ""},
        headers=HEADERS,
        cookies=format_cookies(request),
    )

    try:
        return {
            i: j
            for i, j in response.json()["InternalMarksList"][0].items()
            if j not in [None, "null", "-"]
            and i not in ["sno", "RegistrationNo", "StudentName"]
        }
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=401, detail={"message": "unauthorized"})


@app.get("/grades")
async def grades(request: Request, semester: int):
    print(request.cookies.get("verification_token"))

    response = requests.post(
        url=f"{LOGIN_URL}/Student/Academic/GetGradesForFaculty",
        data={"Enrollment": "", "Semester": toRoman(semester)},
        headers=HEADERS,
        cookies=format_cookies(request),
    )

    try:
        return response.json()["InternalMarksList"]
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=401, detail={"message": "unauthorized"})


@app.get("/internal_marks")
async def internal_marks(request: Request, semester: int):
    response = requests.post(
        url=f"{LOGIN_URL}/Student/Academic/GetInternalMarkForFaculty",
        data={"Enrollment": "", "Semester": toRoman(semester)},
        headers=HEADERS,
        cookies=format_cookies(request),
    )

    try:
        return response.json()["InternalMarksList"]
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=401, detail={"message": "unauthorized"})
