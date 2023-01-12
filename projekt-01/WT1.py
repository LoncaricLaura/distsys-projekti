import aiosqlite
import asyncio
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/")
async def get_data(request):
    try:
        data = await request.json()
        res = []
        wt1 = [i for i in data if i["username"].lower().startswith(("w", "d"))]
        if (wt1):
            res.append(wt1)
            print(res)
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:8083/gatherdata", json=res) as res:
                    result = await res.json()
                    print("Send!")
        return web.json_response({"status":"ok", "data_receive":res, "result": result.get("data")}, status=200) 
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500) 


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8082)