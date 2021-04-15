import random
import re
import unicodedata

from pynvim import (
    NvimError,
)

from kb_notes.application import Application
from kb_notes.helpers import (
    buffer_is_empty,
    current_note_name,
)
from kb_notes.config import (
    ALLOWED_CHARS_PATTERN,
    DEFAULT_SEPARATOR,
    OPEN_NOTE_SINK,
)
from kb_notes.preview import Preview


class Note:
    def __init__(
        self,
        app: Application,
        preview: Preview,
    ):
        self.app = app
        self.preview = preview

    @staticmethod
    def slugify(text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = text.lower()
        text = text.strip()
        text = re.sub(ALLOWED_CHARS_PATTERN, DEFAULT_SEPARATOR, text)
        return text

    def insert_template(self, note_name: str):
        note_content = self.app.config.template.format(note_name=note_name)
        self.app.nvim.current.buffer[:] = note_content.split("\n")

    def command_new_note(self):
        try:
            note_name = self.app.nvim.eval(
                f"input('Enter note name: ', '{current_note_name(self.app.nvim)}')"
            )
        except NvimError as e:
            self.app.nvim.out_write(f"{e}\n")
            return

        note_name_normalized = self.slugify(note_name)
        if not note_name_normalized:
            self.app.nvim.out_write("filename is required\n")
            return

        self.app.nvim.command(
            f"e {self.app.note_finder.get_full_path_for_note(note_name_normalized)}"
        )

        if buffer_is_empty(self.app.nvim.current.buffer):
            self.insert_template(note_name_normalized)
            self.app.nvim.command("w")

    def command_random_note(self):
        note_file = random.choice(self.app.note_finder.find_notes())
        self.app.nvim.command(
            f"e {self.app.note_finder.get_full_path_for_note(note_file)}"
        )

    def command_search_note(self):
        self.preview.fzf_with_preview(
            source=self.app.note_finder.find_notes(),
            sink=OPEN_NOTE_SINK,
            location=self.app.config.note_folder,
        )

    def command_search_note_with_prefix(self):
        self.preview.fzf_with_preview(
            source=self.app.note_finder.find_notes(),
            sink=OPEN_NOTE_SINK,
            location=self.app.config.note_folder,
            search_term=f"^{current_note_name(self.app.nvim)}",
        )
