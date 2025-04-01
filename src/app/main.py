import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status, Security
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException as StarletteHTTPException

from .api.user import router as users_router
from .api.quests import router as quests_router
from .models import enums, models
from .schemas import schemas
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from .config.database_config import async_get_db
from .api.points_summary import router as points_summary_router
from .api.user_rxp import router as user_rxp_router
from .api.all_rxp import router as all_rxp_router
from .api.signature import router as signature_router 

load_dotenv()

app = FastAPI()  # Remove the dependencies parameter
# 0xf191b68344902d6116d07c48eaaa084680ed7041d968a26f6122c5845966c418
# Remove the API key security check
# API_KEY = os.getenv("API_KEY")
# API_KEY_NAME = "access_token"

# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# async def get_api_key(
#     api_key_header: str = Security(api_key_header),
# ):
#     if api_key_header == API_KEY:
#         return api_key_header
#     else:
#         raise HTTPException(status_code=403, detail="Could not validate credentials")

# Apply to all routes
# app = FastAPI(dependencies=[Depends(get_api_key)])  # Remove this line

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app.include_router(users_router)
app.include_router(quests_router)
app.include_router(points_summary_router)
app.include_router(user_rxp_router)
app.include_router(all_rxp_router)
app.include_router(signature_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)