import pynvim

from kb_notes.application import Application
from kb_notes.helpers import handle_exceptions
from kb_notes.highlight import Highlight
from kb_notes.link import Link
from kb_notes.note import Note
from kb_notes.config import (
    LINK_SUGGESTION_SINK_FIND_AND_REPLACE_NOTE,
    LINK_SUGGESTION_SINK_INSERT_NOTE,
    OPEN_NOTE_SINK,
)
from kb_notes.note_renamer import NoteRenamer
from kb_notes.preview import Preview


@pynvim.plugin
class NotesPlugin:
    def __init__(self, nvim: pynvim.Nvim):
        self.app = Application(nvim=nvim)
        preview = Preview(self.app)

        self.note_renamer = NoteRenamer(self.app)
        self.highlight = Highlight(self.app)

        self.note = Note(self.app, preview=preview)
        self.link = Link(
            app=self.app, highlight=self.highlight, note=self.note, preview=preview
        )

    #############################################################
    # Notes
    #############################################################
    @handle_exceptions
    @pynvim.command("KBNewNote")
    def new_note(self):
        self.note.command_new_note()

    #############################################################
    # Renaming
    #############################################################
    @handle_exceptions
    @pynvim.command("KBRenameNote")
    def rename_note(self):
        self.note_renamer.command_rename_note()
