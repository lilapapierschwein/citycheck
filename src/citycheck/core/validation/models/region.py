from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict


class BaseRegion(BaseModel):
    name: str

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Baseregion(name={self.name})"


class RegionModel(BaseRegion):
    id: int

    medel_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class RegionSchema(RegionModel): ...


class BaseSubregion(BaseModel):
    name: str
    region_id: int

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"{BaseSubregion}(name={self.name}, region_id={repr(self.region_id)})"


class SubregionModel(BaseSubregion):
    id: int
    region: RegionModel

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f"region_id={self.region_id}"
            ")"
        )


class SubregionSchema(SubregionModel): ...
