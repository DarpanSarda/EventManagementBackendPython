from eventapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.connect import MongoDBSingleton
from routes.authentication import authRouter
from routes.userRoute import userRouter
from routes.events import eventRouter
from routes.companies import companyRouter
from routes.review import reviewRouter
from routes.feedback import feedbackRouter
from routes.faqs import faqRouter
from routes.ticket import ticketrouter
from routes.payments import paymentrouter
from routes.booking import bookingRouter
from routes.offers import offerRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],         # Allows all HTTP methods
    allow_headers=["*"],
)

#Include Routes
app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(eventRouter)
app.include_router(companyRouter)
app.include_router(reviewRouter)
app.include_router(feedbackRouter)
app.include_router(faqRouter)
app.include_router(ticketrouter)
app.include_router(paymentrouter)
app.include_router(bookingRouter)
app.include_router(offerRouter)

#Connect to Db
db = MongoDBSingleton().get_database()
@app.get("/")
def root():
    if db is not None:
        return {"message":"DB connect Successfully"}
    return {"message":"Connection Failure"}