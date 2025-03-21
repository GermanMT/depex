from asyncio import TimeoutError, sleep
from json import JSONDecodeError
from typing import Any

from aiohttp import ClientConnectorError, ContentTypeError

from app.cache import get_cache, set_cache
from app.http_session import get_session
from app.logger import logger


async def get_rubygems_versions(
    name: str,
    constraints: str | None = None,
    parent_id: str | None = None,
    parent_version_name: str | None = None
) -> tuple[list[dict[str, Any]], str, str | None, str | None, str | None]:
    response = await get_cache(name)
    if response:
        versions = response
    else:
        url = f"https://rubygems.org/api/v1/versions/{name}.json"
        session = await get_session()
        while True:
            try:
                logger.info(f"RUBYGEMS - {url}")
                async with session.get(url) as resp:
                    response = await resp.json()
                    break
            except (ClientConnectorError, TimeoutError):
                await sleep(5)
            except (JSONDecodeError, ContentTypeError):
                return [], name, constraints, parent_id, parent_version_name
        versions = [{"name": version.get("number"), "count": count} for count, version in enumerate(response)]
        await set_cache(name, versions)
    return versions, name, constraints, parent_id, parent_version_name


async def get_rubygems_requires(
    version_id: str,
    version: str,
    name: str
) -> tuple[dict[str, list[str] | str], str, str]:
    key = f"{name}:{version}"
    response = await get_cache(key)
    if response:
        require_packages = response
    else:
        url = f"https://rubygems.org/api/v2/rubygems/{name}/versions/{version}.json"
        session = await get_session()
        while True:
            try:
                logger.info(f"RUBYGEMS - {url}")
                async with session.get(url) as resp:
                    response = await resp.json()
                    break
            except (ClientConnectorError, TimeoutError):
                await sleep(5)
            except (JSONDecodeError, ContentTypeError):
                return {}, version_id, name
        require_packages: dict[str, Any] = {
            dep.get("name"): dep.get("requirements") for dep in response.get("dependencies", {}).get("runtime", []) or []
        }
        await set_cache(key, require_packages)
    return require_packages, version_id, name
