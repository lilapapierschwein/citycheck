import asyncio
import os
from asyncio import create_task
from asyncio import sleep as as_sleep
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal, TypeVar, override

from colorama import Fore, Style

from citycheck.core.utils import config


def get_term_width() -> int:
    return os.get_terminal_size().columns


def print_headline(
    headline: str,
    width: int = 80,
    fillchar: str = "=",
    color: Literal["green", "yellow", "red"] | None = None,
) -> None:
    headline = f" {headline.strip()} ".center(width, fillchar)
    if color:
        match color:
            case "green":
                headline = f"{Fore.GREEN}{headline}"
            case "yellow":
                headline = f"{Fore.YELLOW}{headline}"
            case "red":
                headline = f"{Fore.RED}{headline}"
        headline = f"{headline}{Style.RESET_ALL}"
    print(headline)


MESSAGES = {
    "success": f"{Fore.GREEN}DONE{Style.RESET_ALL}",
    "warning": f"{Fore.YELLOW}WARN{Style.RESET_ALL}",
    "failure": f"{Fore.RED}FAIL{Style.RESET_ALL}",
}
SLEEP_TIME = 0.19


class JWTAlgorithm(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"


@dataclass
class EnvVars:
    secrets: config.Secrets
    security: config.Security

    @override
    def __str__(self) -> str:
        return "\n".join(self._compile())

    @property
    def compiled(self) -> list[str]:
        return self._compile()

    def _compile(self) -> list[str]:
        vars: list[str] = [
            f"SECRETS__RESTCOUNTRIES_API_KEY={self.secrets.restcountries_api}",
            f"SECURITY__JWT_SECRET_KEY={self.security.jwt_secret_key}",
            f"SECURITY__JWT_SECRET_KEY={self.security.jwt_algorithm}",
        ]
        return vars


class EnvFileGenerator:
    def __init__(self, filename: str = ".env") -> None:
        self.filename: str = filename

        self._output_file: Path | None = None

        self._rc_api_key: str | None = None
        self._jwt_secret_key: str | None = None
        self._jwt_algorithm: JWTAlgorithm = JWTAlgorithm.HS256

        self._jwt_algo_choices: list[str] = [algo.value for algo in JWTAlgorithm]
        self._input_functions: list[Callable[[], None]] = [
            self._get_rc_api_key,
            self._get_jwt_secret_key,
            self._get_jwt_algorithm,
        ]

    def __call__(self) -> None:
        for func in self._input_functions:
            func()

        if self._jwt_secret_key is None:
            raise AttributeError("No JWT secret key found")
        env_vars = EnvVars(
            secrets=config.Secrets.model_validate(
                {"restcountries_api_key": self._rc_api_key or "rc_live_00example00"}
            ),
            security=config.Security.model_validate(
                {"jwt_secret_key": self._jwt_secret_key, "jwt_algorithm": self._jwt_algorithm}
            ),
        )

        file = Path.cwd() / "test.env"
        with file.open("w", encoding="utf-8") as f:
            f.writelines(line + "\n" for line in env_vars.compiled)

    def _get_rc_api_key(self) -> None:
        rc_api_key = input("paste your restcountries api key (optional): ").strip()
        if rc_api_key:
            self._rc_api_key = rc_api_key
        return None

    def _get_jwt_secret_key(self) -> None:
        while True:
            try:
                self._jwt_secret_key = input("paste your jwt secret key: ").strip()
                if self._jwt_secret_key == "":
                    raise ValueError("empty key")
                break
            except ValueError as err:
                print("\nerror:", err, end="\n")
        return None

    def _get_jwt_algorithm(self) -> None:
        while True:
            try:
                jwt_algo = (
                    input(f"set jwt algorithm (optional) [{'/'.join(self._jwt_algo_choices)}]: ")
                    .strip()
                    .upper()
                )
                if jwt_algo == "":
                    break
                if jwt_algo and jwt_algo in self._jwt_algo_choices:
                    self._jwt_algorithm = JWTAlgorithm(jwt_algo)
                    break
                raise ValueError(
                    f"""invalid algorithm: {jwt_algo!r}. choose one of \
{", ".join(repr(c) for c in self._jwt_algo_choices)} or \
leave empty to use default ({self._jwt_algorithm})."""
                )
            except ValueError as err:
                print("\nerror:", err, end="\n")
        return None


class ProgressBar:
    def __init__(
        self, total: int, scale: Literal[10, 20, 50, 100] = 50, char: Literal["#", "*"] = "#"
    ) -> None:
        self.total: int = total
        self.scale: int = scale
        self.char: str = char

        self.bar_value: float = 100 / self.scale
        self.bar_empty: str = "." * self.scale

    def __call__(self, c: int) -> str:
        percentage = self._get_percentage(c)
        bars_count = self._get_bars_count(percentage)
        bars = self._get_bars(bars_count)
        return f"[{self._get_current_bar(bars, bars_count)}]"

    def _get_percentage(self, c: int | float) -> float:
        return (c / self.total) * 100

    def _get_bars_count(self, p: float) -> int:
        return int(p // self.bar_value)

    def _get_bars(self, c: int) -> str:
        return self.char * c

    def _get_current_bar(self, b: str, c: int) -> str:
        return b + self.bar_empty[c:]


async def display_loading_text(
    text: str, max_fill: int = 3, fillchar: str = ".", sleep_time: float = SLEEP_TIME
) -> None:
    i = 0
    while True:
        loading_text = text + (fillchar * (i % (max_fill + 1)))
        print(loading_text + (" " * max_fill), end="\r")
        await as_sleep(sleep_time)
        i += 1


R = TypeVar("R")


async def execWhileLoading[R](func: Callable[..., R], text: str) -> R:
    # load animation on another thread
    loading_t = create_task(display_loading_text(text))

    # returns a result after some time (NOT asyncronous)
    result = await asyncio.get_event_loop().run_in_executor(None, func)

    # fetching is done - cancel loading animation
    _ = loading_t.cancel()  # cancel animation thread

    print(text + ("." * 3) + MESSAGES["success"])
    return result
