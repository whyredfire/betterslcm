import requests
from bs4 import BeautifulSoup
from roman import toRoman

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}
LOGIN_URL = "https://mujslcm.jaipur.manipal.edu:122"


def get_login_token():
    res = requests.get(LOGIN_URL, headers=HEADERS, allow_redirects=False, timeout=5)
    soup = BeautifulSoup(res.content, "html.parser")

    token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]

    try:
        cookie = res.headers.get("Set-Cookie").split(";")[0]
    except AttributeError:
        print(f"Failed to extract cookie from {LOGIN_URL}")
        return False

    return token, cookie


def login(username, password):
    res = get_login_token()
    if not res:
        return False

    token, cookie = res[0], res[1]

    headers = HEADERS.copy()
    headers["Cookie"] = cookie

    payload = {
        "__RequestVerificationToken": token,
        "EmailFor": "@muj.manipal.edu",
        "LoginFor": "2",
        "UserName": username,
        "Password": password,
    }

    res = requests.post(
        LOGIN_URL, data=payload, headers=headers, allow_redirects=False, timeout=5
    )

    if not res:
        return False
    if not res.headers.get("Set-Cookie"):
        print(f"\nFailed to login as {username}.\n")
        return False

    try:
        asp_net_cookie = res.headers.get("Set-Cookie").split(";")[0]
    except AttributeError:
        print(f"\nFailed to log in as {username}")

    print(f"\nSuccesfully logged in as {username}.")
    return cookie, asp_net_cookie


def _send_request(cookie, asp_net_cookie, URL, payload, timeout=3):
    cookie = cookie.split("=")[1]
    asp_net_cookie = asp_net_cookie.split("=")[1]

    cookies = {
        "__RequestVerificationToken": cookie,
        "ASP.NET_SessionId": asp_net_cookie,
    }

    response = requests.post(
        URL,
        headers=HEADERS,
        cookies=cookies,
        allow_redirects=False,
        timeout=timeout,
        data=payload,
    )

    return response.json()


def get_attendance(cookie, asp_net_cookie):
    return _send_request(
        cookie,
        asp_net_cookie,
        f"{LOGIN_URL}/Student/Academic/GetAttendanceSummaryList",
        {"StudentCode": ""},
    )["AttendanceSummaryList"]


def get_cgpa(cookie, asp_net_cookie):
    return _send_request(
        cookie,
        asp_net_cookie,
        f"{LOGIN_URL}/Student/Academic/GetCGPAGPAForFaculty",
        {"Enrollment": "", "AcademicYear": "", "ProgramCode": ""},
    )["InternalMarksList"][0]


def get_grades(cookie, asp_net_cookie, semester):
    return _send_request(
        cookie,
        asp_net_cookie,
        f"{LOGIN_URL}/Student/Academic/GetGradesForFaculty",
        {"Enrollment": "", "Semester": toRoman(semester)},
    )["InternalMarksList"]


def get_internal_marks(cookie, asp_net_cookie, semester):
    return _send_request(
        cookie,
        asp_net_cookie,
        f"{LOGIN_URL}/Student/Academic/GetInternalMarkForFaculty",
        {"Enrollment": "", "Semester": toRoman(semester)},
    )["InternalMarksList"]
