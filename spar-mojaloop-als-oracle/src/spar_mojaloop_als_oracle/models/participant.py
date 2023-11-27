from typing import List

from pydantic import BaseModel


class PartyTypeIdInfo(BaseModel):
    fspId: str


class ParticipantsTypeIDGetResponse(BaseModel):
    partyList: List[PartyTypeIdInfo]
