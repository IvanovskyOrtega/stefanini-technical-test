"""Concurrent tasks module."""
import asyncio
from time import time
from typing import Any, Dict

from aiohttp import ClientSession


async def task(delay: int) -> Dict[str, Any]:
    """async_example.

    Runs a simple async HTTP GET request to https://httpbin.org/delay/{delay}.

    Arguments
    ----------
    delay : int
        The time delay that'll be applied to the request.

    Returns
    -------
    Dict[str, Any] : The JSON response as a Python dictionary.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(task(0))
    {}
    """
    url = f"https://httpbin.org/delay/{delay}"
    print(f"Sending request to: {url}")
    async with ClientSession() as session:
        async with session.get(url) as response:
            print(f"Request for {url} suceed!")
            return await response.json()


def run_concurrent_tasks() -> float:
    """run_concurrent_tasks.

    Runs a list of tasks with different values for the delay.
    An evetloop is created to run the concurrent tasks.

    Returns
    -------
    float : The amount of seconds that took to process the tasks.

    Examples
    --------
    >>> run_async_tasks()
    0.28911447525024414
    """
    loop = asyncio.get_event_loop()
    tasks = [task(delay) for delay in range(10)]
    begin = time()
    values = loop.run_until_complete(asyncio.gather(*tasks))
    # print(values)
    end = time()
    total = end - begin
    print(f"Total: {total} seconds")
    loop.close()
    return total


if __name__ == "__main__":
    run_concurrent_tasks()
