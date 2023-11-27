from typing import List

from pydantic import BaseModel


class Extension(BaseModel):
    key: str
    value: str


class ExtensionList(BaseModel):
    extension: List[Extension]


class ErrorInformation(BaseModel):
    errorCode: str
    errorDescription: str
    extensionList: ExtensionList = None


class ErrorInformationResponse(BaseModel):
    errorInformation: ErrorInformation
