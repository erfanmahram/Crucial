import strawberry
from strawberry.scalars import JSON
from pydantic import typing, Field
from dataclasses import field


@strawberry.type
class SuggestInfo:
    ram: typing.Optional[typing.List[JSON]] = field(default_factory=lambda: [])
    ssd: typing.Optional[typing.List[JSON]] = field(default_factory=lambda: [])
    externalSsd: typing.Optional[typing.List[JSON]] = field(default_factory=lambda: [])


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
    # suggestInfo: typing.Optional[JSON] = None
    suggestInfo: typing.Optional[SuggestInfo] = Field(default_factory=SuggestInfo)
    indexed: typing.Optional[int] = 0
    lastUpdate: typing.Optional[str] = ""


if __name__ == '__main__':
    s = SuggestInfo()
    print(s.externalSsd)
    print(s.ssd)
    print(s.ram)

