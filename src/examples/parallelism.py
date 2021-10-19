"""Parallelism with Python's multiprocessing module."""
from io import BytesIO
from os import stat
from multiprocessing import Process
from requests import get
from time import time
from typing import Tuple
from uuid import uuid4

from PIL import Image


allowed_types = set(["image/jpeg", "image/png", "image/jpg"])


def task(url: str, p_num: int) -> Tuple[bool, int]:
    """task.

    Download a file image with the given url and halfs its resolution.

    Arguments
    ----------
    url : str
        The image url.
    p_num : int
        The process number.

    Returns
    -------
    Tuple[bool, int] : (`True`, file_size_in_bytes) if downloaded, (`False`, 0)
        otherwise.

    Examples
    --------
    >>> task(url,)
    (True, 86427)
    """
    try:
        print(f"[PROCESS-{p_num}] Downloading image from {url}")
        response = get(url, allow_redirects=True)
        content_type = response.headers.get("Content-Type")

        if content_type not in allowed_types:
            raise Exception("Not an allowed extension.")

        filename = f"{str(uuid4())}.{content_type.split('/')[-1]}"
        image = Image.open(BytesIO(response.content))
        width, lenght = image.size
        new_size = width // 2, lenght // 2
        image = image.resize(new_size)
        filepath = f"./downloads/images/{filename}"
        image.save(filepath)
        print(f"[PROCESS-{p_num}] Download completed!")
        return True, stat(filepath).st_size
    except Exception as e:
        print("[PROCESS-%s] Error while downloading the file: %s" % (p_num, e))
        return False, 0


def run_parallel_taks() -> float:
    """run_parallel_taks.

    Run the task in a set of parallel processes. Each process download an
    image from an url.

    Returns
    -------
    float : The time that took to perform the downloads.

    Examples
    --------
    >>> run_parallel_taks()
    [PROCESS-0] Downloading image from https://upload...
    [PROCESS-1] Downloading image from https://upload...
    [PROCESS-1] Download completed!
    [PROCESS-0] Download completed!
    Total: 1.616037130355835 seconds
    """
    urls = []
    with open("./files/image-urls.txt", "r") as f:
        urls = f.readlines()
        urls = [url.replace("\n", "") for url in urls]
    processes = []
    for num, url in enumerate(urls):
        processes.append(Process(target=task, args=(url, num)))
    begin = time()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    end = time()
    total = end - begin
    print(f"Total: {total} seconds")
    return total


if __name__ == "__main__":
    run_parallel_taks()
