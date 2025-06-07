from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import asyncio
from services.auditService import AuditService
from schemas.auditSchema import Audit

class KafkaConsumerService:
    def __init__(self, topics=['audit_logs'], group_id='audit_log_consumer_group'):
        """
        Initialize the KafkaConsumerService with a Kafka consumer.
        
        Args:
            topics (list): List of topics to subscribe to
            group_id (str): Consumer group ID
        """
        self.topics = topics
        self.group_id = group_id
        self.consumer = None
        self.running = False
        
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                bootstrap_servers='localhost:9092',  # Adjust as necessary
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',  # Start from beginning if no offset
                enable_auto_commit=True,
                auto_commit_interval_ms=1000,
                api_version=(2, 8, 0)  # Match producer API version
            )
            print(f"Kafka Consumer initialized for topics: {self.topics}")
        except KafkaError as e:
            print(f"Error initializing Kafka Consumer: {str(e)}")
            self.consumer = None

    async def start_consuming_async(self, message_handler=None):
        """
        Start consuming messages from Kafka topics with async support.
        
        Args:
            message_handler (callable): Optional async or sync message handler function
        """
        if not self.consumer:
            print("Kafka Consumer is not initialized.")
            return
        
        self.running = True
        print(f"Starting to consume messages from topics: {self.topics}")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                try:
                    # Check if handler is async or sync
                    if message_handler:
                        if asyncio.iscoroutinefunction(message_handler):
                            # Async handler - await it
                            await message_handler(message)
                        else:
                            # Sync handler - call directly
                            message_handler(message)
                    else:
                        # Default handler
                        self._default_message_handler(message)
                        
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    print(f"Message: {message.value}")
                    
        except KafkaError as e:
            print(f"Error consuming messages: {str(e)}")
        except KeyboardInterrupt:
            print("Consumer interrupted by user")
        finally:
            self.stop_consuming()

    def start_consuming(self, message_handler=None):
        """
        Synchronous version - kept for backward compatibility
        Only works with synchronous handlers
        """
        if not self.consumer:
            print("Kafka Consumer is not initialized.")
            return
        
        self.running = True
        print(f"Starting to consume messages from topics: {self.topics}")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                try:
                    # Use custom handler if provided, otherwise use default
                    if message_handler:
                        if asyncio.iscoroutinefunction(message_handler):
                            # For async handlers, we need to run them in event loop
                            try:
                                loop = asyncio.get_event_loop()
                                loop.run_until_complete(message_handler(message))
                            except RuntimeError:
                                # No event loop running, create one
                                asyncio.run(message_handler(message))
                        else:
                            message_handler(message)
                    else:
                        self._default_message_handler(message)
                        
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    print(f"Message: {message.value}")
                    
        except KafkaError as e:
            print(f"Error consuming messages: {str(e)}")
        except KeyboardInterrupt:
            print("Consumer interrupted by user")
        finally:
            self.stop_consuming()

    def _default_message_handler(self, message):
        """
        Default message handler for audit log messages.
        
        Args:
            message: Kafka message object
        """
        audit_log = message.value
        print(f"Received Audit Log:")
        print(f"  Topic: {message.topic}")
        print(f"  Partition: {message.partition}")
        print(f"  Offset: {message.offset}")
        print(f"  User ID: {audit_log.get('userId', 'N/A')}")
        print(f"  Action: {audit_log.get('action', 'N/A')}")
        print(f"  Timestamp: {audit_log.get('timestamp', 'N/A')}")
        print(f"  Details: {audit_log.get('details', {})}")
        print("-" * 50)

    def consume_single_message(self, timeout_ms=1000):
        """
        Consume a single message with timeout.
        
        Args:
            timeout_ms (int): Timeout in milliseconds
            
        Returns:
            dict: Message data or None if timeout
        """
        if not self.consumer:
            print("Kafka Consumer is not initialized.")
            return None
        
        try:
            message_pack = self.consumer.poll(timeout_ms=timeout_ms)
            
            for topic_partition, messages in message_pack.items():
                for message in messages:
                    return {
                        'topic': message.topic,
                        'partition': message.partition,
                        'offset': message.offset,
                        'value': message.value,
                        'timestamp': message.timestamp
                    }
            
            return None  # No messages received within timeout
            
        except KafkaError as e:
            print(f"Error polling for messages: {str(e)}")
            return None

    def stop_consuming(self):
        """
        Stop consuming messages and close the consumer.
        """
        self.running = False
        if self.consumer:
            self.consumer.close()
            print("Kafka Consumer stopped and closed.")

    def seek_to_beginning(self):
        """
        Seek to the beginning of all assigned partitions.
        """
        if not self.consumer:
            print("Kafka Consumer is not initialized.")
            return
        
        try:
            self.consumer.seek_to_beginning()
            print("Seeked to beginning of all partitions.")
        except KafkaError as e:
            print(f"Error seeking to beginning: {str(e)}")

    def commit_offsets(self):
        """
        Manually commit current offsets.
        """
        if not self.consumer:
            print("Kafka Consumer is not initialized.")
            return
        
        try:
            self.consumer.commit()
            print("Offsets committed successfully.")
        except KafkaError as e:
            print(f"Error committing offsets: {str(e)}")


# Example usage and custom message handler
async def custom_audit_handler(message):
    """
    Custom handler for audit log messages with additional processing.
    
    Args:
        message (KafkaMessage): Raw Kafka message object containing audit data
        
    Raises:
        ValueError: If required audit log fields are missing
        Exception: For other processing errors
    """
    try:
        # Extract value from Kafka message
        audit_log = message.value
        if not isinstance(audit_log, dict):
            raise ValueError("Invalid audit log format")

        # Validate required fields
        required_fields = ['userId', 'action', 'timestamp']
        if not all(field in audit_log for field in required_fields):
            raise ValueError("Missing required audit log fields")

        # Log the incoming audit
        print(f"📩 Received audit log: {audit_log}")

        # Save to database
        try:
            audit_model = Audit(
                 userId=audit_log['userId'],
                action=audit_log['action'],
                timestamp=audit_log['timestamp'],
                details=str(audit_log.get('details', {})),  # Convert details to string
                ip_adress=audit_log.get('ip_adress', '0.0.0.0'),  # Default IP if not provided
                status='SUCCESS',  # Default status
                api_path=audit_log.get('api_path', ''),  # Default empty path
                eventId=audit_log.get('eventId'),  # Optional field
                error_description=audit_log.get('error_description')  # Optional field
            )
            await AuditService.add_audits(audit_model)
            print(f"✅ Audit saved to database: {audit_log['userId']}")
        except Exception as db_error:
            print(f"❌ Database error: {str(db_error)}")
            raise

        # Process based on action type with improved logging
        action = audit_log.get('action', '').upper()
        user_id = audit_log['userId']
        timestamp = audit_log['timestamp']
        
        match action:
            case 'LOGIN':
                print(f"🔐 User {user_id} logged in at {timestamp}")
            case 'LOGOUT':
                print(f"🚪 User {user_id} logged out at {timestamp}")
            case 'DATA_ACCESS':
                details = audit_log.get('details', {})
                print(f"📊 User {user_id} accessed data: {details}")
            case _:
                print(f"ℹ️  User {user_id} performed: {action}")

    except ValueError as ve:
        print(f"❌ Validation error: {str(ve)}")
        # You might want to send invalid messages to a dead letter queue
    except Exception as e:
        print(f"❌ Error processing audit log: {str(e)}")
        raise
