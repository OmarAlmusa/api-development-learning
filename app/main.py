from fastapi import FastAPI
# from .postgres_ORM import create_DB_and_tables
# from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from .routes import characters, users, auth, vote

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_DB_and_tables()
#     yield




# app = FastAPI(lifespan=lifespan, title="Characters API")
app = FastAPI(title="Characters API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### ======================================= STATIC FILES ===============================================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def homepage():
    html_file_path = os.path.join("app", "static", "index.html")
    with open(html_file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



#### ======================================= API/V1/CHARACTERS ===============================================
app.include_router(characters.router)

#### ======================================= USERS ===============================================
app.include_router(users.router)

#### ======================================= AUTHORIZATION ===============================================
app.include_router(auth.router)

#### ======================================= Voting ===============================================
app.include_router(vote.router)