from time import perf_counter
from fastapi import FastAPI, Request, Response


app = FastAPI()

...

# Append new lines in the log file
def add_log(log: str) -> None:
    with open("file.log", 'a') as file:
        file.write(f"{log}\n")


# Add custom middleware
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()

    response: Response = await call_next(request)

    end = perf_counter()
    time_taken = round(end - start, 2)

    add_log.delay(f"{request.method} {request.url} ({response.status_code}) {time_taken} s")

    return response


# An endpoint to test above middleware
@app.get("/shipment")
def get_shipment(id: int):
    return dict(
        id=id,
        content="mysterious",
        status="in_transit",
    )