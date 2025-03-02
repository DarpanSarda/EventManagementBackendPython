from fastapi import FastAPI
from db.connect import MongoDBSingleton
from routes.authentication import authRouter
from routes.userRoute import userRouter
from routes.events import eventRouter
from routes.companies import companyRouter

app = FastAPI()

#Include Routes
app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(eventRouter)
app.include_router(companyRouter)

#Connect to Db
db = MongoDBSingleton().get_database()
@app.get("/")
def root():
    if db is not None:
        return {"message":"DB connect Successfully"}
    return {"message":"Connection Failure"}