import strawberry
from pydantic import typing, Field, BaseModel


class Ram(BaseModel):
    title: typing.Optional[str] = ""
    capacity: typing.Optional[str] = ""
    speed: typing.Optional[str] = ""
    manufactureTech: typing.Optional[str] = ""
    moduleType: typing.Optional[str] = ""
    voltage: typing.Optional[str] = ""
    specs: typing.Optional[typing.List[str]] = Field(default_factory=lambda: list)
    category: typing.Optional[str] = ""


@strawberry.experimental.pydantic.type(Ram)
class RamType:
    title: strawberry.auto
    capacity: strawberry.auto
    speed: strawberry.auto
    manufactureTech: strawberry.auto
    moduleType: strawberry.auto
    voltage: strawberry.auto
    specs: strawberry.auto
    category: strawberry.auto


class ExternalSsd(BaseModel):
    title: typing.Optional[str] = ""
    capacity: typing.Optional[str] = ""
    specs: typing.Optional[typing.List[str]] = Field(default_factory=lambda: list)
    category: typing.Optional[str] = ""


@strawberry.experimental.pydantic.type(ExternalSsd)
class ExternalSsdType:
    title: strawberry.auto
    capacity: strawberry.auto
    specs: strawberry.auto
    category: strawberry.auto


class Ssd(BaseModel):
    title: typing.Optional[str] = ""
    capacity: typing.Optional[str] = ""
    interface: typing.Optional[str] = ""
    formFactor: typing.Optional[str] = ""
    specs: typing.Optional[typing.List[str]] = Field(default_factory=lambda: list)
    category: typing.Optional[str] = ""


@strawberry.experimental.pydantic.type(Ssd)
class SsdType:
    title: strawberry.auto
    capacity: strawberry.auto
    interface: strawberry.auto
    formFactor: strawberry.auto
    specs: strawberry.auto
    category: strawberry.auto


class SuggestInfo(BaseModel):
    ram: typing.Optional[typing.List[Ram]] = Field(
        default_factory=lambda: list)
    ssd: typing.Optional[typing.List[Ssd]] = Field(
        default_factory=lambda: list)
    externalSsd: typing.Optional[typing.List[ExternalSsd]] = Field(
        default_factory=lambda: list)


@strawberry.experimental.pydantic.type(SuggestInfo)
class SuggestInfoType:
    ram: strawberry.auto
    ssd: strawberry.auto
    externalSsd: strawberry.auto


class Modelql(BaseModel):
    id: typing.Optional[int] = 0
    categoryName: typing.Optional[str] = ""
    brandName: typing.Optional[str] = ""
    modelName: typing.Optional[str] = ""
    modelUrl: typing.Optional[str] = ""
    maximumMemory: typing.Optional[str] = ""
    slots: typing.Optional[str] = ""
    standardMemory: typing.Optional[str] = ""
    strgType: typing.Optional[str] = ""
    suggestInfo: typing.Optional[SuggestInfo] = Field(default_factory=SuggestInfo)
    indexed: typing.Optional[int] = 0
    lastUpdate: typing.Optional[str] = ""


@strawberry.experimental.pydantic.type(Modelql)
class ModelqlType:
    id: strawberry.auto
    categoryName: strawberry.auto
    brandName: strawberry.auto
    modelName: strawberry.auto
    modelUrl: strawberry.auto
    maximumMemory: strawberry.auto
    slots: strawberry.auto
    standardMemory: strawberry.auto
    strgType: strawberry.auto
    suggestInfo: strawberry.auto
    indexed: strawberry.auto
    lastUpdate: strawberry.auto


