from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


app = FastAPI()

shipments = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}


@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:
    # Check for shipment with given id
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!"
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, int]:
    # Validate weight
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kgs"
        )
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }
    # Return id for later use
    return {"id": new_id}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
