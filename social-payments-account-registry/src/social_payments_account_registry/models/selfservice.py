from typing import List, Optional

from pydantic import BaseModel

from .key_value import KeyValuePair


class GetTxnStatus(BaseModel):
    txn_id: str
    status: str
    fa: Optional[str] = None


class UpdateTxnStatus(BaseModel):
    txn_id: str
    status: str


class FaUpdateRequest(BaseModel):
    level_values: List[KeyValuePair]
