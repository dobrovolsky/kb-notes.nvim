import os
import subprocess
from contextlib import contextmanager
from typing import (
    Optional,
    ContextManager,
    Generator,
    List,
)

from pynvim import Nvim
from pynvim.api import Buffer


def find_all(text: bytes, sub: bytes) -> Generator[int, None, None]:
    start = 0
    while True:
        start = text.find(sub, start)
        if start == -1:
            return

        yield start
        start += len(sub)


def buffer_is_empty(buffer: Buffer) -> bool:
    return not any(buffer)


def current_note_name(nvim: Nvim) -> str:
    current_file_name = os.path.basename(nvim.current.buffer.name)
    return os.path.splitext(current_file_name)[0]


@contextmanager
def disable_deoplete(nvim: Nvim) -> ContextManager[None]:
    nvim.call("deoplete#disable")
    try:
        yield
    finally:
        nvim.call("deoplete#enable")


def fzf_with_preview(
    nvim: Nvim,
    source: list,
    sink: str,
    location: str,
    search_term: Optional[str] = None,
):
    if search_term is not None:
        options = f"-q {search_term}"
    else:
        options = ""

    nvim.call(
        "fzf#run",
        nvim.call(
            "fzf#wrap",
            nvim.call(
                "fzf#vim#with_preview",
                {
                    "source": source,
                    "sink": sink,
                    "dir": location,
                    "options": options,
                },
            ),
        ),
    )


def char_under_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')-1]")


def char_after_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')]")


def execute_command(command: List[str]) -> str:
    try:
        return subprocess.check_output(command).decode()
    except subprocess.CalledProcessError:
        return ""
