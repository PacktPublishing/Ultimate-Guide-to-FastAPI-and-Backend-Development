# Recieve arguments for decorator function
def custom_fence(fence: str = "+"):
    # Decorator function
    def add_fence(func):
        # Original function wrapper
        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))
        
        return wrapper
    
    return add_fence


# Use custom decorator
@custom_fence("x")
def log(text: str):
    print(text)


# Call function with defined name
log("ballon")


# Function Typing
from typing import Callable, Any

def decorator( func: Callable[[Any], None] ):
#              argument/s type ☝️    👆 return type
    pass