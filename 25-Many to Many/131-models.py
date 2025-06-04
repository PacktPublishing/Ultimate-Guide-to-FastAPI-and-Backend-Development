from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class Order(SQLModel, table=True):
    shipment_id: UUID = Field(foreign_key="shipment.id", primary_key=True)
    product_id: UUID = Field(foreign_key="product.id", primary_key=True)

    created_at: datetime
    quantity: int = Field(default=1)

    shipment: "Shipment" = Relationship(back_populates="orders")
    product: "Product" = Relationship(back_populates="orders")


class Product(SQLModel, table=True):
    id: UUID
    title: str
    description: str
    price: float
    weight: float

    orders: list["Order"] = Relationship(
        back_populates="products",
    )


class Shipment(SQLModel, table=True):
    id: UUID
    status: str
    weight: float
    destination: str

    orders: list[Order] = Relationship(
        back_populates="shipments",
    )



# Create a new shipment
shipment = Shipment()


# Create products or get reference to, say from a cart
power_bank = Product()
artifical_plant = Product()
torch = Product()

# Define the links, as orders
order_power_bank = Order(
    shipment=shipment,
    product=power_bank,
)
# Specify extra fields if required
order_artifical_plant = Order(
    shipment=shipment,
    product=artifical_plant,
    quantity=4,
)

order_torch = Order(
    shipment=shipment,
    product=torch,
    quantity=4,
)

# Access the relationships from either side
shipment.orders[0].created_at
power_bank.orders[0].shipment
