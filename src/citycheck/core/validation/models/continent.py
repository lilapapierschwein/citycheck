from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict


class BaseContinent(BaseModel):
    name: str

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"BaseContinent(name={repr(self.name)})"


class ContinentModel(BaseContinent):
    id: int

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={repr(self.id)}, name={repr(self.name)})"


class ContinentSchema(ContinentModel): ...
