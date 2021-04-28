import queue
import threading

num_worker_threads = 10


def do_work(item, visited):
    print(item, threading.get_ident())
    x = item//10
    if x not in visited:
        visited.append(x)


def source():
    return range(100)


def worker(q, visited):
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item, visited)
        q.task_done()


def main():
    q = queue.Queue()
    visited = []
    threads = []

    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(q,visited))
        t.start()
        threads.append(t)

    for item in source():
        q.put(item)

    # block until all tasks are done
    q.join()

    print('stopping workers!')

    # stop workers
    for i in range(num_worker_threads):
        q.put(None)

    for t in threads:
        t.join()

    print(visited)


main()
