from fastapi import FastAPI
from db.connect import connect_database
from routes.authentication import authRouter

app = FastAPI()

#Include Routes
app.include_router(authRouter)


#Connect to Db
db_client = connect_database()
@app.get("/")
def root():
    if db_client:
        return {"message":"DB connect Successfully"}
    return {"message":"Connection Failure"}