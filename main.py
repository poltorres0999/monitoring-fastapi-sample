import random
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)


def random_wait():
    return random.randint(0, 30000) / 1000.0


def random_response_code():
    return random.choice([200, 400, 500])


@app.get("/health")
def health():
    time.sleep(random_wait())
    return JSONResponse(content={"message": "PUT endpoint test response"}, status_code=200)


@app.get("/get_endpoint")
def get_endpoint():
    time.sleep(random_wait())
    return JSONResponse(content={"message": "GET endpoint test response"}, status_code=random_response_code())


@app.post("/post_endpoint")
def post_endpoint():
    time.sleep(random_wait())
    return JSONResponse(content={"message": "POST endpoint test response"}, status_code=random_response_code())


@app.put("/put_endpoint")
def put_endpoint():
    time.sleep(random_wait())
    return JSONResponse(content={"message": "PUT endpoint test response"}, status_code=random_response_code())


@app.delete("/delete_endpoint")
def delete_endpoint():
    time.sleep(random_wait())
    return JSONResponse(content={"message": "DELETE endpoint test response"}, status_code=random_response_code())
