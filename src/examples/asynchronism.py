"""Asynchronous tasks module."""
import asyncio
from json import loads
from threading import Thread
from time import sleep
from typing import Any, Dict, Coroutine, List
from uuid import uuid4

import aiofiles
from aiohttp import ClientSession, StreamReader


QUOTES_API_URL: str = "https://zenquotes.io/api/random/"


async def read_pdf_urls_list() -> Coroutine[None, None, List[str]]:
    """read_pdf_urls_list.

    Read the text file that contains a list of PDF urls using aiofiles.

    Returns
    -------
    Coroutine[None, None, List[str]] : A Python coroutine that once completed,
        returns a List of urls.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(read_pdf_urls_list())
    ["...", "...",]
    """
    pdfs = []
    async with aiofiles.open("./files/pdfs-list.txt", "r") as input_file:
        pdfs = await input_file.readlines()
        pdfs = [pdf.replace("\n", "") for pdf in pdfs]
    return pdfs


async def write_file(
    filepath: str, content: StreamReader
) -> Coroutine[None, None, None]:
    """write_file.

    Write asynchronously the bytes from a aiohttp.StreamReader to a file.

    Arguments
    ----------
    filepath : str
        The path to the output file.
    content : StreamReader
        The aiohttp.StreamReader object to read the bytes.

    Returns
    -------
    Coroutine[None, None, None] : A Python coroutine.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(write_file("./files/1.pdf", content))
    >>>
    """
    async with aiofiles.open(filepath, "wb") as output_file:
        while True:
            chunk = await content.read(2048)
            if chunk in (None, b""):
                break
            await output_file.write(chunk)


async def download_file(
    pdf_url: str, pdf_num: int
) -> Coroutine[None, None, None]:
    """download_file.

    Async download a file from a given url, it checks that the content/type is
    application/pdf.

    Arguments
    ----------
    pdf_url : str
        The pdf url.
    pdf_num : int
        The number of the pdf to download.

    Returns
    -------
    Coroutine[None, None, None] : A Python coroutine.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(download_file("...", "1"))
    [ASYNC] PDF 1 downloaded to filesystem!
    >>>
    """
    async with ClientSession() as session:
        async with session.get(pdf_url, allow_redirects=True) as response:
            content_type = response.headers.get("Content-Type")

            if content_type != "application/pdf":
                print("[ASYNC] Not an allowed extension.")
                return

            filepath = f"./downloads/pdfs/{str(uuid4())}.pdf"

            await write_file(filepath, response.content)

            print(f"[ASYNC] PDF {pdf_num} downloaded to filesystem!")


async def download_pdfs() -> Coroutine[None, None, None]:
    """download_pdfs.

    Async download a list of pdfs.

    Returns
    -------
    Coroutine[None, None, None] : A Python Coroutine.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(download_pdfs())
    [ASYNC] Downloading PDF 1...
    [ASYNC] PDF 1 downloaded to filesystem!
    >>>
    """
    try:
        pdf_urls = await read_pdf_urls_list()
        for pdf_num, pdf_url in enumerate(pdf_urls):
            print(f"[ASYNC] Downloading PDF {pdf_num}...")
            await download_file(pdf_url, pdf_num)
    except Exception as e:
        print("[ASYNC] Error while downloading the file: %s" % e)


async def get_quote() -> Coroutine[None, None, Dict[str, Any]]:
    """get_quote.

    Get a quote from a Quotes API asynchronously.

    Returns
    -------
    Coroutine[None, None, Dict[str, Any]] : A Python Coroutine that once
        completed, returns the JSON response as a Python dictionary.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(get_quote())
    {"q": "...", "a": "..."}
    """
    async with ClientSession() as session:
        async with session.get(QUOTES_API_URL) as response:
            quotes = await response.text()
            quotes = loads(quotes)
            return quotes[0]


async def get_quotes() -> Coroutine[None, None, None]:
    """get_quotes.

    Get 20 quotes from a Quotes API asynchronously. The API is called with a
    6 seconds delay (due to API limitations). Once completed the quote is
    shown to stdout.

    Returns
    -------
    Coroutine[None, None, None] : [description].

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> result = loop.run_until_complete(get_quotes())
    Charles Dickens: 'A loving heart is the truest wisdom.'
    Publilius Syrus: 'To do two things at once is to do neither.'
    ...
    >>>
    """
    for _ in range(20):
        await asyncio.sleep(6)  # API is limited to 5 requests per 30 seconds
        quote = await get_quote()
        print(f"[ASYNC] {quote['a']}: '{quote['q']}'")


def run_async_tasks(loop: asyncio.AbstractEventLoop):
    """run_async_tasks.

    Run the download_pdfs and get_quotes tasks with asyncio.

    Arguments
    ----------
    loop : asyncio.AbstractEventLoop
        The asyncio eventloop.

    Examples
    --------
    >>> loop = asyncio.get_event_loop()
    >>> run_async_tasks(loop,)
    [ASYNC] Downloading PDF 0...
    [ASYNC] PDF 0 downloaded to filesystem!
    [ASYNC] Downloading PDF 1...
    [ASYNC] PDF 1 downloaded to filesystem!
    ...
    """
    asyncio.set_event_loop(loop)
    tasks = [download_pdfs(), get_quotes()]
    loop.run_until_complete(asyncio.gather(*tasks))


def run_async_tasks_in_background():
    """run_async_tasks_in_background.

    Run the async tasks simulating a non blocking task in the main thread.
    At the end we call `thread.join()` just for prevent running this example
    along the other ones.

    Examples
    --------
    >>> run_async_tasks_in_background()
    [MAIN] Task in running now in background without blocking the main task!
    [ASYNC] Downloading PDF 0...
    [ASYNC] PDF 0 downloaded to filesystem!
    [MAIN] And still running as non blocking!
    ...
    """
    loop = asyncio.get_event_loop()
    thread = Thread(target=run_async_tasks, args=(loop,))
    thread.start()
    print(
        "[MAIN]",
        "Task in running now in background without blocking the main task!",
    )
    sleep(5)
    print("[MAIN] And still running as non blocking!")
    sleep(5)
    print("[MAIN] We can keep doing stuff in the main thread/process.")
    sleep(5)
    print("[MAIN] Now we can call thread.join() to wait for its execution")
    thread.join()


if __name__ == "__main__":
    run_async_tasks_in_background()
