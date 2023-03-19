import asyncio
import logging
import random
import time
from datetime import datetime
from pathlib import Path

import aiohttp

parent_p = Path(__file__).parent
log_p = parent_p / "debug.log"

try:
    logging.basicConfig(format='%(asctime)-s %(levelname)s [%(name)s]: %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(log_p, encoding="utf-8"),
            logging.StreamHandler()
    ])
except Exception as e:
    logging.error(f"while logger init! -> error: {e}")

start_time = time.time()

async def main():
    urls_p = parent_p / 'urls.txt'

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
                logging.debug(f'({url_index+1}.) {archive_url} -> {req_status}')
        
            #break

try:
    lastmod_p = parent_p / "lastmod.txt"
    with open(lastmod_p, 'w+', encoding='utf-8') as fh:
        fh.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
except Exception as e:
    logging.error(f"failed to write to lastmod.txt -> error: {e}")

asyncio.run(main())

logging.info("INFO: completed run after %s seconds" % (time.time() - start_time))
