"""Main module."""
from os import wait
from time import sleep

from examples.asynchronism import run_async_tasks_in_background
from examples.concurrency import run_concurrent_tasks
from examples.parallelism import run_parallel_taks
from examples.semaphore import run_semaphore_example
from examples.workerpool import run_workerpool_tasks


def wait_for(n: int):
    print("Next example will run in...")
    while n >= 0:
        print(f"{n}...")
        n -= 1
    print("Now!")


def main():
    print("Running async tasks...")
    run_async_tasks_in_background()
    print("Async tasks completed!")
    wait_for(5)
    print("Running concurrent tasks...")
    run_concurrent_tasks()
    print("Concurrent tasks completed!")
    wait_for(5)
    print("Running parallel tasks...")
    run_parallel_taks()
    print("Parallel tasks completed!")
    wait_for(5)
    print("Running semaphore tasks...")
    run_semaphore_example()
    print("Semaphore tasks completed!")
    wait_for(5)
    print("Running workerpool tasks...")
    run_workerpool_tasks()
    print("Workerpool tasks completed!")


if __name__ == "__main__":
    main()
