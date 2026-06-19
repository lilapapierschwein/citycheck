import os
from typing import Literal

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
