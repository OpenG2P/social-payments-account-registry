from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DfspLevelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    level: int
    next_level_id: Optional[int] = None
    validation_regex: Optional[str] = None


class DfspLevelValueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    level_id: Optional[int] = None
    next_level_id: Optional[int] = None


class DfspLevelValuesHttpResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    levelValues: List[DfspLevelValueResponse]


class DfspLevelHttpResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    levels: List[DfspLevelResponse]
