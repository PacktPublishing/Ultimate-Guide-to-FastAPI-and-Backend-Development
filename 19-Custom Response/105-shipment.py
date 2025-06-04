from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.utils import TEMPLATE_DIR
from ..dependencies import  ShipmentServiceDep

router = APIRouter(prefix="/shipment", tags=["Shipment"])


templates = Jinja2Templates(TEMPLATE_DIR)

### Tracking details of shipment
@router.get("/track", include_in_schema=False)
async def get_tracking(request: Request, id: UUID, service: ShipmentServiceDep):
    # Check for shipment with given id
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context,
    )