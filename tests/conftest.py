import os
import time
from multiprocessing import Process

import pytest
import uvicorn

from indexer import ingest_csv
from main import app, Paper, init_es
from models import init_es, delete_papers


@pytest.yield_fixture(scope="session", autouse=True)
def test_server():
    init_es(index_name="test-index")
    ingest_csv("test_metadata.csv", "test-index")
    # uvicorn server is blocking so need a process
    proc = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={"host": "0.0.0.0", "port": 8081, "env_file": ".test-env"},
        daemon=True
    )
    proc.start()
    time.sleep(0.5)  # Time for the server to start
    yield
    delete_papers("test-index")
    proc.terminate()
