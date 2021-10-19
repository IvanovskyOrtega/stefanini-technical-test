"""Sempahore implemetation in Python."""
from threading import Thread, Semaphore
from time import sleep
from typing import List

from faker import Faker
from ipwhois import IPWhois

valid_ips: List = []  # The shared resource


def get_address_info(address: str, semaphore: Semaphore, t_num: int):
    """get_address_info.

    Get the IPV4 address info using IPWhois. If the result of IPWhois is not
    None, the result is added to the shared list. The semaphore allows
    only 3 threads to access at the same time to the shared list.

    Arguments
    ----------
    address : str
        The address to get its information.
    semaphore : Semaphore
        The Python threading.Semaphore instance.
    t_num : int
        The number ot the thread.

    Examples
    --------
    >>> sem = threading.Semaphore()
    >>> t = Thread(target=get_address_info, args=("21.177.64.80", sem, 1))
    >>> t.start()
    [THREAD-1] Acquiring access to shared resource
    [THREAD-1] Releasing access to shared resource
    [..., ...,]
    """
    try:
        obj = IPWhois(address=address)
        result = obj.lookup_whois()
        if result is None:
            return
        with semaphore:  # Same as semaphore.acquire() (release is implicit)
            print(f"[THREAD-{t_num}] Acquiring access to shared resource")
            valid_ips.append((address, result))
            sleep(3)
        print(f"[THREAD-{t_num}] Releasing access to shared resource")
    except Exception as e:
        print(f"[THREAD-{t_num}] Exception {e}")


def run_semaphore_example():
    """run_semaphore_example.

    Runs the semaphore example. It creates a list of IPV4 IP addresses with
    faker library that will be arguments for the get_address_info function.
    A set of threads is created an then invoked to run the target function.
    Each thread access a shared resource `valid_ips` whic is a Python List.
    Once completed, the list is printed to stdout.

    Examples
    --------
    >>> run_semaphore_example()
    [THREAD-1] Acquiring access to shared resource
    [THREAD-2] Acquiring access to shared resource
    [THREAD-1] Releasing access to shared resource
    [THREAD-1] Releasing access to shared resource
    [('6.236.186.61',{...}), ('164.113.239.191', {...})]
    """
    faker = Faker()
    semaphore = Semaphore(4)  # Allow access for 3 Threads at time
    ips = [faker.ipv4() for _ in range(20)]
    threads = []
    for t_num, ip in enumerate(ips):
        t = Thread(target=get_address_info, args=(ip, semaphore, t_num))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(valid_ips)


if __name__ == "__main__":
    run_semaphore_example()
