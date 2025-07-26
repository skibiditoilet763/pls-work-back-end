from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import auth, dishes, ingredient  # Added ingredient

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

app.include_router(auth.router, prefix="/auth")
app.include_router(dishes.router, prefix="/dishes")
app.include_router(ingredient.router, prefix="/ingredients")  # Added ingredient router

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}