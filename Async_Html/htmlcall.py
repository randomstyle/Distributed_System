import requests
import asyncio


def getSync(website, fuId=None):
    print(fuId)
    r = requests.get(website)
    print(r.status_code)

async def http_get(website, fuId):
    
    res = requests.get(website)
    if fuId == 1:
        await asyncio.sleep(0.4)
    else:
        await asyncio.sleep(0.1)
    
    return res
    
async def getAsysnc(website, fuId=None):
    print(fuId)
    res = await http_get(website,fuId)
    print(res.status_code)

print('----------------------Asynchronous call-----------------------')
loop = asyncio.get_event_loop()
task1 = asyncio.ensure_future(getAsysnc('https://httpbin.org/status/200', 1))
task2 = asyncio.ensure_future(getAsysnc('https://httpbin.org/status/204', 2))

tasks = asyncio.gather(task1, task2)
loop.run_until_complete(tasks)
loop.close()

print('----------------------Synchronous call-----------------------') 
getSync('https://httpbin.org/status/200', 1)
getSync('https://httpbin.org/status/204', 2)
