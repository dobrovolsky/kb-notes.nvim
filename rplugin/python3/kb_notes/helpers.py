import os
import re
import subprocess
import unicodedata
from contextlib import contextmanager
from typing import (
    ContextManager,
    Generator,
    List,
)

from pynvim import Nvim
from pynvim.api import Buffer

from kb_notes.config import (
    ALLOWED_CHARS_PATTERN,
    DEFAULT_SEPARATOR,
)


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


def char_under_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')-1]")


def char_after_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')]")


def execute_command(command: List[str]) -> str:
    try:
        return subprocess.check_output(command).decode()
    except subprocess.CalledProcessError:
        return ""


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.lower()
    text = text.strip()
    text = re.sub(ALLOWED_CHARS_PATTERN, DEFAULT_SEPARATOR, text)
    return text
