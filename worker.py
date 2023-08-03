import os
from rq import Queue, Worker, Connection
import redis

listen = ['high', 'default', 'low']

# Connect to Redis
r = redis.Redis(host='localhost', port=6379)

# Set up the RQ queue
queue = Queue(connection=r)

if __name__ == '__main__':
    with Connection(r):
        worker = Worker(map(Queue, listen))
        worker.work()