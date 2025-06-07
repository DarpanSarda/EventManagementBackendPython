from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import datetime

class KafkaPublisher:
    def __init__(self):
        """
        Initialize the KafkaPublisher with a Kafka producer.
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers='localhost:9092',  # Adjust as necessary
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(2, 8, 0)  # Specify the API version if needed
            )
            print("Kafka Producer initialized.")
        except KafkaError as e:
            print(f"Error initializing Kafka Producer: {str(e)}")

    async def publish(self, user_id: str, action: str, details: dict):
        """
        Publish an event to the Kafka topic.
        
        Args:
            user_id (str): The ID of the user associated with the event.
            action (str): The action performed by the user.
            details (dict): Additional details about the event.
        """
        if not self.producer:
            print("Kafka Producer is not initialized.")
            return
        
        audit = {
            "userId": user_id,
            "action": action,
            "details": details,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        try:
            self.producer.send('audit_logs', value=audit)
            self.producer.flush()  # Ensure the message is sent
            print(f"Audit Log: {audit}")
            return True
        except KafkaError as e:
            print(f"Failed to publish event: {str(e)}") 
            return False
    
    def close(self):
        """
        Close the Kafka producer.
        """
        if self.producer:
            self.producer.close()
            print("Kafka Producer closed.")