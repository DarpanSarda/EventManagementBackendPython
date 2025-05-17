from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from schemas.offerSchema import OfferSchemaReq, OfferSchemaRes, AdminOfferSchemaReq
from services.offerService import OfferService
from datetime import datetime
from bson import ObjectId
from fastapi.responses import JSONResponse

offerRouter = APIRouter(
    prefix="/offers",
    tags=["offers"],
)

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    return data  # Return as is if it's not an ObjectId

@offerRouter.get("/", response_model=List[OfferSchemaRes])
async def get_offers(active_only: bool = Query(False, description="Filter active offers only")):
    """Get all offers with optional active only filter"""
    try:
        offers = await OfferService.get_all_offers(active_only)
        for offer in offers:
            offer['_id'] = str(offer['_id'])
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.get("/promo/{promo_code}")
async def get_offer_by_promo_code(promo_code: str):
    """Get offer by promo code"""
    try:
        offer = await OfferService.get_offer_by_promo_code(promo_code)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer with promo code not found"
            )
        offer['_id'] = str(offer['_id'])
        return offer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.post("/", status_code=status.HTTP_201_CREATED)
async def create_offer(offer: OfferSchemaReq):
    """Create a new offer"""
    try:
        print("Inside offer router")
        result = await OfferService.create_offer(offer)
        transformed_result = {
            **result,
            "_id": str(result["_id"]),
            "valid_till": result["valid_till"].isoformat(),
            "created_at": result["created_at"].isoformat() if "created_at" in result else None,
            "updated_at": result["updated_at"].isoformat() if "updated_at" in result else None
        }
        
        return transformed_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.get("/{offer_id}", response_model=OfferSchemaRes)
async def get_offer(offer_id: str):
    """Get offer by ID"""
    try:
        offer = await OfferService.get_offer_by_id(offer_id)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        offer['_id'] = str(offer['_id'])
        return offer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.put("/{offer_id}")
async def update_offer(offer_id: str, offer: AdminOfferSchemaReq):
    """Update an existing offer"""
    try:
        updated_offer = await OfferService.update_offer(offer_id, offer)
        print("Updated offer:", updated_offer)
        if updated_offer:
            updated_offer['_id'] = str(updated_offer['_id'])
            updated_offer["valid_till"] = updated_offer["valid_till"].isoformat()
            updated_offer["created_at"] = updated_offer["created_at"].isoformat() if "created_at" in updated_offer else None
            updated_offer["updated_at"] = updated_offer["updated_at"].isoformat() if "updated_at" in updated_offer else None
            print("jfksajdfdf")
            response = {
                "status": "success",
                "data": updated_offer,
                "message": "Event updated successfully",
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: str):
    """Delete an offer"""
    try:
        await OfferService.delete_offer(offer_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.get("/featured/", response_model=List[OfferSchemaRes])
async def get_featured_offers():
    """Get all featured offers"""
    try:
        offers = await OfferService.get_featured_offers()
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@offerRouter.post("/{offer_id}/calculate", status_code=status.HTTP_200_OK)
async def calculate_discount(
    offer_id: str, 
    amount: float = Query(..., gt=0),
    payment_method: str = Query(...)
):
    """Calculate discount for a given offer and amount"""
    try:
        discount = await OfferService.calculate_discount(offer_id, amount, payment_method)
        return {
            "offer_id": offer_id,
            "original_amount": amount,
            "discount_amount": discount,
            "final_amount": amount - discount
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )