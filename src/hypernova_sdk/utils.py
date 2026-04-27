"""Rich-powered logging utilities for simplified, pretty console output."""

from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Iterable, Iterator

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.status import Status
from rich.table import Table
from rich.tree import Tree

if TYPE_CHECKING:
    from rich.progress import ProgressType
    from rich.table import Column, Row

__all__ = [
    "NovaLogger",
    "nova_log",
    "print_success",
    "print_warning",
    "print_error",
    "print_info",
    "print_header",
    "print_table",
    "print_tree",
    "progress",
    "status",
    "timer",
]


class NovaLogger:
    """A rich-styled logger with severity levels and coloured output."""

    def __init__(
        self,
        *,
        show_time: bool = True,
        show_level: bool = True,
        level_key: bool = True,
    ) -> None:
        self._console = Console(
            file=sys.stdout,
            force_terminal=True,
        )
        self._show_time = show_time
        self._show_level = show_level
        self._level_key = level_key

    def _format(self, message: str, level: str, style: str) -> str:
        prefix_parts = []
        if self._show_time:
            now = time.strftime("%H:%M:%S")
            prefix_parts.append(f"[dim][[[/dim][b magenta]{now}[/b magenta][dim]]][/dim]")
        if self._show_level:
            prefix_parts.append(f"[{style}]{level}[/{style}]")
        if prefix_parts:
            prefix = " ".join(prefix_parts)
            return f"{prefix}  {message}"
        return message

    def success(self, message: str) -> None:
        self._console.print(self._format(message, "✓ SUCCESS", "bold green"), highlight=False)

    def warning(self, message: str) -> None:
        self._console.print(self._format(message, "⚠ WARNING", "bold yellow"), highlight=False)

    def error(self, message: str) -> None:
        self._console.print(self._format(message, "✗ ERROR", "bold red"), highlight=False)

    def info(self, message: str) -> None:
        self._console.print(self._format(message, "ℹ INFO", "bold blue"), highlight=False)

    def debug(self, message: str) -> None:
        self._console.print(self._format(message, "⚙ DEBUG", "dim"), highlight=False)

    def plain(self, message: str) -> None:
        self._console.print(message, highlight=False)

    def section(self, title: str) -> None:
        self._console.rule(f"[bold]{title}[/bold]")

    def table(
        self,
        *headers: str,
        rows: Iterable[list[str]] | Iterable[tuple[str, ...]] | None = None,
        title: str | None = None,
        **kwargs: Any,
    ) -> Table:
        table = Table(title=title, **kwargs)
        for h in headers:
            table.add_column(f"[bold]{h}[/bold]")
        if rows:
            for row in rows:
                table.add_row(*row)
        self._console.print(table)
        return table


# ─── Module-level convenience helpers ───────────────────────────────────────

nova_log = NovaLogger()
"""Default shared logger instance."""


def print_success(message: str) -> None:
    nova_log.success(message)


def print_warning(message: str) -> None:
    nova_log.warning(message)


def print_error(message: str) -> None:
    nova_log.error(message)


def print_info(message: str) -> None:
    nova_log.info(message)


def print_header(title: str) -> None:
    nova_log.section(title)


def print_table(
    *headers: str,
    rows: Iterable[list[str]] | Iterable[tuple[str, ...]] | None = None,
    title: str | None = None,
    **kwargs: Any,
) -> Table:
    return nova_log.table(*headers, rows=rows, title=title, **kwargs)


def print_tree(label: str, *children: str | tuple[str, Iterable[str]]) -> Tree:
    """Print a tree structure.

    Args:
        label: Root node label.
        *children: Either plain strings (leaf nodes) or (label, iterable) tuples
                   for branches with sub-children.

    Example:
        >>> print_tree("Project", ("src", ["a.py", "b.py"]), "README.md")
    """
    tree = Tree(f"[bold]{label}[/bold]")
    for child in children:
        if isinstance(child, str):
            tree.add(f"[dim]{child}[/dim]")
        else:
            label_, sub = child
            branch = tree.add(f"[bold cyan]{label_}[/bold cyan]")
            for item in sub:
                branch.add(f"[dim]{item}[/dim]")
    nova_log.plain(str(tree))
    return tree


@contextmanager
def progress(*columns: str | ProgressType, **kwargs: Any) -> Iterator[Progress]:
    """Context manager that displays a progress bar while running.

    Args:
        *columns: Custom progress columns (defaults provided if none given).
        **kwargs: Passed to rich.progress.Progress.

    Yields:
        A rich Progress instance.

    Example:
        >>> with progress() as prog:
        ...     task = prog.add_task("Downloading...", total=100)
        ...     for i in range(100):
        ...         prog.update(task, advance=1)
    """
    if not columns:
        columns = (
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        )
    prog = Progress(*columns, console=nova_log._console, **kwargs)
    prog.start()
    try:
        yield prog
    finally:
        prog.stop()


@contextmanager
def status(message: str = "Working...", **kwargs: Any) -> Iterator[Status]:
    """Context manager that displays a spinner with a message.

    Example:
        >>> with status("Fetching data..."):
        ...     data = fetch_data()
    """
    stat = Status(message, console=nova_log._console, **kwargs)
    stat.start()
    try:
        yield stat
    finally:
        stat.stop()


@contextmanager
def timer(message: str = "Elapsed") -> Iterator[None]:
    """Context manager that prints elapsed time on exit.

    Example:
        >>> with timer("Operation"):
        ...     do_work()
    """
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    nova_log.info(f"{message}: {elapsed:.2f}s")
