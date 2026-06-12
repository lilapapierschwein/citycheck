from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict, model_serializer


class RegionCreate(BaseModel):
    name: str

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"RegionCreate(name={self.name})"


class RegionModel(BaseModel):
    id: int
    name: str

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class RegionSchema(RegionModel): ...


class SubregionCreate(BaseModel):
    name: str
    region_id: int

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"SubregionCreate(name={self.name}, region_id={repr(self.region_id)})"


class SubregionModel(BaseModel):
    id: int
    name: str
    region_id: int

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


class SubregionSchema(SubregionModel):
    @model_serializer
    def serialize_model(self):
        return {"id": self.id, "name": self.name, "region": self.region}
