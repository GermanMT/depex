from datetime import datetime, timedelta
from typing import Any

from app.apis import get_requires, get_versions
from app.controllers.cve_controller import attribute_cves
from app.services import (
    count_number_of_versions_by_package,
    create_package_and_versions,
    create_requirement_file,
    create_versions,
    read_cpe_product_by_package_name,
    read_package_by_name,
    read_versions_names_by_package,
    relate_packages,
    update_package_moment,
)


async def cargo_create_requirement_file(name: str, file: Any, repository_id: str) -> None:
    new_req_file_id = await create_requirement_file(
        {"name": name, "manager": "cargo", "moment": datetime.now()}, repository_id
    )
    await cargo_generate_packages(file["dependencies"], new_req_file_id)


async def cargo_generate_packages(
    dependencies: dict[str, str], parent_id: str, parent_version_name: str | None = None
) -> None:
    packages: list[dict[str, Any]] = []
    for name, constraints in dependencies.items():
        package = await read_package_by_name("cargo", "none", name)
        if package:
            package["parent_id"] = parent_id
            package["parent_version_name"] = parent_version_name
            package["constraints"] = constraints
            if package["moment"] < datetime.now() - timedelta(days=10):
                await cargo_search_new_versions(package)
            packages.append(package)
        else:
            await cargo_create_package(
                name, constraints, parent_id, parent_version_name
            )
    await relate_packages(packages)


async def cargo_create_package(
    name: str,
    constraints: str | None = None,
    parent_id: str | None = None,
    parent_version_name: str | None = None,
) -> None:
    all_versions = await get_versions("cargo", name)
    if all_versions:
        cpe_product = await read_cpe_product_by_package_name(name)
        versions = [
            await attribute_cves(version, cpe_product, "cargo")
            for version in all_versions
        ]
        new_versions = await create_package_and_versions(
            {"manager": "cargo", "group_id": "none", "name": name, "moment": datetime.now()},
            versions,
            constraints,
            parent_id,
            parent_version_name,
        )
        for new_version in new_versions:
            await cargo_extract_packages(name, new_version)


async def cargo_extract_packages(
    parent_package_name: str, version: dict[str, Any]
) -> None:
    require_packages = await get_requires(
        version["name"], "cargo", name=parent_package_name
    )
    await cargo_generate_packages(require_packages, version["id"], parent_package_name)


async def cargo_search_new_versions(package: dict[str, Any]) -> None:
    all_versions = await get_versions("cargo", package["name"])
    counter = await count_number_of_versions_by_package("cargo", "none", package["name"])
    if counter < len(all_versions):
        no_existing_versions: list[dict[str, Any]] = []
        cpe_product = await read_cpe_product_by_package_name(package["name"])
        actual_versions = await read_versions_names_by_package("cargo", "none", package["name"])
        for version in all_versions:
            if version["name"] not in actual_versions:
                version["count"] = counter
                new_version = await attribute_cves(
                    version, cpe_product, "cargo"
                )
                no_existing_versions.append(new_version)
                counter += 1
        new_versions = await create_versions(
            package,
            no_existing_versions
        )
        for new_version in new_versions:
            await cargo_extract_packages(package["name"], new_version)
    await update_package_moment("cargo", "none", package["name"])
