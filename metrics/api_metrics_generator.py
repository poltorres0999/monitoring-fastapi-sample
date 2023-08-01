import asyncio
import logging
import aiohttp
import random


endpoints = [{
    "method": "GET",
    "endpoint": "get_endpoint"},
    {"method": "POST",
     "endpoint": "post_endpoint"},
    {"method": "PUT",
     "endpoint": "put_endpoint"},
    {"method": "DELETE",
     "endpoint": "delete_endpoint"}]


async def call_endpoint(session, endpoint_data):
    method = endpoint_data.get("method")
    endpoint = endpoint_data.get("endpoint")
    if method == "GET":
        async with session.get(f"http://fast-api-metrics-test:8000/{endpoint}") as response:
            return await response.json()
    elif method == "POST":
        async with session.post(f"http://fast-api-metrics-test:8000/{endpoint}") as response:
            return await response.json()
    elif method == "PUT":
        async with session.put(f"http://fast-api-metrics-test:8000/{endpoint}") as response:
            return await response.json()
    elif method == "DELETE":
        async with session.delete(f"http://fast-api-metrics-test:8000/{endpoint}") as response:
            return await response.json()


async def main():

    num_clients = 25 # Change this to the number of clients you want to simulate

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                tasks = [call_endpoint(session, random.choice(
                    endpoints)) for _ in range(num_clients)]
                responses = await asyncio.gather(*tasks)

                # Process the responses if needed
                for response in responses:
                    print(response)

                # Introduce a delay before the next round of requests
                # Adjust the delay time (in seconds) as needed
                await asyncio.sleep(5)

            except Exception as err:
                logging.error(f"{err}")

if __name__ == "__main__":
    asyncio.run(main())
