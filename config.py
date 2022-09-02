# pylint: skip-file
import os

api_port = os.getenv("UVICORN_PORT")
api_host = os.getenv("UVICORN_HOST")
python_path = "venv"
bind = f"{api_host}:{api_port}"
workers = 2
threads = 8
worker_class = "uvicorn.workers.UvicornH11Worker"
timeout = 60
worker_tmp_dir = "/dev/shm"
