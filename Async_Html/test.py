import asyncio

async def slow_operation(future, id=None):
    print('waiting...', id)
    await asyncio.sleep(1)
    future.set_result('future ' + str(id) + ' is done!')

loop = asyncio.get_event_loop()
future1 = asyncio.Future()
asyncio.ensure_future(slow_operation(future1, 1))
future2 = asyncio.Future()
asyncio.ensure_future(slow_operation(future2, 2))
loop.run_until_complete(future1)
loop.run_until_complete(future2)
print(future1.result())
print(future2.result())
loop.close()