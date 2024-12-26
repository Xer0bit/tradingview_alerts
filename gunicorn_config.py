import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'
