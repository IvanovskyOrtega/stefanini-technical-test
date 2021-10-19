# Stefanini Technical test

This project contains my Stefanini Technical Test code.

## Content

- [Dependencies](#Dependencies)
- [VSCode setup](#VSCode-setup)
- [Running the examples](#Running-the-examples)
- [Undestanding the solution](#Understanding-the-solution)
    - [Asynchronism](#Asynchronism)
    - [Concurrency](#Concurrency)
    - [Parallelism](#Parallelism)
    - [Semaphore](#Semaphore)
    - [Workerpool](#Workerpool)

## Dependencies

To properly run the project you need the following dependencies:

|Tool/Program|Version|
|-|-|
|docker|20.10.8|
|python|3.9.5|
|python-virtualenv|20.8.0|
|python pip|20.3.4|
|vscode (optional)|1.59.1|

It should run without any problem under Linux environments. Older versions may work, but properly execution is not ensured.

## VSCode setup

To have linting, code auto-formatting, support and autodocstring generator with the [.pydocstyle.mustache](.pydocstyle.mustache) template. You need to run the following command on the project's root path:

```bash
technical-test/ $ make environ
```

A VSCode restart on the project may be required to have the linters and formaters to work properly.

The last step is to install the following extension to VSCode: https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring

Now everthing is ready to run the project. The VSCode settings in [.vscode/setting.json](.vscode/setting.json) will replace the default settings for this project.

## Running the examples

Open a VSCode terminal or your prefered terminal in the project's root path and run the following commands:

```bash
technical-test/ $ make build && make run-docker
```

> **_Note:_** If you don't have docker installed in your Linux distribution, but have Python 3.9.5, you may use `make run-python` instead `make build && make run-docker`

## Understanding the solution:

Let's understand the logs generated by the previous execution.

### Asynchronism

*Full implementation and documented code:* [./src/examples/asynchronism.py](./src/examples/asynchronism.py)

For the asynchronous execution we download PDF files and get some quotes from a Quotes API in background as `async` functions running inside a thread, without blocking the main thread (which is the main feature of asynchronous execution).

Here is the `run_async_tasks_in_background` function implementation:

```python
def run_async_tasks_in_background():
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
```

We can identify the messages at the beginig of the strings, which indicates if that's running in the main (`[MAIN]`) thread or in the async tasks (`[ASYNC]`). At the middle of the execution we call `thread.join()` just to do not have a disorder with the next examples.
```shell
Running async tasks...
[MAIN] Task in running now in background without blocking the main task!
[ASYNC] Downloading PDF 0...
[ASYNC] PDF 0 downloaded to filesystem!
[ASYNC] Downloading PDF 1...
[MAIN] And still running as non blocking!
[ASYNC] George Bernard Shaw: 'The single biggest problem in communication is the illusion that it has taken place.'
[ASYNC] PDF 1 downloaded to filesystem!
[ASYNC] Downloading PDF 2...
[ASYNC] Not an allowed extension.
[ASYNC] Downloading PDF 3...
[ASYNC] PDF 3 downloaded to filesystem!
[ASYNC] Downloading PDF 4...
[MAIN] We can keep doing stuff in the main thread/process.
[ASYNC] John Tukey: 'The greatest value of a picture is when it forces us to notice what we never expected to see.'
[MAIN] Now we can call thread.join() to wait for its execution
[ASYNC] Vince Lombardi: 'Confidence is contagious. So is lack of confidence.'
[ASYNC] PDF 4 downloaded to filesystem!
...
Async tasks completed!
Next example will run in...
5...
4...
3...
2...
1...
0...
```


### Concurrency

*Full implementation and documented code:* [./src/examples/concurrency.py](./src/examples/concurrency.py)

For the concurrent tasks I used `asyncio` to make GET requests to `https://httpbin.org/delay/{value_in_seconds}`. Each task has a different value for the delay. As we can see, it seems that the whole tasks are being executed simultaneously, but the processor just executes a part of the function at time. Which doesn't happen on parallelism.


Here is the `run_concurrent_tasks` function implementation:

```python
def run_concurrent_tasks() -> float:
    loop = asyncio.get_event_loop()
    tasks = [task(delay) for delay in range(10)]
    begin = time()
    values = loop.run_until_complete(asyncio.gather(*tasks))
    # print(values)
    end = time()
    total = end - begin
    loop.close()
    return total
```

Here are the logs for the execution:

```shell
Running concurrent tasks...
Sending request to: https://httpbin.org/delay/0
Sending request to: https://httpbin.org/delay/1
Sending request to: https://httpbin.org/delay/2
Sending request to: https://httpbin.org/delay/3
Sending request to: https://httpbin.org/delay/4
Sending request to: https://httpbin.org/delay/5
Sending request to: https://httpbin.org/delay/6
Sending request to: https://httpbin.org/delay/7
Sending request to: https://httpbin.org/delay/8
Sending request to: https://httpbin.org/delay/9
Request for https://httpbin.org/delay/1 suceed!
Request for https://httpbin.org/delay/2 suceed!
Request for https://httpbin.org/delay/3 suceed!
Request for https://httpbin.org/delay/4 suceed!
Request for https://httpbin.org/delay/0 suceed!
Request for https://httpbin.org/delay/5 suceed!
Request for https://httpbin.org/delay/6 suceed!
Request for https://httpbin.org/delay/7 suceed!
Request for https://httpbin.org/delay/8 suceed!
Request for https://httpbin.org/delay/9 suceed!
Total: 9.344942092895508 seconds
Concurrent tasks completed!
Next example will run in...
5...
4...
3...
2...
1...
0...
Now!
```

### Parallelism

*Full implementation and documented code:* [./src/examples/parallelism.py](./src/examples/parallelism.py)

For parallel processing I used the Python's `multiprocessing` library, to create Process that'll download images from given urls. In this case each process is executed with its own resources, allowing to perform the downloads in parallel.

Here is the `run_parallel_tasks` function implementation:

```python
def run_parallel_taks() -> float:
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
```

We can identify the logs of each process at the begining of the line.

```shell
Running parallel tasks...
[PROCESS-0] Downloading image from https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2048px-Python-logo-notext.svg.png
[PROCESS-1] Downloading image from https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Python_icon_%28black_and_white%29.svg/2048px-Python_icon_%28black_and_white%29.svg.png
[PROCESS-2] Downloading image from https://thumbs.dreamstime.com/b/icono-de-python-aislado-en-fondo-s%C3%ADmbolo-moda-f-del-vector-la-serpiente-117452925.jpg
[PROCESS-3] Downloading image from https://i.redd.it/rxezjyf4ojx41.png
[PROCESS-4] Downloading image from https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShRTQ5AQzs_FahcqOv2GGnfgziQw1wwfJHaA&usqp=CAU
[PROCESS-4] Download completed!
[PROCESS-1] Error while downloading the file: Not an allowed extension.
[PROCESS-2] Download completed!
[PROCESS-0] Download completed!
[PROCESS-3] Download completed!
Total: 2.5340263843536377 seconds
Parallel tasks completed!
Next example will run in...
5...
4...
3...
2...
1...
0...
Now!
```

### Semaphore

*Full implementation and documented code:* [./src/examples/semaphore.py](./src/examples/semaphore.py)

For the semaphore implementation, I created a task that gets the information of an IPV4 address using `IPWhois` Python's library, if the library gets the info, the IP and its info is added to a list that will be shared bye all the threads that will execute the same function for different IP Addresses. A time delay of 3 seconds is used to view the behaviour of the semaphore. This semaphore will allow only four threads to access simultaneously to the shared list.

Here is the `run_semaphore_example` function implementation:

```python
def run_semaphore_example():
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
```

We can see the logs of each thread acquiring and releasing the resource:

```shell
Running semaphore tasks...
[THREAD-15] Exception IPv4 address 10.251.62.94 is already defined as Private-Use Networks via RFC 1918.
[THREAD-0] Acquiring access to shared resource
[THREAD-19] Acquiring access to shared resource
[THREAD-4] Acquiring access to shared resource
[THREAD-13] Acquiring access to shared resource
[THREAD-0] Releasing access to shared resource
[THREAD-17] Acquiring access to shared resource
[THREAD-19] Releasing access to shared resource
[THREAD-4] Releasing access to shared resource
[THREAD-18] Acquiring access to shared resource
[THREAD-2] Acquiring access to shared resource
[THREAD-13] Releasing access to shared resource
[THREAD-1] Acquiring access to shared resource
[THREAD-17] Releasing access to shared resource
[THREAD-6] Acquiring access to shared resource
[THREAD-18] Releasing access to shared resource
[THREAD-7] Acquiring access to shared resource
[THREAD-2] Releasing access to shared resource
[THREAD-8] Acquiring access to shared resource
[THREAD-1] Releasing access to shared resource
[THREAD-14] Acquiring access to shared resource
[THREAD-6] Releasing access to shared resource
[THREAD-12] Acquiring access to shared resource
[THREAD-7] Releasing access to shared resource
[THREAD-10] Acquiring access to shared resource
[THREAD-8] Releasing access to shared resource
[THREAD-16] Acquiring access to shared resource
[THREAD-14] Releasing access to shared resource
[THREAD-11] Acquiring access to shared resource
[THREAD-12] Releasing access to shared resource
[THREAD-5] Acquiring access to shared resource
[THREAD-10] Releasing access to shared resource
[THREAD-9] Acquiring access to shared resource
[THREAD-16] Releasing access to shared resource
[THREAD-11] Releasing access to shared resource
[THREAD-5] Releasing access to shared resource
[THREAD-9] Releasing access to shared resource
[THREAD-3] Acquiring access to shared resource
[THREAD-3] Releasing access to shared resource
[('111.17.22.197', {...}, ...] # Full logs won't be shown here
Semaphore tasks completed!
Next example will run in...
5...
4...
3...
2...
1...
0...
Now!
```
### Workerpool

*Full implementation and documented code:* [./src/examples/workerpool.py](./src/examples/workerpool.py)

Finally, the workpool implementation. As in the parallel tasks implementation, I used the `multiprocessing` Python's library. A pool of three workers is created, each worker will execute a function to train a Stochastic Gradient Descent Classifier. Since the training doesn't take that much time, a time delay was added to allow watch the behaviour of the pool. Once a worker complete its job, can take another task until the whole tasks are completed.

Here is the `run_workerpool_tasks` function implementation:

```python
def run_workerpool_tasks() -> float:
    begin = time()
    with Pool(3) as pool:
        pool.map(train_model, list(range(100, 200, 10)))
    end = time()
    total = end - begin
    print(f"Total: {total} seconds")
    return total
```

Here are the logs for the pool:

```shell
Running workerpool tasks...
Iterations: 100, Accuracy: 0.9033391915641477
Iterations: 110, Accuracy: 0.9033391915641477
Iterations: 120, Accuracy: 0.9033391915641477
Iterations: 130, Accuracy: 0.9191564147627417
Iterations: 140, Accuracy: 0.9191564147627417
Iterations: 150, Accuracy: 0.9191564147627417
Iterations: 160, Accuracy: 0.9226713532513181
Iterations: 170, Accuracy: 0.9226713532513181
Iterations: 180, Accuracy: 0.9226713532513181
Iterations: 190, Accuracy: 0.9244288224956063
Total: 20.148380041122437 seconds
Workerpool tasks completed!
```



## Author

|Name|Occupation|Contact|
|-|-|-|
|Ortega Victoriano Ivan|SW/ML Engineer|ivanovskyortega@outlook.com|