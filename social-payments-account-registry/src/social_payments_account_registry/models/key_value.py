from pydantic import BaseModel


class KeyValuePair(BaseModel):
    key: str
    value: str
