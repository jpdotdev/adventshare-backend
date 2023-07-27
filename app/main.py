from fastapi import FastAPI
from .routers import stories, users, auth, likes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stories.router) 
app.include_router(users.router) 
app.include_router(auth.router) 
app.include_router(likes.router) 

@app.get("/")
def root():
    return {"message": "Successfully deployed from CI/CD pipeline."}



