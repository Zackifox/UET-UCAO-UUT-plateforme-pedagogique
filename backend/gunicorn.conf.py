bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100

# Logs vers la console (Render compatible)
accesslog = "-"
errorlog = "-"
loglevel = "info"
