import pytest
import requests,json


def main_url():
    return "https://reqres.in/api/login"

def test_main():
    url = main_url()
    data = {"email":"abc@gmail.com","passwars":123}
    response = requests.get(url,data)
    assert response.status_code == 200

