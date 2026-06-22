import json
import re
from argparse import Namespace
from dataclasses import dataclass
from datetime import datetime as dt
from pathlib import Path
from typing import Literal, TypedDict, override

from citycheck import app_config

paths = app_config.paths


class LCPathDict(TypedDict):
    full: str
    relative: str


class LCountsDict(TypedDict):
    total: int
    by_extension: dict[str, int]


class LineCountResultDict(TypedDict):
    project: str
    path: LCPathDict
    count: LCountsDict
    filetypes: list[str]
    ignored_files: list[str] | None
    ignore_empty_lines: bool
    timestamp: str


@dataclass
class LineCountResult:
    total_lines: int
    lines_by_extension: dict[str, int]
    root: Path
    pattern: re.Pattern[str]
    ignored_files: list[str] | None = None
    timestamp: dt = dt.now().replace(microsecond=0)
    project_root: Path | None = None
    project_name: str | None = None
    ignore_empty_lines: bool = True

    @override
    def __str__(self) -> str:
        root = self.root.relative_to(self.project_root.parent) if self.project_root else self.root

        if not self.total_lines:
            return f"No lines of code found in {root}"

        results = self.as_dict()

        result = [
            f"> Found {self.total_lines} total lines of code in '{root}'",
            "",
            f"> Filetypes:  {''.join(f'\n    *{ft}' for ft in results['filetypes'])}",
            "",
            f"> Ignored:    {
                ''.join([f'\n    {repr(f)}' for f in results['ignored_files']])
                if results['ignored_files']
                else '-'
            }",
            "",
            "> Line count by filetype (greatest to lowest):",
            *[
                f"    *{f'{k}:'.ljust(self.get_max_extension_len() + 2)} {v}"
                for k, v in results["count"]["by_extension"].items()
            ],
            "",
            f"> Empty lines ignored: {results['ignore_empty_lines']}",
            "",
            f"> Timestamp: {results['timestamp']}",
        ]
        if self.project_name:
            result.insert(0, f"> Project: {repr(self.project_name)}\n")
        return "\n".join(result)

    def get_lines_by_extension_sorted(
        self, sort: Literal["desc", "asc"] = "desc"
    ) -> dict[str, int]:
        lines_by_ext = sorted(
            [(k, v) for k, v in self.lines_by_extension.items()],
            key=lambda ext: ext[1],
            reverse=(sort == "desc"),
        )
        return {ext[0]: ext[1] for ext in lines_by_ext}

    def as_dict(self) -> LineCountResultDict:
        rel_path = (
            f"./{str(self.root.relative_to(self.project_root))}" if self.project_root else "-"
        )
        return {
            "project": self.project_name or "N/A",
            "path": {
                "full": str(self.root),
                "relative": rel_path,
            },
            "count": {
                "total": self.total_lines,
                "by_extension": self.get_lines_by_extension_sorted(),
            },
            "filetypes": re.sub(r"\s+", " ", self.get_extensions_from_pattern())
            .strip()
            .replace("*", "")
            .split(" "),
            "ignored_files": self.ignored_files,
            "ignore_empty_lines": self.ignore_empty_lines,
            "timestamp": self.timestamp.isoformat(),
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2)

    def get_max_extension_len(self) -> int:
        return max(len(ext) for ext in self.lines_by_extension)

    def get_extensions_from_pattern(self) -> str:
        og_pattern = self.pattern.pattern
        pattern = re.search(r"(\({1}[-a-zA-Z0-9._|]+\){1})", og_pattern)
        if not pattern:
            return "-"
        return "\n" + "\n".join([f"    *.{ext}" for ext in pattern.group().strip(")(").split("|")])

    def get_ignored_files(self) -> str:
        if not self.ignored_files:
            return "-"
        return "\n" + "\n".join(f"    '{file}'" for file in self.ignored_files)


