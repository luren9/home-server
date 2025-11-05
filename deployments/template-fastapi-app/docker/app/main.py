from fastapi import FastAPI

import requests

from requests import exceptions as requestexceptions

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world"}

@app.get("/health")
def read_root():
    return {"alive": True}
