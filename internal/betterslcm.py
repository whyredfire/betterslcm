import requests
from bs4 import BeautifulSoup
from roman import toRoman

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}
URL = "https://mujslcm.jaipur.manipal.edu:122"


def get_login_token():
    res = requests.get(URL, headers=HEADERS, allow_redirects=False, timeout=5)
    soup = BeautifulSoup(res.content, "html.parser")

    token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
    cookie = res.headers.get("Set-Cookie").split(";")[0]

    return token, cookie


def login(username, password):
    token, cookie = get_login_token()

    HEADERS["Cookie"] = cookie

    payload = {
        "__RequestVerificationToken": token,
        "EmailFor": "@muj.manipal.edu",
        "LoginFor": "2",
        "UserName": username,
        "Password": password,
    }

    res = requests.post(
        URL, data=payload, headers=HEADERS, allow_redirects=False, timeout=5
    )

    if not res:
        return False
    if not res.headers.get("Set-Cookie"):
        print(f"\nFailed to login as {username}.\n")
        return False

    asp_net_cookie = res.headers.get("Set-Cookie").split(";")[0]

    print(f"\nSuccesfully logged in as {username}.")
    return cookie, asp_net_cookie


def get_attendance(cookie, asp_net_cookie):
    HEADERS["Cookie"] = f"{cookie}; {asp_net_cookie}"
    res = requests.post(
        f"{URL}/Student/Academic/GetAttendanceSummaryList",
        headers=HEADERS,
        allow_redirects=False,
        timeout=3,
        data={"StudentCode": ""},
    )

    return res.json()["AttendanceSummaryList"]


def get_cgpa(cookie, asp_net_cookie):
    HEADERS["Cookie"] = f"{cookie}; {asp_net_cookie}"
    res = requests.post(
        f"{URL}/Student/Academic/GetCGPAGPAForFaculty",
        headers=HEADERS,
        allow_redirects=False,
        timeout=3,
        data={"Enrollment": "", "AcademicYear": "", "ProgramCode": ""},
    )

    return res.json()["InternalMarksList"][0]


def get_grades(cookie, asp_net_cookie, semester):
    HEADERS["Cookie"] = f"{cookie}; {asp_net_cookie}"
    res = requests.post(
        f"{URL}/Student/Academic/GetGradesForFaculty",
        headers=HEADERS,
        allow_redirects=False,
        timeout=3,
        data={"Enrollment": "", "Semester": toRoman(semester)},
    )

    return res.json()["InternalMarksList"]


def get_internal_marks(cookie, asp_net_cookie, semester):
    HEADERS["Cookie"] = f"{cookie}; {asp_net_cookie}"
    res = requests.post(
        f"{URL}/Student/Academic/GetInternalMarkForFaculty",
        headers=HEADERS,
        allow_redirects=False,
        timeout=3,
        data={"Enrollment": "", "Semester": toRoman(semester)},
    )

    return res.json()["InternalMarksList"]
