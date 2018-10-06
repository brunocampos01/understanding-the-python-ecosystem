from amino import List


async def gather_sync(data, f):
    results = List()
    for el in data:
        results = results + List(await f(el))
    return results


async def gather_sync_flat(data, f):
    results = List()
    for el in data:
        results = results + (await f(el)).to_list
    return results

__all__ = ('gather_sync', 'gather_sync_flat')
