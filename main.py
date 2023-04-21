import os
import time
import json
from fastapi import FastAPI, Form
import browser_func

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_url")
async def upload_url(url: str = Form()):
    print(url)
    data = {}
    data = browser_func.main_browser_func(url)
    print(f"Return Data : ")
    print(data)
    return data

# if __name__ == '__main__':
#     
