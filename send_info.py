import requests


WEB_APP_URL = "http://127.0.0.1:5000/"


def send_user_info(data):
    requests.post(WEB_APP_URL, json=data)# .__dict__)
