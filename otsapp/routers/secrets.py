from typing import Optional
from fastapi import Depends, Form, Request
from fastapi import APIRouter
from otsapp.settings import Settings, get_settings
from otsapp.dtos import SecretData

from ..services.secret_keeper import SecretKeeper
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="otsapp/templates")
secret_keeper = SecretKeeper()


@router.get("/")
def home(request: Request, settings: Settings = Depends(get_settings)):
    print("settings", settings.BASE_URL)
    return templates.TemplateResponse("home.html", {"request": request, "id": 123})


@router.post("/secret")
def create_secret(
    request: Request,
    secret: str = Form(...),
    passphrase: Optional[str] = Form(default=None),
    settings: Settings = Depends(get_settings),
):
    key = secret_keeper.add_secret(
        data=SecretData(secret=secret, passphrase=passphrase)
    )
    return templates.TemplateResponse(
        "secret_link.html",
        {"request": request, "base_url": settings.BASE_URL.rstrip("/"), "key": key},
    )


@router.get("/{key}")
def get_secret(request: Request, key: str):
    if not secret_keeper.is_key_valid(key=key):
        return templates.TemplateResponse(
            "invalid.html", {"request": request, "message": "Not found!"}
        )

    return templates.TemplateResponse("show_secret.html", {"request": request})


@router.post("/{key}")
def view_secret(
    request: Request, key: str, passphrase: Optional[str] = Form(default=None)
):
    try:
        data = secret_keeper.get_secret(key=key)
        assert data.passphrase == passphrase
    except KeyError:
        return templates.TemplateResponse(
            "invalid.html", {"request": request, "message": "Not found!"}
        )

    except AssertionError:
        return templates.TemplateResponse(
            "invalid.html",
            {
                "request": request,
                "message": "Unauthorized. Pls enter correct passphrase",
            },
        )

    secret_keeper.remove_secret(key=key)
    return templates.TemplateResponse(
        "read_secret.html", {"request": request, "secret": data.secret}
    )
