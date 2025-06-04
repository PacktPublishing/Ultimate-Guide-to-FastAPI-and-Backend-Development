from typing import Any


# Custom class as type
class City:
    def __init__(self, name: str, location: int):
        self.name = name
        self.location = location


# Variable pype hints
text: str = "value"
pert: int = 90
temp: float = 37.5

# Two possible types
number: int | float = 12

# Sequence datatype
digits: list[int] = [1, 2, 3, 4, 5]

# Tuple like a list
table_5: tuple[int, ...] = (5, 10, 15, 20, 25)

# Tuple with 2 elements
hampshire = City("hamspshire", 2048593)
city_temp: tuple[City, float] = (hampshire, 20.5)

# Dictionary key and value hinting
shipment: dict[str, Any] = {
    "id": 12701,
    "weight": 1.2,
    "content": "wooden table",
    "status": "in transit",
}


# Hinting function argument and return type
def root(num: int | float, exp: float | None = .5) -> float:
    return pow(num, .5)
