from typing import List, Optional, Union

from pydantic import BaseModel

from .key_value import KeyValuePair


class GetTxnStatus(BaseModel):
    txn_id: str
    status: str
    status_reason_code: Optional[str] = None
    fa: Optional[Union[str, List[KeyValuePair]]] = None


class UpdateTxnStatus(BaseModel):
    txn_id: str
    status: str
    status_reason_code: Optional[str] = None


class FaUpdateRequest(BaseModel):
    level_values: List[KeyValuePair]
