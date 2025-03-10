from pydantic import BaseModel, Field, validator

from .agregator import Agregator
from .node_type import NodeType
from .patterns import NEO4J_ID_PATTERN
from .validators import validate_max_level


class MinMaxImpactRequest(BaseModel):
    requirement_file_id: str = Field(
        pattern=NEO4J_ID_PATTERN
    )
    limit: int = Field(
        ge=1
    )
    max_level: int = Field(...)
    node_type: NodeType
    agregator: Agregator

    @validator("max_level")
    def validate_max_level(cls, value):
        return validate_max_level(value)
