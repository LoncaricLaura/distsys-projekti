import asyncio
import aiohttp
import random
from aiohttp import web
import logging

routes = web.RouteTableDef()

N = random.randint(5, 10) # number of workers
print("Number of workers", N)

workers = {"id" + str(id) : [] for id in range(1, N+1)}
print("Workers:", workers)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

M = 1000 # sample size
received_requests = 0
received_responses = 0
send_tasks = 0
completed_tasks = 0
max_number = 10000

@routes.get("/")
async def get_function(req):
    try:
        tasks = []
        res = []
        received_requests += 1
        logging.info(f"Received new request: {received_requests} / {max_number}")
        data = await req.json()
        content_len = len(data.get("content"))
        all_content = '\n'.join(data.get("content"))
        content = all_content.split("\n")
        
        data["content"] = ["\n".join(content[i:i+M]) for i in range(0, len(content), M)]
        async with aiohttp.ClientSession() as session:
            cur_worker = 1
            for i in range(len(data.get("content"))):
                task = asyncio.create_task(session.get(f"http://127.0.0.1:{8080 + cur_worker}/"), json={'id': data.get("id"), "content": data.get("content")[i]})
                send_tasks += 1
                tasks.append(task)
                workers["id:", str(cur_worker)].append(tasks)
                if cur_worker != N:
                    cur_worker += 1
                else:
                    cur_worker = 1
            res = await asyncio.gather(*tasks)
            res = [await x.json() for x in res]

            avg_word = [res.get("words_number") for res in res]
            avg_word = int(sum(avg_word) / len(data.get("content")))
            received_responses += 1
        return web.json_response({"status":"ok", "averageWordCount":avg_word, "id": res.get("id")}, status=200)
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8080)
