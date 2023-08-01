import asyncio

async def run_script(script_name):
    process = await asyncio.create_subprocess_exec('python', script_name)
    await process.wait()

async def main():
    tasks = [run_script('metrics/api_metrics_generator.py'), run_script('metrics/log_generator.py')]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())