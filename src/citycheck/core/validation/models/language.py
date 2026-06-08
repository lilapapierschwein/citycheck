from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict


class LanguageCreate(BaseModel):
    name: str

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"BaseLanguage(name={repr(self.name)})"


class LanguageModel(BaseModel):
    id: int
    name: str

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={repr(self.id)}, name={repr(self.name)})"


class LanguageSchema(LanguageModel): ...
