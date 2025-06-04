import asyncio
import time


async def endpoint(route: str) -> str:
    print(f">> handling {route}")
    
    # emulate database delay
    await asyncio.sleep(1)
    
    print(f"<< response {route}")

    return route


async def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=4",
        "GET /shipment?id=3",
    )

    start = time.perf_counter()

    # create tasks
    requests = [
        asyncio.create_task( endpoint(route) )
        for route in tests
    ]
    # run tasks with efficient waiting
    finished, pending = await asyncio.wait(requests)

    # get result from finished tasks
    for task in finished:
        print("Result:", task.result())

    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f}s")


# Run server
asyncio.run(server())
