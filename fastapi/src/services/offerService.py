from typing import List, Optional, Dict
from datetime import datetime
from repository.offers_repo import OffersRepo
from schemas.offerSchema import OfferSchemaReq, OfferSchemaRes
from models.offers import DiscountType

class OfferService:
    @staticmethod
    async def create_offer(offer_data: OfferSchemaReq) -> Dict:
        """Create a new offer"""
        try:
            print("Inside offer service")
            # Add tracking fields
            offer_dict = offer_data.dict()
            offer_dict["created_at"] = datetime.utcnow()
            offer_dict["updated_at"] = datetime.utcnow()
            offer_dict["is_active"] = True
            
            result = await OffersRepo.create_offer(offer_dict)
            print("Inserted offer:", result)
            return result
        except Exception as e:
            raise Exception(f"Failed to create offer: {str(e)}")

    @staticmethod
    async def get_all_offers(active_only: bool = False) -> List[Dict]:
        """Get all offers with optional active only filter"""
        try:
            offers = await OffersRepo.find_all_offers(active_only)
            return offers
        except Exception as e:
            raise Exception(f"Failed to fetch offers: {str(e)}")

    @staticmethod
    async def get_offer_by_promo_code(promo_code: str) -> Optional[Dict]:
        """
        Get offer by promo code
        """
        try:
            offer = await OffersRepo.find_offer_by_promo_code(promo_code)
            if not offer:
                return "Offer with promo code not found"
            return offer
        except Exception as e:
            raise Exception(f"Failed to fetch offer: {str(e)}")

    @staticmethod
    async def get_offer_by_id(offer_id: str) -> Optional[Dict]:
        """Get offer by ID"""
        try:
            offer = await OffersRepo.find_offer_by_id(offer_id)
            if not offer:
                raise Exception("Offer not found")
            return offer
        except Exception as e:
            raise Exception(f"Failed to fetch offer: {str(e)}")

    @staticmethod
    async def update_offer(offer_id: str, offer_data: OfferSchemaReq) -> Dict:
        """Update an existing offer"""
        try:
            # Verify offer exists
            existing_offer = await OffersRepo.find_offer_by_id(offer_id)
            if not existing_offer:
                raise Exception("Offer not found")
            
            # Update tracking fields
            update_data = offer_data.dict()
            update_data["updated_at"] = datetime.utcnow()
            
            updated_offer = await OffersRepo.update_offer(offer_id, update_data)
            if not updated_offer:
                raise Exception("Failed to update offer")
            return updated_offer
        except Exception as e:
            raise Exception(f"Failed to update offer: {str(e)}")

    @staticmethod
    async def delete_offer(offer_id: str) -> bool:
        """Delete an offer"""
        try:
            result = await OffersRepo.delete_offer(offer_id)
            if not result:
                raise Exception("Offer not found or couldn't be deleted")
            return True
        except Exception as e:
            raise Exception(f"Failed to delete offer: {str(e)}")

    @staticmethod
    async def get_featured_offers() -> List[Dict]:
        """Get all featured offers"""
        try:
            offers = await OffersRepo.find_featured_offers()
            return offers
        except Exception as e:
            raise Exception(f"Failed to fetch featured offers: {str(e)}")

    @staticmethod
    async def calculate_discount(offer_id: str, amount: float, payment_method: str) -> float:
        """Calculate discount amount for a given offer and purchase amount"""
        try:
            offer = await OffersRepo.find_offer_by_id(offer_id)
            if not offer:
                raise Exception("Offer not found")

            # Validate offer
            if not offer["is_active"]:
                raise Exception("Offer is not active")
            if datetime.utcnow() > offer["valid_till"]:
                raise Exception("Offer has expired")
            if payment_method not in offer["valid_payment_methods"]:
                raise Exception("Payment method not valid for this offer")
            if amount < offer["minimum_order_value"]:
                raise Exception(f"Minimum order value is {offer['minimum_order_value']}")

            # Calculate discount
            if offer["discount_type"] == DiscountType.PERCENTAGE:
                discount = (amount * offer["discount_value"]) / 100
                return min(discount, offer["maximum_discount"])
            else:
                return min(offer["discount_value"], amount)

        except Exception as e:
            raise Exception(f"Failed to calculate discount: {str(e)}")