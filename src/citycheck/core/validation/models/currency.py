from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict


class CurrencyCreate(BaseModel):
    name: str
    symbol: str

    @override
    def __str__(self) -> str:
        return f"{self.name} ({self.symbol})"

    @override
    def __repr__(self) -> str:
        return f"CurrencyCreate(name={self.name}, symbol={self.symbol})"


class CurrencyModel(BaseModel):
    id: int
    name: str
    symbol: str

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return f"{self.name} ({self.symbol})"

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f"symbol={self.symbol}"
            ")"
        )


class CurrencySchema(CurrencyModel): ...
