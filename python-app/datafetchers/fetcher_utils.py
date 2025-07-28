import aiohttp
import asyncio
import aiofiles


class DebugOption:
    NONE: int = 0
    SAVE_TO_FILE: int = 1
    READ_FROM_FILE: int = 2


async def async_fetch_url(target_url: str,
                          debug_option: DebugOption = DebugOption.NONE,
                          debug_file: str = None) -> bytearray:
    # TODO: make this separate function and remake tests for this.
    file_content = bytearray()
    if debug_option == DebugOption.READ_FROM_FILE:
        # print('Will read from file:', debug_file)
        async with aiofiles.open(debug_file, 'rb') as f:
            file_content = await f.read()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url) as response:
                if debug_option == DebugOption.SAVE_TO_FILE:
                    async with aiofiles.open(debug_file, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await f.write(chunk)
                            file_content.extend(chunk)
                else:
                    return await response.content.read()
    return str(file_content, 'utf-8')
