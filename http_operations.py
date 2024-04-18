import fake_useragent
import aiohttp
import os
from typing import List, Dict

from json_operations import load_from_json
from files import get_files
from logger import write_log, success_to_str, error_to_str


user = fake_useragent.UserAgent().random
header = {
    "user-agent": user
}


async def parse(course: str) -> List[str]:
    """Main-func for parsing"""

    logins = load_from_json("logins.json")
    async with aiohttp.ClientSession() as session:
        if await login(session, logins, course):
            response = await find_course(session, course)
            return await get_files(session, response, course)

    return []


async def login(session: aiohttp.ClientSession, logins: Dict, course: str) -> None:
    """Login in system with session"""

    try:
        header.update({"Content-Type": "application/x-www-form-urlencoded"})  # updating in header Content-Type
        async with session.post(url=os.getenv("LINK"), data=logins[course], headers=header) as response:
            response.raise_for_status()

    except aiohttp.ClientError as e:
        write_log("Login", error_to_str(str(e)))

    else:
        write_log("Login", success_to_str())


async def find_course(session: aiohttp.ClientSession, course: str) -> aiohttp.ClientResponse:
    """Searching course"""

    try:
        header.update({"Content-Type": "application/json"})  # updating in header Content-Type
        response = await session.post(url="https://profile.robocode.ua/student/get/topics",
                                      json={"level": course, "express": False}, headers=header)

        response.raise_for_status()

    except aiohttp.ClientError as e:
        write_log("Course", error_to_str(str(e)))

    else:
        write_log("Course", success_to_str())
        return response
