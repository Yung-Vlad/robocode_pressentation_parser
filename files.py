import aiohttp
import asyncio
import aiofiles
import json
import os
from typing import List, Dict

from logger import write_log, error_to_str, success_to_str


async def get_files(session: aiohttp.ClientSession, response: aiohttp.ClientResponse, course: str) -> List[str]:
    """Getting files"""

    try:
        # Files without "testing"
        filter_files = [item for item in reversed((await response.json())["topics"])
                        if item.get("title") != "Тестування"]

        files = {item["id"]: item["counter"] for item in filter_files[:4]}
        files_name = await download_files(session, files, course)

    except (aiohttp.ClientError, json.JSONDecodeError) as e:
        write_log("Files", error_to_str(str(e)))

    else:
        write_log("Files", success_to_str())
        return files_name


async def download_file(session: aiohttp.ClientSession, file_id: str, counter: int, course: str) -> str:
    """Downloading single file"""

    try:
        async with session.get(f"https://profile.robocode.ua/student/summary/{file_id}") as response:
            response.raise_for_status()

            file_name = f"{os.getenv('PATH_TO_PDF')}{course} Lesson {counter}.pdf"
            async with aiofiles.open(file_name, "wb") as pdf:
                await pdf.write(await response.read())
                return file_name

    except aiohttp.ClientError as e:
        write_log("Download", error_to_str(str(e)))


async def download_files(session: aiohttp.ClientSession, files: Dict, course: str) -> List[str]:
    """Downloading files asynchronously"""

    tasks = [download_file(session, file, counter, course) for file, counter in files.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            write_log("Download", error_to_str(str(result)))
        else:
            write_log("Download", success_to_str())

    return results


def del_files(path) -> None:
    os.remove(path)
