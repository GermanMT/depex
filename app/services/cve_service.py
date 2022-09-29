from app.services.dbs.databases import cve_collection


async def create_cve(cve_data: dict) -> dict:
    cve = await cve_collection.insert_one(cve_data)
    new_cve = await cve_collection.find_one({'_id': cve.inserted_id})
    return new_cve

async def read_cve_by_cve_id(cve_id: str) -> dict:
    cve = await cve_collection.find_one({'cve_id': cve_id})
    return cve