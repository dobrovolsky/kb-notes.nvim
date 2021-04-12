import pynvim

from kb_notes.application import Application
from kb_notes.highlight import Highlight
from kb_notes.link import Link
from kb_notes.note import Note
from kb_notes.config import (
    LINK_SUGGESTION_SINK_FIND_AND_REPLACE_NOTE,
    LINK_SUGGESTION_SINK_INSERT_NOTE,
    SPELL_SUGGESTION_SINK,
)
from kb_notes.note_renamer import NoteRenamer
from kb_notes.spell import Spell


@pynvim.plugin
class NotesPlugin:
    def __init__(self, nvim: pynvim.Nvim):
        app = Application(nvim=nvim)

        self.spell = Spell(app)
        self.highlight = Highlight(app)
        self.note = Note(app)
        self.link = Link(
            app=app,
            highlight=self.highlight,
            note=self.note,
            note_renamer=NoteRenamer(app),
        )

    #############################################################
    # Links
    #############################################################
    @pynvim.command("KBGetLinks")
    def get_links(self):
        self.link.get_links()

    @pynvim.command("KBOpenLink")
    def open_link(self):
        self.link.open_link()

    @pynvim.command(LINK_SUGGESTION_SINK_FIND_AND_REPLACE_NOTE, nargs="*")
    def link_suggestion_sink_find_note_and_replace(self, args):
        self.link.link_suggestion_sink_find_note_and_replace(args)

    @pynvim.command(LINK_SUGGESTION_SINK_INSERT_NOTE, nargs="*")
    def link_suggestion_sink_insert_note(self, args):
        self.link.link_suggestion_sink_insert_note(args)

    @pynvim.command("KBLinkSuggestion")
    def link_suggestion(self):
        self.link.link_suggestion()

    @pynvim.command("KBGoToParentNote")
    def go_up(self):
        self.link.go_to_parent_note()

    @pynvim.command("KBRenameNote")
    def rename_note(self):
        self.link.rename_note()

    #############################################################
    # Notes
    #############################################################
    @pynvim.command("KBNewNote")
    def new_note(self):
        self.note.new_note()

    @pynvim.command("KBRandomNote")
    def random_note(self):
        self.note.random_note()

    @pynvim.command("KBSearchNote")
    def search_note(self):
        self.note.search_note()

    @pynvim.command("KBSearchNoteWithPrefix")
    def search_note_with_prefix(self):
        self.note.search_note_with_prefix()

    #############################################################
    # Highlight
    #############################################################
    @pynvim.command("KBHighlightWikiLinks")
    def highlight_wikilinks(self):
        self.highlight.highlight_wikilinks()

    #############################################################
    # Spelling
    #############################################################
    @pynvim.command(SPELL_SUGGESTION_SINK, nargs="*")
    def spell_suggestion_sink(self, args):
        self.spell.spell_suggestion_sink(args)

    @pynvim.command("KBSpellSuggestion")
    def spell_suggestion(self):
        self.spell.spell_suggestion()
