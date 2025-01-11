from bs4 import BeautifulSoup
from fastapi import APIRouter, Response, Request, HTTPException
from roman import toRoman
import requests

from schemas import Credentials

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}
API_REF = {
    "login": "https://mujslcm.jaipur.manipal.edu",
    "logout": "/Home/Logout",
    "attendance": "/Student/Academic/GetAttendanceSummaryList",
    "cgpa": "/Student/Academic/GetCGPAGPAForFaculty",
    "grades": "/Student/Academic/GetGradesForFaculty",
    "internal_marks": "/Student/Academic/GetInternalMarkForFaculty",
}


def make_request(endpoint, request, data=None):
    try:
        return requests.post(
            url=API_REF["login"] + API_REF[endpoint],
            data=data,
            headers=HEADERS,
            cookies={
                "__RequestVerificationToken": request.cookies.get("verification_token"),
                "ASP.NET_SessionId": request.cookies.get("session_id"),
            },
        ).json()
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=401, detail={"message": "unauthorized"})


app = APIRouter()


@app.post("/login")
async def login(creds: Credentials, response: Response):

    _res = requests.get(
        API_REF["login"], headers=HEADERS, allow_redirects=False, timeout=5
    )
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
        url=API_REF["login"],
        data=payload,
        headers=HEADERS,
        cookies=cookies,
        allow_redirects=False,
    )

    if not res.headers.get("Set-Cookie"):
        raise HTTPException(status_code=401, detail={"message": "invalid credentials"})

    session_id = res.headers.get("Set-Cookie").split(";")[0].split("=")[1]

    response.set_cookie(key="verification_token", value=cookie, expires="Session")
    response.set_cookie(key="session_id", value=session_id)
    return {"message": "logged in"}


@app.get("/logout")
async def logout(request: Request, response: Response):

    requests.post(
        url=API_REF["login"] + API_REF["logout"],
        headers=HEADERS,
        cookies=request.cookies.get("session_id"),
    )

    return {"message": "user logged out"}


@app.get("/attendance")
async def attendance(request: Request):
    return make_request("attendance", request=request, data={"StudentCode": ""})[
        "AttendanceSummaryList"
    ]


@app.get("/cgpa")
async def cgpa(request: Request):
    return {
        i: j
        for i, j in make_request(
            "cgpa",
            request=request,
            data={"Enrollment": "", "AcademicYear": "", "ProgramCode": ""},
        )["InternalMarksList"][0].items()
        if j not in [None, "null", "-"]
        and i not in ["sno", "RegistrationNo", "StudentName"]
    }


@app.get("/grades")
async def grades(request: Request, semester: int):
    return (
        {
            i: j
            for i, j in subject.items()
            if j not in [None, "null", "-"] and i != "sno"
        }
        for subject in make_request(
            "grades",
            request=request,
            data={"Enrollment": "", "Semester": toRoman(semester)},
        )["InternalMarksList"]
    )


@app.get("/internal_marks")
async def internal_marks(request: Request, semester: int):
    return make_request(
        "internal_marks",
        request=request,
        data={"Enrollment": "", "Semester": toRoman(semester)},
    )["InternalMarksList"]
