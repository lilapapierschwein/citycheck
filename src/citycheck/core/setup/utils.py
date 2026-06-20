import asyncio
import os
from asyncio import create_task
from asyncio import sleep as as_sleep
from collections.abc import Callable
from typing import Literal, TypeVar

from colorama import Fore, Style


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
