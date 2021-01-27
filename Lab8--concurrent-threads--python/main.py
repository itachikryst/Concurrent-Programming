import sys
import threading
import time
import multiprocessing
import random

class Queue:

    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        data = None
        try:
            data = self.queue.pop(0)
        except IndexError as ex:
            pass
        return data

    def isEmpty(self):
        return len(self.queue) == 0


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def sum(_list):
    sum = 0
    for x in _list:
        sum += x
    return sum

if __name__ == '__main__':
    startingList = list(range(0, 100000000))
    # startingList = [random.randrange(0, 100, 1) for i in range(1000000)]
    numberOfThreads = 12
    result = 0



    options = sys.argv[1:]

    if "--async" in options:
        if numberOfThreads > 12:
            startingList = chunkIt(startingList, numberOfThreads)
        else:
            startingList = [startingList]
        start = time.time()
        with multiprocessing.Pool(numberOfThreads) as p:
            results = p.map(sum, startingList)
        result = sum(results)
        end = time.time()
        print(result)
        print(end - start)

    else:
        resultQueue = Queue()
        threadList = []
        if numberOfThreads > 1:
            startingList = chunkIt(startingList, numberOfThreads)
        start = time.time()
        if numberOfThreads > 1:
            for subList in startingList:
                process = threading.Thread(target=lambda q, arg: q.enqueue(sum(subList)),
                                           args=(resultQueue, subList,))
                process.setDaemon(True)
                process.start()
                threadList.append(process)
            for t in threadList:
                t.join()
            while not resultQueue.isEmpty():
                result += resultQueue.dequeue()
        else:
            result = sum(startingList)
        end = time.time()
        print(result)
        print(end - start)
