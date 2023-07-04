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
    # Links
    #############################################################
    @handle_exceptions
    @pynvim.command("KBGetLinks")
    def get_links(self):
        self.link.command_get_links()

    @handle_exceptions
    @pynvim.command("KBOpenLink")
    def open_link(self):
        self.link.command_open_link()

    @handle_exceptions
    @pynvim.command(OPEN_NOTE_SINK, nargs="*")
    def open_note_sink(self, args):
        self.link.command_open_note_sink(args)

    @handle_exceptions
    @pynvim.command(LINK_SUGGESTION_SINK_FIND_AND_REPLACE_NOTE, nargs="*")
    def link_suggestion_sink_find_note_and_replace(self, args):
        self.link.command_link_suggestion_sink_find_note_and_replace(args)

    @handle_exceptions
    @pynvim.command(LINK_SUGGESTION_SINK_INSERT_NOTE, nargs="*")
    def link_suggestion_sink_insert_note(self, args):
        self.link.command_link_suggestion_sink_insert_note(args)

    @handle_exceptions
    @pynvim.command("KBLinkSuggestion")
    def link_suggestion(self):
        self.link.command_link_suggestion()

    @handle_exceptions
    @pynvim.command("KBGoToParentNote")
    def go_up(self):
        self.link.command_go_to_parent_note()

    @handle_exceptions
    @pynvim.command("KBShowParentNotes")
    def show_parent_notes(self):
        self.link.command_show_parent_notes()

    @handle_exceptions
    @pynvim.command("KBShowConnectedNotesForLink")
    def show_connected_notes_for_link(self):
        self.link.command_show_connected_notes_for_link()

    #############################################################
    # Notes
    #############################################################
    @handle_exceptions
    @pynvim.command("KBNewNote")
    def new_note(self):
        self.note.command_new_note()

    @handle_exceptions
    @pynvim.command("KBRandomNote")
    def random_note(self):
        self.note.command_random_note()

    @handle_exceptions
    @pynvim.command("KBSearchNote")
    def search_note(self):
        self.note.command_search_note()

    @handle_exceptions
    @pynvim.command("KBSearchNoteWithPrefix")
    def search_note_with_prefix(self):
        self.note.command_search_note_with_prefix()

    #############################################################
    # Highlight
    #############################################################
    @handle_exceptions
    @pynvim.command("KBHighlightWikiLinks")
    def highlight_wikilinks(self):
        self.highlight.command_highlight_wikilinks()

    #############################################################
    # Renaming
    #############################################################
    @handle_exceptions
    @pynvim.command("KBRenameNote")
    def rename_note(self):
        self.note_renamer.command_rename_note()
