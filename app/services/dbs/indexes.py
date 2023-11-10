from app.services.dbs.databases import get_collection, get_graph_db_session


async def create_indexes() -> None:
    cves_collection = get_collection("cves")
    cpe_matchs_collection = get_collection("cpe_matchs")
    cpes_collection = get_collection("cpes")
    exploits_collection = get_collection("exploits")
    await cves_collection.create_index("id", unique=True)
    await cves_collection.create_index("products", unique=False)
    await cpe_matchs_collection.create_index("matchCriteriaId", unique=True)
    await cpes_collection.create_index("cpeNameId", unique=True)
    await exploits_collection.create_index("id", unique=True)
    await exploits_collection.create_index("cves", unique=False)
    for session in get_graph_db_session("ALL"):
        await session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Package) REQUIRE p.name IS UNIQUE"
        )
        await session.run(
            "CREATE TEXT INDEX IF NOT EXISTS FOR (p: Package) ON (p.name)"
        )