@dataclass
class LinesCounter:
    root: Path
    pattern: re.Pattern[str]
    ignore_files: list[str] | None = None
    project_root: Path | None = None
    ignore_empty_lines: bool = True
    project_name: str | None = None
    result: LineCountResult | None = None

    def __call__(self) -> LineCountResult:
        """Counts the number of lines of code in files matching the given pattern, ignoring specified files.

        Args:
            root(`pathlib.Path`): The root directory to search for files.
            pattern(`re.Pattern`[`str`]): A regular expression pattern to match file names.
            ignore_files(`list`[`str`]): A list of file names to ignore.

        Returns:
            `:class:LineCountResult`: An object containing the total line count, line count by file extension,
                             and other relevant information.
        """
        lines_by_extension: dict[str, int] = {}
        total_lines = 0

        for file in self.root.rglob("*"):
            if file.is_file() and self.pattern.search(file.name):
                if self.ignore_files and file.name in self.ignore_files:
                    continue
                try:
                    with file.open("r", encoding="utf-8", errors="ignore") as f:
                        lines = (
                            sum(1 for _ in f)
                            if not self.ignore_empty_lines
                            else sum(1 for line in f if line.strip())
                        )
                        total_lines += lines

                        if file.suffix not in lines_by_extension:
                            lines_by_extension[file.suffix] = 0
                        lines_by_extension[file.suffix] += lines
                except PermissionError, FileNotFoundError:
                    continue
        self.result = LineCountResult(
            total_lines=total_lines,
            lines_by_extension=lines_by_extension,
            root=self.root,
            pattern=self.pattern,
            ignored_files=self.ignore_files,
            project_root=self.project_root,
            project_name=self.project_name,
            ignore_empty_lines=self.ignore_empty_lines,
        )
        return self.result


def count_lines_of_code(
    root: Path,
    pattern: re.Pattern[str],
    ignore_files: list[str] | None = None,
    project_root: Path | None = None,
    ignore_empty_lines: bool = True,
    project_name: str | None = None,
) -> LineCountResult:
    """Counts the number of lines of code in files matching the given pattern, ignoring specified files.

    Args:
        root(`pathlib.Path`): The root directory to search for files.
        pattern(`re.Pattern`[`str`]): A regular expression pattern to match file names.
        ignore_files(`list`[`str`]): A list of file names to ignore.

    Returns:
        `:class:LineCountResult`: An object containing the total line count, line count by file extension,
                         and other relevant information.
    """

    lines_by_extension: dict[str, int] = {}
    total_lines = 0

    for file in root.rglob("*"):
        if file.is_file() and pattern.search(file.name):
            if ignore_files and file.name in ignore_files:
                continue
            try:
                with file.open("r", encoding="utf-8", errors="ignore") as f:
                    lines = (
                        sum(1 for _ in f)
                        if not ignore_empty_lines
                        else sum(1 for line in f if line.strip())
                    )
                    total_lines += lines

                    if file.suffix not in lines_by_extension:
                        lines_by_extension[file.suffix] = 0
                    lines_by_extension[file.suffix] += lines
            except PermissionError, FileNotFoundError:
                continue

    return LineCountResult(
        total_lines=total_lines,
        lines_by_extension=lines_by_extension,
        root=root,
        pattern=pattern,
        ignored_files=ignore_files,
        project_root=project_root,
        project_name=project_name,
        ignore_empty_lines=ignore_empty_lines,
    )


def count_lines_cli(args: Namespace) -> None:
    filetypes: list[str] | None = args.filetypes
    if not filetypes:
        raise AttributeError("No filetypes for counting specified.")
    filetypes = [ft.strip(".") for ft in filetypes]

    count_lines = LinesCounter(
        root=(args.path or paths.directories.src).absolute(),
        pattern=re.compile(rf"\.({'|'.join(filetypes)})$"),
        ignore_files=args.ignore,
        project_root=paths.root,
        project_name=app_config.general.app_name,
        ignore_empty_lines=not args.include_empty_lines,
    )

    mode: Literal["plain", "json"] = args.mode or "plain"
    output: Path | Literal["stdout"] = args.output or "stdout"
    result = count_lines()
    result_out = str(result) if mode == "plain" else result.as_json()

    if isinstance(output, str) and output == "stdout":
        print(result_out)
        return None

    output_filetypes = {"plain": [".txt", ".md"], "json": [".json"]}
    if output.suffix not in output_filetypes[mode]:
        raise ValueError(
            f"Invalid filetype: {output.suffix!r}. "
            + f"{mode!r}-style output must be stored as {', '.join(output_filetypes[mode])}."
        )
    file = output.resolve()
    if not file.exists() and not file.parent.exists():
        print(f"Directory not found at {file.parent!r}")
        user_confirm = input("Do you want to create it with all parents? [Y/n]: ").strip().lower()
        if user_confirm in ("n", "no"):
            print(result)
            return None
        file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        _ = f.write(result_out)
    print(f"Lines count saved to file {repr(str(file))}.")
