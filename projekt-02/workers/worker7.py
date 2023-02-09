import asyncio
import aiohttp
from aiohttp import web
import random
import time
import re

routes = web.RouteTableDef()

@routes.get("/")
async def word_count(req):
    try:
        await asyncio.sleep(random.uniform(0.1, 0.3))

        data = await req.json()
        words = re.sub("["+ string.punctuation +"]", "", data.get("content").split())
        all_words = len(words)

        await asyncio.sleep(random.uniform(0.1, 0.3))
        return web.json_response({ "status": ok, "wordCount": all_words}, status=200)
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8087)