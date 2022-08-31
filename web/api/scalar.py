import strawberry
from strawberry.scalars import JSON
from pydantic import typing, Field


# @strawberry.type
# class suggestInfo:
#     ram: typing.Optional[JSON] = None
#     ssd: typing.Optional[JSON] = None
#     externalSsd: typing.Optional[JSON] = None


@strawberry.type
class Modelql:
    id: typing.Optional[int] = 0
    categoryName: typing.Optional[str] = ""
    brandName: typing.Optional[str] = ""
    modelName: typing.Optional[str] = ""
    modelUrl: typing.Optional[str] = ""
    maximumMemory: typing.Optional[str] = ""
    slots: typing.Optional[str] = ""
    standardMemory: typing.Optional[str] = ""
    strgType: typing.Optional[str] = ""
    suggestInfo: typing.Optional[JSON] = None
    # suggestInfo: typing.Optional[typing.List[suggestInfo]] = Field(default_factory=list)
    indexed: typing.Optional[int] = 0
    lastUpdate: typing.Optional[str] = ""
