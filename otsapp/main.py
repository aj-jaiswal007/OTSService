from dotenv import load_dotenv
from fastapi import FastAPI

from otsapp.routers import secrets

load_dotenv()
app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router=secrets.router, prefix="")
