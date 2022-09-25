import aiohttp
import asyncio
from pathlib import Path
import time
import random

start_time = time.time()

async def main():
    urls_p = Path(__file__).parent / 'urls.txt'

    with open(urls_p, 'r', encoding='utf-8') as fh:
        urls_raw = str(fh.read())
    urls_list = urls_raw.split('\n')
    random.shuffle(urls_list)

    async with aiohttp.ClientSession() as session:
        for url_index in range(len(urls_list)):
            archive_url = f'https://web.archive.org/save/{urls_list[url_index]}'
            time.sleep(2)
            async with session.get(archive_url) as resp:
                req_status = resp.status
                archive_resp = await resp.text()
                print(f'({url_index+1}.) {archive_url} -> {req_status}')
        
            #break

asyncio.run(main())
print("INFO: completed run after %s seconds" % (time.time() - start_time))
