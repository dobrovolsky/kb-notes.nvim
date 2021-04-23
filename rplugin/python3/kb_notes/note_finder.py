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
from kb_notes.types import WikiLinkRegexMatch


class NoteFinder:
    def __init__(self, config: Config):
        self.config = config

    def get_full_path_for_note(
        self,
        note_name,
    ):
        return os.path.join(self.config.note_folder, note_name) + ".md"

    def get_note_name(self, path):
        return os.path.splitext(os.path.basename(path))[0]

    def find_backlinks(self, note_name: str) -> List[str]:
        backlinks_files = []
        backlinks = execute_command(
            [
                "rg",
                "-l",
                "-e",
                f"\\[\\[{note_name}(#)?([-a-zA-Z0-9\\.\\s]*)?(\\|)?([-a-zA-Z0-9\\.\\s]*)?(\\^)?([-a-zA-Z0-9\\.\\s]*)\\]\\]",
                self.config.note_folder,
            ],
        )

        for line in backlinks.split("\n"):
            if line:
                backlinks_files.append(self.get_note_name(line))

        return backlinks_files

    def find_children(self, note_name: str) -> List[str]:
        files = []
        res = execute_command(
            [
                "fd",
                f"^{note_name}",
                self.config.note_folder,
            ],
        )

        for line in res.split("\n"):
            if line:
                note = self.get_note_name(line)
                if note != note_name:
                    files.append(note)

        return files

    def find_notes(self) -> List[str]:
        res = execute_command(
            ["ls", "-t", self.config.note_folder],
        )
        return [
            self.get_note_name(line)
            for line in res.split("\n")
            if line and line.endswith(".md")
        ]

    @staticmethod
    def find_parent(note_name) -> Optional[str]:
        hierarchy = note_name.split(".")

        if len(hierarchy) < 2:
            return

        return ".".join(hierarchy[:-1])

    @staticmethod
    def find_links_in_lines(lines: List[str]) -> List[WikiLinkRegexMatch]:
        current_buffer_links = []
        for line in lines:
            for link in WIKILINK_PATTERN.finditer(line):
                current_buffer_links.append(
                    WikiLinkRegexMatch(
                        name=link["note"],
                        reference=link["reference"],
                        alias=link["alias"],
                        block_reference=link["block_reference"],
                        original=link.string[link.start() : link.end()],
                    )
                )
        return current_buffer_links
