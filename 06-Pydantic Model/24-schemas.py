from pydantic import BaseModel, Field


class Shipment(BaseModel):
    content: str = Field(
        description="Contents of the shipment",
        # max length of characters
        max_length=30,
        # can use min length as well
        min_length=8,
    )
    weight: float = Field(
        description="Weight of the shipment in kilograms (kg)",
        # [l]ess than or [e]qual to
        le=25,
        # [g]reater than or [e]qual to
        ge=1,
    )
    destination: int | None = Field(
        description="Destination Zipcode. If not provided will be sent off to a random location",
        # fixed default value
        default=11000,
        # or generate at runtime using default_factory
        # here a random integer 
        # default_factory=lambda : randint(11000, 11999),
    )
