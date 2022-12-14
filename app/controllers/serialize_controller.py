from typing import Any

from bson import ObjectId
from flamapy.metamodels.dn_metamodel.models import (
    DependencyNetwork,
    RequirementFile,
    Package,
    Version
)
from flamapy.metamodels.dn_metamodel.transformations import SerializeNetwork

from app.services.package_edge_service import read_package_edge_by_id
from app.services.serialize_service import aggregate_network_by_id

all_package_edges: dict[str, dict[str, Any]] = {}
all_package_edges_ids: list[ObjectId] = []
all_versions: dict[str, Version] = {}
all_packages: dict[str, Package] = {}


async def serialize_network(network_id: str) -> DependencyNetwork | None:
    network = await aggregate_network_by_id(network_id)
    requirement_files = network['requirement_files']
    network['requirement_files'] = []
    serializer = SerializeNetwork(source_model=network)
    serializer.transform()
    await read_requirement_files(requirement_files, serializer.destination_model)
    return serializer.destination_model


async def read_requirement_files(
    requirement_files: list[dict[str, Any]],
    dn_model: DependencyNetwork
) -> None:
    for requirement_file in requirement_files:
        if not requirement_file['package_edges']:
            continue
        package_edges = requirement_file['package_edges']
        requirement_file['packages'] = []
        requirement_file = RequirementFile(**requirement_file)
        dn_model.requirement_files.append(requirement_file)
        await read_packages(package_edges, requirement_file)
        all_package_edges.clear()
        all_package_edges_ids.clear()
        all_versions.clear()
        all_packages.clear()


async def read_packages(
    package_egdes: list[dict[str, Any]],
    parent: RequirementFile | Version
) -> None:
    for package_edge in package_egdes:
        key = package_edge['package_name'] + str(package_edge['constraints'])
        if key in all_packages:
            parent.packages.append(all_packages[key])
        else:
            package = Package(**{
                'name': package_edge['package_name'],
                'constraints': package_edge['constraints'],
                'versions': []
            })
            all_packages[key] = package
            parent.packages.append(package)
            await read_versions(package_edge['versions'], package)


async def read_versions(versions: list[dict[str, Any]], package: Package) -> None:
    for version in versions:
        package_edges = []
        if 'package_edges' in version:
            package_edges = await search_package_edge(version['package_edges'])
        version['packages'] = []
        version = Version(**version)
        package.versions.append(version)
        if package_edges:
            await read_packages(package_edges, version)


async def search_package_edge(package_edge_ids: list[ObjectId]) -> list[dict[str, Any]]:
    package_edges = []
    for package_edge_id in package_edge_ids:
        key = str(package_edge_id)
        if package_edge_id not in all_package_edges_ids:
            package_edge = await read_package_edge_by_id(package_edge_id, 'pypi')
            all_package_edges[key] = package_edge
            all_package_edges_ids.append(package_edge_id)
            package_edges.append(package_edge)
            continue
        package_edge = all_package_edges[key]
        package_edges.append(package_edge)
    return package_edges