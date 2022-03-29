from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status

from otsapp.routers import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from otsapp.settings import Settings, get_settings

security = HTTPBasic()
load_dotenv()


def validate_credentials(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
):
    if (
        credentials.username != settings.MASTER_USERNAME
        or credentials.password != settings.MASTER_PASSWORD
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(security), Depends(validate_credentials)],
)
app.include_router(router=secrets.router, prefix="")
