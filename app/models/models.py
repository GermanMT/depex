from datetime import datetime
from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel, Field
from pytz import timezone


class Agregator(str, Enum):
    mean = "mean"
    weighted_mean = "weighted_mean"


class PackageManager(str, Enum):
    pip = "PIP"
    npm = "NPM"
    mvn = "MVN"


class VersionModel(BaseModel):
    release: str
    release_date: datetime | None
    count: int
    cves: list[dict[Any, Any]] | None
    mean: int
    weighted_mean: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "release": "1.26.5",
                "release_date": datetime.now(),
                "count": 23,
                "cves": [],
                "mean": 0,
                "weighted_mean": 0,
            }
        }


class PackageModel(BaseModel):
    name: str
    group_id: str | None
    moment: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {"name": "urllib3", "group_id": None, "moment": datetime.now()}
        }


class RequirementFile(BaseModel):
    name: str
    manager: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {"name": "requirements.txt", "manager": "PIP"}
        }


class RepositoryModel(BaseModel):
    owner: str = Field(
        ...,
        min_length=1,
        description="The owner repository size must be greater than zero",
    )
    name: str = Field(
        ...,
        min_length=1,
        description="The name repository size must be greater than zero",
    )
    moment: datetime
    add_extras: bool
    is_complete: bool

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "owner": "depexorg",
                "name": "pip_test",
                "moment": datetime.now(timezone("Europe/Madrid")),
                "add_extras": False,
                "is_complete": False,
            }
        }
