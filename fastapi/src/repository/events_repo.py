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
        print(f"inside findevents")
        events_cursor = events_collection.find({}, {'_id': 0})
        events = events_cursor.to_list(length=None)
        print(f"events repo {events}")
        return events
    
    @staticmethod
    def findEventById(eventId: str):
        """
        Find an event by its ID
        Args:
            eventId (str): The ID of the event to find
        Returns:
            dict: The event document if found, None if not found
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
            
            if not ObjectId.is_valid(eventId):
                raise Exception("Invalid event ID format")
                
            event = events_collection.find_one({"_id": ObjectId(eventId)})
            return event
            
        except Exception as e:
            raise Exception(f"Error finding event: {str(e)}")
        
    @staticmethod
    def findEventByName(eventName: str):
        """
        Find an event by its name
        
        Args:
            eventName (str): The name of the event to find
            
        Returns:
            list: List of event documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
                
            if not eventName or not isinstance(eventName, str):
                raise Exception("Invalid event name")
                
            cursor = events_collection.find({"name": eventName})
            events = list(cursor)  # Convert cursor to list
            return events
            
        except Exception as e:
            raise Exception(f"Error finding event by name: {str(e)}")
    
    @staticmethod
    def findEventByCategory(eventCategory : str):
        return events_collection.find_one({"category": eventCategory})
    
    @staticmethod
    def findEventByStateName(stateName: str):
        """
        Find events by state name
        
        Args:
            stateName (str): The state name to find events for
            
        Returns:
            list: List of event documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
                
            if not stateName or not isinstance(stateName, str):
                raise Exception("Invalid state name")
                
            cursor = events_collection.find({"state": stateName})
            events = list(cursor)  # Convert cursor to list
            return events
            
        except Exception as e:
            raise Exception(f"Error finding events by state: {str(e)}")
    
    @staticmethod
    def findEventByCityName(stateName: str, cityName: str):
        """
        Find events by state name and city name
        
        Args:
            stateName (str): The state name to find events for
            cityName (str): The city name to find events for
            
        Returns:
            list: List of event documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
                
            if not stateName or not isinstance(stateName, str):
                raise Exception("Invalid state name")
                
            if not cityName or not isinstance(cityName, str):
                raise Exception("Invalid city name")
                
            cursor = events_collection.find({"state": stateName, "city": cityName})
            events = list(cursor)  # Convert cursor to list
            return events
            
        except Exception as e:
            raise Exception(f"Error finding events by city: {str(e)}")
        
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