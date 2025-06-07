from fastapi import FastAPI
from routers.audit import audit_router
from fastapi.middleware.cors import CORSMiddleware
from services.kafka.consumer import KafkaConsumerService, custom_audit_handler
import threading
import asyncio

app = FastAPI()
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

#initialize Kafka Consumer
kafka_consumer = KafkaConsumerService()

def run_async_consumer():
    """Helper function to run async consumer in thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(kafka_consumer.start_consuming_async(custom_audit_handler))
    finally:
        loop.close()

async def start_kafka_consumer():
    await kafka_consumer.start_consuming(custom_audit_handler)

@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=run_async_consumer, daemon=True)
    consumer_thread.start()
    print("Kafka Consumer started in a separate thread.")

@app.on_event("shutdown")
def shutdown_event():
    kafka_consumer.stop_consuming()
    print("🛑 Kafka Consumer stopped")

# Include the audit router
app.include_router(audit_router, prefix="/api/v1", tags=["audits"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Audit API. Use /api/v1/audits for audit operations."}