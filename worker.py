import os
from rq import Queue, Worker, Connection
import redis
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

listen = ['high', 'default', 'low']

# Connect to Redis locally
# r = redis.Redis(host='localhost', port=6379)

# Connect to Redis production
url = urlparse(os.getenv("REDIS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None) # connect to redis - via Heroku docs

# Set up the RQ queue
queue = Queue(connection=r, default_timeout=300)

if __name__ == '__main__':
    with Connection(r):
        worker = Worker(map(Queue, listen))
        worker.work()