if __name__ == '__main__':
    from models import traverse

    s = {
        "ram": [
            {
                "Title": "2GB DDR2 PC2-6400 800MT/s 200-pin SODIMM Non ECC Memory RAM ",
                "Capacity": "2GB",
                "Speed": "800MT/s (PC2-6400)",
                "ManufactureTech": "DDR2",
                "ModuleType": "SODIMM",
                "Voltage": "1.8v",
                "Specs": [
                    "CL6",
                    "1.8v",
                    "SODIMM",
                    "Non-ECC",
                    "200 Pin",
                    "1R (Single Rank)",
                    "no info",
                    "DDR2",
                    "800MT/s (PC2-6400)"
                ],
                "Category": "RAM"
            },
            {
                "Title": "1GB DDR2 PC2-6400 800MT/s 200-pin SODIMM Non ECC Memory RAM ",
                "Capacity": "1GB",
                "Speed": "800MT/s (PC2-6400)",
                "ManufactureTech": "DDR2",
                "ModuleType": "SODIMM",
                "Voltage": "1.8v",
                "Specs": [
                    "CL6",
                    "1.8v",
                    "SODIMM",
                    "Non-ECC",
                    "200 Pin",
                    "no info",
                    "no info",
                    "DDR2",
                    "800MT/s (PC2-6400)"
                ],
                "Category": "RAM"
            }
        ],
        "ssd": [
            {
                "Title": "SanDisk Plus 2TB (2000GB) SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 545MB/s R, 450MB/s W ",
                "Capacity": "2.0TB (2000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 545MB/s",
                    "Up To 445MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "SanDisk Plus 1TB (1000GB) SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 535MB/s R, 450MB/s W ",
                "Capacity": "1.0TB (1000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.0TB (1000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 535MB/s",
                    "Up To 450MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "SanDisk Plus 480GB SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 535MB/s R, 445MB/s W ",
                "Capacity": "480GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "480GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 535MB/s",
                    "Up To 445MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "SanDisk Plus 240GB SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 530MB/s R, 440MB/s W ",
                "Capacity": "240GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "240GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 530MB/s",
                    "Up To 440MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "SanDisk Ultra 3D 4TB (4000GB) SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 560MB/s R, 530MB/s W ",
                "Capacity": "4.0TB (4000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "4.0TB (4000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 560MB/s",
                    "Up To 530MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "SanDisk Ultra 3D 2TB (2000GB) SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 560MB/s R, 530MB/s W ",
                "Capacity": "2.0TB (2000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 560MB/s",
                    "Up To 530MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 2TB (2048GB) KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W, (Bundle) ",
                "Capacity": "2.0TB (2048GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2048GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 1TB (1024GB) KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W, (Bundle) ",
                "Capacity": "1.0TB (1024GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.0TB (1024GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 512GB KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W, (Bundle) ",
                "Capacity": "512GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "512GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 256GB KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 500MB/s W, (Bundle) ",
                "Capacity": "256GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "256GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 4TB (4000GB) MX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 510MB/s R, 560MB/s W ",
                "Capacity": "4.0TB (4000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "4.0TB (4000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 510MB/s",
                    "Up To 560MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 2TB (2000GB) MX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 510MB/s R, 560MB/s W ",
                "Capacity": "2.0TB (2000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 510MB/s",
                    "Up To 560MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 1TB (1000GB) MX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 510MB/s R, 560MB/s W ",
                "Capacity": "1.0TB (1000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.0TB (1000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 510MB/s",
                    "Up To 560MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 500GB MX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 510MB/s R, 560MB/s W ",
                "Capacity": "500GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "500GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 510MB/s",
                    "Up To 560MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 250GB MX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 510MB/s R, 560MB/s W ",
                "Capacity": "250GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "250GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 510MB/s",
                    "Up To 560MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 2TB (2000GB) BX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 540MB/s R, 500MB/s W ",
                "Capacity": "2.0TB (2000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 540MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 1TB (1000GB) BX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 540MB/s R, 500MB/s W ",
                "Capacity": "1.0TB (1000GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.0TB (1000GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 540MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 480GB BX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 540MB/s R, 500MB/s W ",
                "Capacity": "480GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "480GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 540MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 500GB BX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 540MB/s R, 500MB/s W ",
                "Capacity": "500GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "500GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 540MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Crucial 240GB BX500 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 540MB/s R, 500MB/s W ",
                "Capacity": "240GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "240GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 540MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 1.92TB (1920GB) A400 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 500MB/s R, 450MB/s W ",
                "Capacity": "1.92TB (1920GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.92TB (1920GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 500MB/s",
                    "Up To 450MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 960GB A400 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 500MB/s R, 450MB/s W ",
                "Capacity": "960GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "960GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 500MB/s",
                    "Up To 450MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 480GB A400 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 500MB/s R, 450MB/s W ",
                "Capacity": "480GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "480GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 500MB/s",
                    "Up To 450MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 120GB A400 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 500MB/s R, 320MB/s W ",
                "Capacity": "120GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "120GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 500MB/s",
                    "Up To 320MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 240GB A400 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 500MB/s R, 350MB/s W ",
                "Capacity": "240GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "240GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 500MB/s",
                    "Up To 350MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 2TB (2048GB) KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W ",
                "Capacity": "2.0TB (2048GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "2.0TB (2048GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 1TB (1024GB) KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W ",
                "Capacity": "1.0TB (1024GB)",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "1.0TB (1024GB)",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 512GB KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 520MB/s W ",
                "Capacity": "512GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "512GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 520MB/s"
                ],
                "Category": "SSD"
            },
            {
                "Title": "Kingston 256GB KC600 SSD 2.5 Inch 7mm, SATA 3.0 (6Gb/s), 3D TLC, 550MB/s R, 500MB/s W ",
                "Capacity": "256GB",
                "Interface": "SATA 3.0 (6Gb/s)",
                "FormFactor": "2.5\" (SATA)",
                "Specs": [
                    "256GB",
                    "SATA 3.0 (6Gb/s)",
                    "Up To 550MB/s",
                    "Up To 500MB/s"
                ],
                "Category": "SSD"
            }
        ],
        "externalSsd": [
            {
                "Title": "SanDisk 2TB (2000GB) Portable SSD USB 3.2, Gen2, Type-C/A, 520MB/s R ",
                "Capacity": "2TB (2000GB)",
                "Specs": [
                    "Read Speed: Up To 520MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 1TB (1000GB) Portable SSD USB 3.2, Gen2, Type-C/A, 520MB/s R ",
                "Capacity": "1TB (1000GB)",
                "Specs": [
                    "Read Speed: Up To 520MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 480GB Portable SSD USB 3.2, Gen2, Type-C/A, 520MB/s R ",
                "Capacity": "480GB",
                "Specs": [
                    "Read Speed: Up To 520MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 4TB (4000GB) Extreme Portable SSD USB 3.1, Type-C/A, 1050MB/s R ",
                "Capacity": "4TB (4000GB)",
                "Specs": [
                    "Read Speed: Up To 1050MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 2TB (2000GB) Extreme Portable SSD USB 3.1, Type-C/A, 1050MB/s R ",
                "Capacity": "2TB (2000GB)",
                "Specs": [
                    "Read Speed: Up To 1050MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 1TB (1000GB) Extreme Portable SSD USB 3.1, Type-C/A, 1050MB/s R ",
                "Capacity": "1TB (1000GB)",
                "Specs": [
                    "Read Speed: Up To 1050MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 500GB Extreme Portable SSD USB 3.1, Type-C/A, 1050MB/s R ",
                "Capacity": "500GB",
                "Specs": [
                    "Read Speed: Up To 1050MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 4TB (4000GB) Extreme Pro Portable SSD USB 3.1, Type-C/A, 2000MB/s R ",
                "Capacity": "4TB (4000GB)",
                "Specs": [
                    "Read Speed: Up To 2000MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 2TB (2000GB) Extreme Pro Portable SSD USB 3.1, Type-C/A, 2000MB/s R ",
                "Capacity": "2TB (2000GB)",
                "Specs": [
                    "Read Speed: Up To 2000MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            },
            {
                "Title": "SanDisk 1TB (1000GB) Extreme Pro Portable SSD USB 3.1, Type-C/A, 2000MB/s R ",
                "Capacity": "1TB (1000GB)",
                "Specs": [
                    "Read Speed: Up To 2000MB/s",
                    "Write Speed: N/A"
                ],
                "Category": "ExternalSSD"
            }
        ]
    }
    c = SuggestInfo.parse_obj(traverse(s))
    print(c)

    print(ModelqlType.from_pydantic(Modelql.parse_obj(s)))
