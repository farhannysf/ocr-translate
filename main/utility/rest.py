import aiohttp
from logging import getLogger

logger = getLogger(__name__)


async def asyncGet(*args, **kwargs):
    async with aiohttp.ClientSession() as client:
        async with client.get(*args, **kwargs) as response:
            if response.status == 200:
                response.body = await response.read()
                return response

            else:
                logger.error(f"{response.url}: {response.status}")
                return {"status": "failed", "reason": response.reason}


async def asyncPost(*args, **kwargs):
    async with aiohttp.ClientSession() as client:
        async with client.post(*args, **kwargs) as response:
            if response.status == 200:
                response.body = await response.read()
                return response

            else:
                logger.error(f"{response.url}: {response.status}")