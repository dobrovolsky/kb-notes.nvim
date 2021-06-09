import os
import re
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
                f"\\[\\[{note_name}(#([-a-zA-Z0-9\\.\\s]*))?(\\|([-a-zA-Z0-9\\.\\s]*))?(\\^([-a-zA-Z0-9\\.\\s]*))?\\]\\]",
                self.config.note_folder,
            ],
        )

        for line in backlinks.split("\n"):
            if line:
                backlinks_files.append(self.get_note_name(line))

        return backlinks_files

    def find_children(self, note_name: str) -> List[str]:
        pattern = re.compile(f"^{note_name}[.](?!md)")
        notes = self.find_notes()

        def is_child(parent, child):
            return parent in child and pattern.match(child)

        return [note for note in notes if is_child(note_name, note)]

    def find_notes(self) -> List[str]:
        res = execute_command(
            ["ls", "-t", self.config.note_folder],
        )
        return [
            self.get_note_name(line)
            for line in res.split("\n")
            if line and line.endswith(".md")
        ]

    def find_parent(self, note_name: str) -> Optional[str]:
        hierarchy = self.get_parent_notes_hierarchy(note_name)

        if not hierarchy:
            return

        return hierarchy[-1]

    def get_not_existing_parents(self, note_name: str) -> List[str]:
        not_existing_parents = []
        for parent in self.get_parent_notes_hierarchy(note_name):
            if not os.path.isfile(self.get_full_path_for_note(parent)):
                not_existing_parents.append(parent)

        return not_existing_parents

    @staticmethod
    def get_parent_notes_hierarchy(note_name: str) -> List[str]:
        hierarchy = note_name.split(".")[:-1]

        res = []
        for i, _ in enumerate(hierarchy, start=1):
            res.append(".".join(hierarchy[:i]))

        return res

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
