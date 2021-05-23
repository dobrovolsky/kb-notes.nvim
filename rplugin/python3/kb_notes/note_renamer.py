import fileinput
import os
import sys
from typing import (
    List,
)


from kb_notes.application import Application
from kb_notes.config import WIKILINK_PATTERN
from kb_notes.exeptions import (
    NoteExists,
    ActionAborted,
)

from kb_notes.helpers import (
    current_note_name,
    slugify,
    capture_input,
    confirm_action,
)
from kb_notes.types import RenameNote


class NoteRenamer:
    def __init__(self, app: Application):
        self.app = app

    def command_rename_note(self):
        new_note_name = capture_input(
            self.app.nvim, "Enter note name: ", default=current_note_name(self.app.nvim)
        )

        if not new_note_name:
            raise ActionAborted

        new_note_name_normalized = slugify(new_note_name)

        not_existing_parents = self.app.note_finder.get_not_existing_parents(
            new_note_name_normalized
        )
        if not_existing_parents:
            confirmed = confirm_action(
                self.app.nvim,
                f"Notes: [{', '.join(not_existing_parents)}] do not exist",
            )
            if not confirmed:
                raise ActionAborted

        self.app.nvim.command("w")

        renamed = self.rename_note(
            RenameNote(
                old_note_name=current_note_name(self.app.nvim),
                new_note_name=new_note_name_normalized,
            )
        )
        self.app.nvim.command(
            f"e {self.app.note_finder.get_full_path_for_note(new_note_name_normalized)}"
        )

        # close all buffers but not current one
        self.app.nvim.command("w | %bd | e#")

        message = ""
        for note in renamed:
            message += f"{note.old_note_name} -> {note.new_note_name}\n"

        self.app.nvim.command(f"echo '{message}'")

    def rename_note(self, rename_note: RenameNote) -> List[RenameNote]:
        children_note = self.app.note_finder.find_children(rename_note.old_note_name)
        new_children_note = [
            note.replace(rename_note.old_note_name, rename_note.new_note_name, 1)
            for note in children_note
        ]

        existing_files = []
        for note in new_children_note:
            if os.path.isfile(self.app.note_finder.get_full_path_for_note(note)):
                existing_files.append(note)

        if os.path.isfile(
            self.app.note_finder.get_full_path_for_note(rename_note.new_note_name)
        ):
            existing_files.append(rename_note.new_note_name)

        if existing_files:
            raise NoteExists(existing_files)

        self._process_note(rename_note)

        processed = [rename_note]

        for old_child_name, new_child_name in zip(children_note, new_children_note):
            note = RenameNote(
                old_note_name=old_child_name, new_note_name=new_child_name
            )
            self._process_note(note)
            processed.append(note)

        return processed

    def _process_note(self, rename_note: RenameNote):
        self._update_links(rename_note)
        self._update_title(rename_note)
        self._move_note(rename_note)

    def _update_links(self, rename_note: RenameNote):
        linked_notes = self.app.note_finder.find_backlinks(rename_note.old_note_name)

        for note in linked_notes:
            with fileinput.input(
                self.app.note_finder.get_full_path_for_note(note.replace(".md", "")),
                inplace=True,
            ) as f:
                for line in f:
                    for link in WIKILINK_PATTERN.finditer(line):
                        if link["note"] == rename_note.old_note_name:
                            old_note_full = link.string[link.start() : link.end()]
                            new_note_full = old_note_full.replace(
                                rename_note.old_note_name, rename_note.new_note_name
                            )

                            line = line.replace(old_note_full, new_note_full)

                    sys.stdout.write(line)

    def _update_title(self, rename_note: RenameNote):
        with fileinput.input(
            self.app.note_finder.get_full_path_for_note(
                rename_note.old_note_name.replace(".md", "")
            ),
            inplace=True,
        ) as f:
            for line, text in enumerate(f):
                if line == 0 and text == f"# {rename_note.old_note_name}\n":
                    text = f"# {rename_note.new_note_name}\n"

                sys.stdout.write(text)

    def _move_note(self, rename_note: RenameNote):
        os.rename(
            self.app.note_finder.get_full_path_for_note(rename_note.old_note_name),
            self.app.note_finder.get_full_path_for_note(rename_note.new_note_name),
        )
