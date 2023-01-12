import aiosqlite
import asyncio
import aiohttp
from aiohttp import web
import numpy as np

routes = web.RouteTableDef()

@routes.get("/")
async def getdata(request):
    try: 
        tasks = []
        async with aiohttp.ClientSession() as session:
            tasks.append(asyncio.create_task(session.get("http://127.0.0.1:8080/getgitlinks")))
            data = await asyncio.gather(*tasks)
            data_res = await data[0].json()
            keys = ["username", "repo_name", "path", "size", "line_max", "copies"]
            data_dict = [dict(zip(keys[0:], i)) for i in data_res["data"]]
            async with session.post("http://127.0.0.1:8082/", json=data_dict) as res:
                result = await res.json()
        async with aiohttp.ClientSession() as session:
            tasks.append(asyncio.create_task(session.get("http://127.0.0.1:8080/getgitlinks")))
            data = await asyncio.gather(*tasks)
            data_res = await data[0].json()
            keys = ["username", "repo_name", "path", "size", "line_max", "copies"]
            data_dict = [dict(zip(keys[0:], i)) for i in data_res["data"]]
            async with session.post("http://127.0.0.1:8083/", json=data_dict) as res:
                result = await res.json()
        return web.json_response({"status": "ok", "data":data_dict}, status=200) 
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)       


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8081)