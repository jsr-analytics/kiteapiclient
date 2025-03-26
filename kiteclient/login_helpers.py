import backoff
import pyotp
import requests


@backoff.on_exception(backoff.constant, ValueError, interval=1, max_tries=5)
def get_enctoken(userid, password, twofa_sec) -> str:
    session = requests.Session()
    response = session.post(
        "https://kite.zerodha.com/api/login",
        data={"user_id": userid, "password": password},
    )
    response = session.post(
        "https://kite.zerodha.com/api/twofa",
        data={
            "request_id": response.json()["data"]["request_id"],
            "twofa_value": pyotp.TOTP(twofa_sec).now(),
            "user_id": response.json()["data"]["user_id"],
        },
    )
    enctoken = response.cookies.get("enctoken")
    if enctoken:
        return enctoken
    else:
        raise ValueError("Enter valid details !!!!")

