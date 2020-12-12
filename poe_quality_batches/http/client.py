import requests


def client():
    response = requests.get("http://localhost:8080/")
    return response
