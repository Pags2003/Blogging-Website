from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import posts, users
from routes.auth import router as auth_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

