from fastapi import FastAPI
from db.connect import MongoDBSingleton
from routes.authentication import authRouter
from routes.userRoute import userRouter
from routes.events import eventRouter

app = FastAPI()

#Include Routes
app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(eventRouter)

#Connect to Db
db = MongoDBSingleton().get_database()
@app.get("/")
def root():
    if db is not None:
        return {"message":"DB connect Successfully"}
    return {"message":"Connection Failure"}