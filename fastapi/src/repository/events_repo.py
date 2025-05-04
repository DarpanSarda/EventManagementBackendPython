from models import event
from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.eventSchema import EventSchemaAdminReq

db = MongoDBSingleton().get_database()
if db is not None:
    events_collection = db["events"]
else:
    events_collection = None


class EventsRepo():

    @staticmethod
    async def findEvents():
        try:
            if events_collection is None:
                raise Exception("Database connection not initialized")
    
            print("Fetching events from database...")
            # Remove the '_id': 0 projection to allow ID conversion
            events_cursor = events_collection.find({})
            events = []
            for event in events_cursor:
                events.append(event)

            # Transform the events to handle ObjectId
            transformed_events = []
            for event in events:
                event['_id'] = str(event['_id'])  # Convert ObjectId to string
                transformed_events.append(event)
    
            print(f"Found {len(transformed_events)} events")
            return transformed_events
    
        except Exception as e:
            print(f"Error in findEvents: {str(e)}")
            raise Exception(f"Failed to fetch events: {str(e)}")
    
    @staticmethod
    def findEventById(eventId : str):
        return events_collection.find_one({"_id": ObjectId(eventId)})
    
    @staticmethod
    def findEventByName(eventName : str):
        return events_collection.find_one({"name": eventName})
    
    @staticmethod
    def findEventByCategory(eventCategory : str):
        return events_collection.find_one({"category": eventCategory})
    
    @staticmethod
    def findEventByStateName(stateName : str):
        return events_collection.find_one({"state": stateName})
    
    @staticmethod
    def findEventByCityName(stateName : str , cityName : str):
        return events_collection.find_one({"state": stateName , "city": cityName})
    
    @staticmethod
    def createEvent(event : EventSchemaAdminReq):
        """Create event"""
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
            returned_event = events_collection.insert_one(event)
            if returned_event is not None:
                return event
            return None
        except Exception as e:
            raise Exception(f"Error creating event: {str(e)}")