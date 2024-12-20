from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import characters, users, auth, vote

app = FastAPI(title="Characters API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### ======================================= API/V1/CHARACTERS ===============================================
app.include_router(characters.router)

#### ======================================= USERS ===============================================
app.include_router(users.router)

#### ======================================= AUTHORIZATION ===============================================
app.include_router(auth.router)

#### ======================================= Voting ===============================================
app.include_router(vote.router)