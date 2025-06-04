import asyncio
import time

from rich import print


async def endpoint(route: str) -> str:
    print(f">> handling {route}")
    
    # emulate database delay
    await asyncio.sleep(1)
    
    print(f"<< response {route}")

    # will be returned from coroutine
    return route


async def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=4",
        "GET /shipment?id=3",
    )

    start = time.perf_counter()

    # Task Group
    async with asyncio.TaskGroup() as task_group:
        tasks =  [
            # on task creation, corountine will
            # be executed as well
            task_group.create_task(endpoint(route))
            for route in tests
        ]

        print(
            "Task[0] Result: ",
            # manually await result for task coroutine
            await tasks[0]
        )

    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f}s")


# Run server with asyncio
asyncio.run(
    server(),
)
