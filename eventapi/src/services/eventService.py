from repository.events_repo import EventsRepo
from schemas.eventSchema import EventSchemaAdminReq

class EventService:
    @staticmethod
    async def getEvents():
        """Get all events"""
        print(f"inside event service")
        events = await EventsRepo.findEvents()
        print(f"event service {events}")
        return events
    
    @staticmethod
    async def getEventById(eventId: str):
        """
        Get event by ID from the database
        
        Args:
            eventId (str): The ID of the event to retrieve
            
        Returns:
            dict: The event object if found
            None: If event is not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            event = await EventsRepo.findEventById(eventId)
            if not event:
                return None
            return event
        except Exception as e:
            print(f"Error retrieving event: {str(e)}")
            raise Exception(f"Failed to retrieve event: {str(e)}")
    
    @staticmethod
    def getEventByName(eventName: str):
        """
        Get event by name from the database
        
        Args:
            eventName (str): The name of the event to retrieve
            
        Returns:
            dict: The event object if found
            None: If event is not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not eventName or not isinstance(eventName, str):
                raise Exception("Invalid event name provided")
                
            event = EventsRepo.findEventByName(eventName)
            if not event:
                return None
            return event
            
        except Exception as e:
            print(f"Error retrieving event by name: {str(e)}")
            raise Exception(f"Failed to retrieve event by name: {str(e)}")
    
    @staticmethod
    def getEventByCategory(eventCategory : str):
        """Get event by category"""
        event = EventsRepo.findEventByCategory(eventCategory)
        return event
    
    @staticmethod
    def getEventByStateName(stateName: str):
        """
        Get events by state name from the database
        
        Args:
            stateName (str): The name of the state to retrieve events for
            
        Returns:
            list: List of event objects if found
            None: If no events are found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not stateName or not isinstance(stateName, str):
                raise Exception("Invalid state name provided")
                
            events = EventsRepo.findEventByStateName(stateName)
            if not events:
                return None
            return events
            
        except Exception as e:
            print(f"Error retrieving events by state: {str(e)}")
            raise Exception(f"Failed to retrieve events by state: {str(e)}")
    
    @staticmethod
    def getEventByCityName(stateName: str, cityName: str):
        """
        Get events by state name and city name from the database
        
        Args:
            stateName (str): The name of the state to retrieve events for
            cityName (str): The name of the city to retrieve events for
            
        Returns:
            list: List of event objects if found
            None: If no events are found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not stateName or not isinstance(stateName, str):
                raise Exception("Invalid state name provided")
                
            if not cityName or not isinstance(cityName, str):
                raise Exception("Invalid city name provided")
                
            events = EventsRepo.findEventByCityName(stateName, cityName)
            if not events:
                return None
            return events
            
        except Exception as e:
            print(f"Error retrieving events by city: {str(e)}")
            raise Exception(f"Failed to retrieve events by city: {str(e)}")
    
    @staticmethod
    def createEvent(event : EventSchemaAdminReq):
        """Create event"""
        try:
            returned_event = EventsRepo.createEvent(event)
            return returned_event
        except Exception as e:
            print(f"Error creating event: {str(e)}")
            return None
        
    @staticmethod
    async def updateEvent(eventId: str, event: EventSchemaAdminReq):
        """
        Update event in the database
        
        Args:
            eventId (str): The ID of the event to update
            event (EventSchemaAdminReq): The updated event data
            
        Returns:
            dict: The updated event object if successful
            None: If update fails
            
        Raises:
            Exception: If there's an error during the database operation
        """
        print(f"eventId : {eventId}")
        try:
            event_data = event.model_dump(exclude_unset=True, exclude_none=True)
            print(f"inside event service update {event_data}")
            updated_event = await EventsRepo.updateEvent(eventId, event_data)
            print(f"event updated : {updated_event}")
            if not updated_event:
                return None
            return updated_event
        except Exception as e:
            print(f"Error updating event: {str(e)}")
            raise Exception(f"Failed to update event: {str(e)}")
        
    @staticmethod
    async def getEventsBycategory(category: str):
        """
        Get events by category from the database

        Args:
            category (str): The category of events to retrieve

        Returns:
            list: A list of events that match the given category
            None: If no events are found
        """
        try:
            events = await EventsRepo.geteventbycategory(category)
            return events or []
        except Exception as e:
            print(f"Error getting events by category: {str(e)}")
            raise Exception(f"Failed to get events by category: {str(e)}")