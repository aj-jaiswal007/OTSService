from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

from otsapp.services.secret_keeper import SecretKeeper
from .dtos import SecretData

app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="otsapp/templates")

secret_keeper = SecretKeeper()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": 123})


@app.post("/secret")
def create_secret(request: Request, secret: str = Form(...)):
    key = secret_keeper.add_secret(data=SecretData(secret=secret))
    return templates.TemplateResponse(
        "secret.html",
        {"request": request, "base_url": "http://127.0.0.1:8000/", "key": key},
    )


@app.get("/{key}")
def read_secret(request: Request, key: str):
    try:
        data = secret_keeper.get_secret(key=key)
    except KeyError:
        return templates.TemplateResponse("invalid.html", {"request": request})

    secret_keeper.remove_secret(key=key)
    return templates.TemplateResponse(
        "read_secret.html", {"request": request, "secret": data.secret}
    )
