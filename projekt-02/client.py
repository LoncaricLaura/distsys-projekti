import asyncio
import aiohttp
import pandas as pd

clientList = list(range(1,1001))

df = pd.read_json("fakeDataset.json", lines=True, nrows=10000)
python_code = df["content"]

client_dict = {id:[] for id in clientList}
client_rows = int(len(df) / len(clientList))

for id, content in client_dict.items():
    row_start = (id-1)*client_rows
    row_end = row_start + client_rows
    for i, row in df.iloc[row_start : row_end].iterrows():
        content.append(row.get("content"))
print(f"Dictionary length: {len(client_dict)}")

res = []
tasks = []
async def codeProcessing():
    async with aiohttp.ClientSession() as session:
        for id, content in client_dict.items():
            tasks.append(asyncio.create_task(session.get("http://127.0.0.1:8080/", json={"id": id, "content": content})))
        print("Data sent!")
        res = await asyncio.gather(*tasks)
        res = [await x.json() for x in res]

# average number of letters
for id, content in client_dict.items():
    count = 0
    for el in content:
        for i in el:
            count += len(i)
    avg_words = float(count) / float(client_rows)
    print("Average word count for client ", id, ":", avg_words)

asyncio.get_event_loop().run_until_complete(codeProcessing())

