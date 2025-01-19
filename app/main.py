from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor  # type: ignore
from pydantic.v1 import BaseSettings
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers import posts, users, auth, vote

# Dependency to get DB session


models.Base.metadata.create_all(bind=engine)

my_posts = [{"title": "Post 1", "body": "This is post 1 content", 'id': 1},
            {"title": "Post 2", "body": "This is post 2 content", 'id': 2}

            ]


# class Settings(BaseSettings):
#
#     password = "vaibhav"
#     database_username = "postgres"
#     database_port = 5432
#     secret_key = "ahsgjhsADHBAJDBSljkbmfbajksabfjbfjafsbjsafbjkasfbajksfbsajfbasjkfbsakjfbsakjfbsajkfbasj"
#
#
# settings = Settings()
# print(settings.database_password)
app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Hello": "Worzzzzzzzd!!!!!"}


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)

    return posts
