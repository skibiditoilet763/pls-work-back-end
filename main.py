
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import auth, dishes, ingredient
from routes.account import router as account_router
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    app.include_router(auth.router, prefix="/auth")
    app.include_router(dishes.router, prefix="/dishes")
    app.include_router(ingredient.router, prefix="/ingredients")
    app.include_router(account_router, prefix="/account")
    logger.info("All routers included successfully")
except Exception as e:
    logger.error(f"Error during router inclusion: {str(e)}")
    raise

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
