import fileinput
import os
import sys

from kb_notes.application import Application
from kb_notes.exeptions import NoteExists


class NoteRenamer:
    def __init__(self, app: Application):
        self.app = app

    def rename_note(self, old_note_name: str, new_note_name: str):
        children_note = [
            file.replace(".md", "")
            for file in self.app.note_finder.find_children(old_note_name)
        ]
        new_children_note = [
            note.replace(old_note_name, new_note_name, 1) for note in children_note
        ]

        existing_files = []
        for note in new_children_note:
            if os.path.isfile(self.app.note_finder.get_full_path_for_note(note)):
                existing_files.append(note)

        if os.path.isfile(self.app.note_finder.get_full_path_for_note(new_note_name)):
            existing_files.append(new_note_name)

        if existing_files:
            raise NoteExists(existing_files)

        self._process_note(old_note_name, new_note_name)

        for old_child_name, new_child_name in zip(children_note, new_children_note):
            self._process_note(old_child_name, new_child_name)

    def _process_note(self, old_note_name: str, new_note_name: str):
        self._update_links(old_note_name, new_note_name)
        self._update_title(old_note_name, new_note_name)
        self._move_note(old_note_name, new_note_name)

    def _update_links(self, old_note_name: str, new_note_name: str):
        linked_notes = self.app.note_finder.find_backlinks(old_note_name)

        for note in linked_notes:
            with fileinput.input(
                self.app.note_finder.get_full_path_for_note(note.replace(".md", "")),
                inplace=True,
            ) as f:
                for line in f:
                    line = line.replace(f"[[{old_note_name}]]", f"[[{new_note_name}]]")
                    sys.stdout.write(line)

    def _update_title(self, old_note_name: str, new_note_name: str):
        with fileinput.input(
            self.app.note_finder.get_full_path_for_note(
                old_note_name.replace(".md", "")
            ),
            inplace=True,
        ) as f:
            for line, text in enumerate(f):
                if line == 0 and text == f"# {old_note_name}\n":
                    text = f"# {new_note_name}\n"

                sys.stdout.write(text)

    def _move_note(self, old_note_name: str, new_note_name: str):
        os.rename(
            self.app.note_finder.get_full_path_for_note(old_note_name),
            self.app.note_finder.get_full_path_for_note(new_note_name),
        )
