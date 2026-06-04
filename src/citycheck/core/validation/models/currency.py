from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict


class BaseCurrency(BaseModel):
    name: str
    code: str
    symbol: str

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return (
            f"BaseCurrency(name={self.name}, code={self.code}, symbol={self.symbol}, )"
        )


class CurrencyModel(BaseCurrency):
    id: int

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f"code={self.code}, "
            f"symbol={self.symbol}"
            ")"
        )


class CurrencySchema(CurrencyModel): ...
