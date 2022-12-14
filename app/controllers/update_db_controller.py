from datetime import datetime
from time import sleep

from typing import Any

from dateutil.parser import parse
from fastapi_utils.tasks import repeat_every
from pymongo import InsertOne, ReplaceOne

from app.config import settings
from app.services.cve_service import bulk_write_cve_actions, read_cve_by_cve_id
from app.services.update_db_service import (
    read_env_variables,
    replace_env_variables
)
from app.utils.get_session import get_session


# 24h = 216000
@repeat_every(seconds=216000)
async def db_updater() -> None:
    env_variables = await read_env_variables()
    today = datetime.today()

    headers = {'apiKey': settings.NVD_APY_KEY}
    session = await get_session()

    while True:
        end_day = await get_end_day(
            today,
            env_variables['last_year_update'],
            env_variables['last_month_update']
        )

        str_month = (
            str(env_variables['last_month_update']) if env_variables['last_month_update'] > 9
            else '0' + str(env_variables['last_month_update'])
        )
        str_begin_day = (
            str(env_variables['last_day_update']) if env_variables['last_day_update'] > 9
            else '0' + str(env_variables['last_day_update'])
        )
        str_end_day = str(end_day) if end_day > 9 else '0' + str(end_day)

        str_begin = (
            str(env_variables['last_year_update']) +
            '-' + str_month + '-' + str_begin_day + 'T00:00:00'
        )
        str_end = (
            str(env_variables['last_year_update']) +
            '-' + str_month + '-' + str_end_day + 'T23:59:59'
        )

        params_pub = {
            'pubStartDate': str_begin,
            'pubEndDate': str_end
        }

        sleep(6)
        response = session.get(
            'https://services.nvd.nist.gov/rest/json/cves/2.0?',
            params=params_pub,
            headers=headers,
            timeout=25
        ).json()

        await update_db(response)

        params_mod = {
            'lastModStartDate': str_begin,
            'lastModEndDate': str_end
        }

        sleep(6)
        response = session.get(
            'https://services.nvd.nist.gov/rest/json/cves/2.0?',
            params=params_mod,
            headers=headers,
            timeout=25
        ).json()

        await update_db(response)

        if (
            env_variables['last_year_update'] == today.year and 
            env_variables['last_month_update'] == today.month
        ):
            env_variables['last_month_update'] = today.month
            env_variables['last_day_update'] = today.day
            env_variables['last_moment_update'] = datetime.now()
            await replace_env_variables(env_variables)
            break

        env_variables['last_month_update'] += 1
        env_variables['last_day_update'] = 1
        if env_variables['last_month_update'] == 13:
            env_variables['last_month_update'] = 1
            env_variables['last_year_update'] += 1


async def get_end_day(today: datetime, last_year: int, last_month: int) -> int:
    if last_year != today.year or last_month != today.month:
        if last_month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        if last_month in [4, 6, 9, 11]:
            return 30
        if last_month == 2:
            if last_year % 4 == 0:
                return 29
            return 28
    return today.day


async def update_db(raw_cves: dict[str, Any]) -> None:
    actions: list[Any] = []
    for raw_cve in raw_cves['vulnerabilities']:
        raw_cve = raw_cve['cve']
        raw_cve['published'] = parse(raw_cve['published'])
        raw_cve['lastModified'] = parse(raw_cve['lastModified'])
        cve = await read_cve_by_cve_id(raw_cve['id'])
        if not cve:
            actions.append(InsertOne(raw_cve))
        else:
            actions.append(ReplaceOne({'id': raw_cve['id']}, raw_cve))

    if actions:
        await bulk_write_cve_actions(actions, True)