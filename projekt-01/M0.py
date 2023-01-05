import aiosqlite
import asyncio
import aiohttp
from aiohttp import web
import json
import pandas as pd 

routes = web.RouteTableDef()

df = pd.read_json("fakeDataset.json", lines=True, nrows=10000)

async def fill_database():
    async with aiosqlite.connect("database.db") as db:
        for index, row in df.iterrows():            
            repo_name = row["repo_name"]
            path = row["path"]
            size = row["size"]
            line_max = row["line_max"]
            copies = row["copies"]
            await db.execute("CREATE TABLE IF NOT EXISTS data(repo_name,path,size,line_max,copies)")
            await db.execute("INSERT INTO data(repo_name,path,size,line_max,copies) VALUES (?,?,?,?,?)", (repo_name,path,size,line_max,copies))
        await db.commit()
    return "Successfully filled the database!"
    
async def check_database(): 
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT COUNT(*) FROM sqlite_schema") as cur:
            async for row in cur:
                if(row[0] == 0):
                    print("Database is empty")
                    r = await fill_database()
                    return r
            await db.commit()
        return "Database is filled!"
check_database = asyncio.run(check_database())
print(check_database)

@routes.get("/getgitlinks")
async def get_git_links(request):
    try:
        response = []
        async with aiosqlite.connect("database.db") as db:
                async with db.execute("SELECT * FROM data LIMIT 100") as cur:
                    async for row in cur:
                        if(row[0] == 0):
                            response.append("Database is empty!")
                            break
                        response.append(row)
                    await db.commit()
        return web.json_response({"status":"ok", "data":response}, status=200)
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8080)








