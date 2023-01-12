import asyncio
import aiofiles
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

async def save_files(el, i, username):
    try:
        async with aiofiles.open(f'files/{username}.txt', ('w')) as f:
            await f.write(str(el))
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)


@routes.post("/gatherdata")
async def gather_data(request):
    try:
        data = await request.json()
        data = data[0]
        print(len(data))
        print(data)
        if (len(data) > 10):
            for i, el in enumerate(data):
                username = el.get("username")
                print(i, el)
                await save_files(el, i, username)
        return web.json_response({"status": "ok", "data":data}, status=200)
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8083)