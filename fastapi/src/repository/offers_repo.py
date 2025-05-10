from typing import List, Optional
from bson import ObjectId
from db.connect import MongoDBSingleton
from models.offers import Offers
from datetime import datetime

db = MongoDBSingleton().get_database()
if db is not None:
    offers_collection = db["offers"]
else:
    offers_collection = None

class OffersRepo:
    @staticmethod
    async def create_offer(offer_data: Offers) -> dict:
        print("Inside offer repo")
        """Create a new offer"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
            result = offers_collection.insert_one(offer_data)
            print("Inserted offer:", result.inserted_id)
            if result.inserted_id:
                offer = await OffersRepo.find_offer_by_id(str(result.inserted_id))
                return offer
            raise Exception("Failed to create offer")
        except Exception as e:
            raise Exception(f"Error creating offer: {str(e)}")

    @staticmethod
    async def find_offer_by_id(offer_id: str) -> Optional[dict]:
        """Find an offer by ID"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            offer = offers_collection.find_one({"_id": ObjectId(offer_id)})
            return offer
        except Exception as e:
            raise Exception(f"Error finding offer: {str(e)}")

    @staticmethod
    async def find_all_offers(active_only: bool = False) -> List[dict]:
        """Find all offers with optional active only filter"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            filter_query = {"is_active": True} if active_only else {}
            cursor = offers_collection.find(filter_query)
            offers = []
            for offer in cursor:
                offers.append(offer)
            return offers
        except Exception as e:
            raise Exception(f"Error finding offers: {str(e)}")

    @staticmethod
    async def update_offer(offer_id: str, offer_data: dict) -> Optional[dict]:
        """Update an offer"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            # Remove _id if present in update data
            if "_id" in offer_data:
                del offer_data["_id"]
                
            result = await offers_collection.update_one(
                {"_id": ObjectId(offer_id)},
                {"$set": offer_data}
            )
            
            if result.modified_count:
                return await OffersRepo.find_offer_by_id(offer_id)
            return None
        except Exception as e:
            raise Exception(f"Error updating offer: {str(e)}")

    @staticmethod
    async def delete_offer(offer_id: str) -> bool:
        """Delete an offer"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            result = await offers_collection.delete_one({"_id": ObjectId(offer_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Error deleting offer: {str(e)}")

    @staticmethod
    async def find_active_offers_by_payment_method(payment_method: str) -> List[dict]:
        """Find active offers for a specific payment method"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            current_date = datetime.utcnow()
            cursor = offers_collection.find({
                "is_active": True,
                "valid_till": {"$gt": current_date},
                "valid_payment_methods": payment_method
            })
            offers = await cursor.to_list(length=None)
            return offers
        except Exception as e:
            raise Exception(f"Error finding offers by payment method: {str(e)}")

    @staticmethod
    async def find_offer_by_promo_code(promo_code: str) -> Optional[dict]:
        """Find an offer by its promo code"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            offer = offers_collection.find_one({"promo_code": promo_code})
            return offer
        except Exception as e:
            raise Exception(f"Error finding offer by promo code: {str(e)}")
    
    @staticmethod
    async def find_featured_offers() -> List[dict]:
        """Find all featured offers"""
        try:
            if offers_collection is None:
                raise Exception("Database connection not initialized")
                
            current_date = datetime.utcnow()
            cursor = offers_collection.find({
                "is_active": True,
                "is_featured": True,
                "valid_till": {"$gt": current_date}
            })
            offers = await cursor.to_list(length=None)
            return offers
        except Exception as e:
            raise Exception(f"Error finding featured offers: {str(e)}")

