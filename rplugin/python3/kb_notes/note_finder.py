import os
from typing import (
    List,
    Optional,
)

from kb_notes.config import (
    Config,
    WIKILINK_PATTERN,
)
from kb_notes.helpers import execute_command


class NoteFinder:
    def __init__(self, config: Config):
        self.config = config

    def get_full_path_for_note(
        self,
        note_name,
    ):
        return os.path.join(self.config.note_folder, note_name) + ".md"

    def find_backlinks(self, note_name: str) -> List[str]:
        backlinks_files = []
        backlinks = execute_command(
            [
                "rg",
                "-l",
                "-e",
                f"\\[\\[{note_name}\\]\\]",
                self.config.note_folder,
            ],
        )

        for line in backlinks.split("\n"):
            if line:
                backlinks_files.append(os.path.basename(line))

        return backlinks_files

    def find_children(self, note_name: str) -> List[str]:
        files = []
        res = execute_command(
            [
                "fd",
                f"^{note_name}[.][^md]",
                self.config.note_folder,
            ],
        )

        for line in res.split("\n"):
            if line:
                files.append(os.path.basename(line))

        return files

    def find_notes(self) -> List[str]:
        res = execute_command(
            ["ls", "-t", self.config.note_folder],
        )

        return [line for line in res.split("\n") if line and line.endswith(".md")]

    @staticmethod
    def find_parent(note_name) -> Optional[str]:
        hierarchy = note_name.split(".")

        if len(hierarchy) < 2:
            return

        return ".".join(hierarchy[:-1])

    @staticmethod
    def find_links_in_lines(lines: List[str]) -> List[str]:
        current_buffer_links = []
        for line in lines:
            current_buffer_links += WIKILINK_PATTERN.findall(line)

        return [link + ".md" for link in current_buffer_links]
