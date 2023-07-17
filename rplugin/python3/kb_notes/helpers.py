import functools
import os
import re
import subprocess
import typing
import unicodedata
from contextlib import contextmanager
from typing import (
    ContextManager,
    Generator,
    List,
    Optional,
)

from pynvim import (
    Nvim,
    NvimError,
)
from pynvim.api import Buffer

from kb_notes.config import (
    ALLOWED_CHARS_PATTERN,
    DEFAULT_SEPARATOR,
)
from kb_notes.exeptions import (
    InputError,
    ActionAborted,
    NoteExists,
    ApplicationException,
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


def char_under_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')-1]")


def char_after_cursor(nvim: Nvim) -> str:
    return nvim.eval("getline('.')[col('.')]")


def capture_input(nvim: Nvim, message: str, default: Optional[str] = None) -> str:
    if default:
        default_str = f", '{default}'"
    else:
        default_str = ""

    try:
        return nvim.eval(f"input('{message}'{default_str})")
    except NvimError as e:
        raise InputError(e)


def confirm_action(nvim: Nvim, message: str) -> bool:
    answer = capture_input(
        nvim,
        f'{message} (to continue press "y"): ',
    )

    return answer.lower() == "y"


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


def handle_exceptions(func: typing.Callable = None) -> typing.Callable:
    @functools.wraps(func)
    def decorated(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # self is NotesPlugin
        self = args[0]

        try:
            return func(*args, **kwargs)
        except InputError as e:
            self.app.nvim.out_write(f"Input error: {e}\n")
        except ActionAborted:
            self.app.nvim.out_write("Action is aborted\n")
        except NoteExists as e:
            self.app.nvim.out_write(f"Note exists: {e}\n")
        except ApplicationException as e:
            self.app.nvim.out_write(f"{e}\n")

    return decorated
