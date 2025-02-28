from fastapi import APIRouter

offerRouter = APIRouter(
    prefix="/offers",
    tags=["offers"],
)

@offerRouter.get("/")
async def get_offers():
    pass

@offerRouter.post("/")
async def create_offer():
    pass

@offerRouter.get("/{offer_id}")
async def get_offer(offer_id: int):
    pass

@offerRouter.put("/{offer_id}")
async def update_offer(offer_id: int):
    pass

@offerRouter.delete("/{offer_id}")
async def delete_offer(offer_id: int):
    pass

@offerRouter.get("/event/{event_id}")
async def get_event_offers(event_id: int):
    pass

@offerRouter.get("/")
async def get_offer_by_type(offer_type: str):
    pass