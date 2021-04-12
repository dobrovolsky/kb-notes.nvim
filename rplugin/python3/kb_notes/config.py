import re

from pynvim import (
    Nvim,
    NvimError,
)

from kb_notes.exeptions import PathIsNotDefined

WIKILINK_PATTERN = re.compile(r"\[\[([-a-z0-9\.]*)\]\]")
WIKILINK_HIGHLIGHT_GROUP = "wikiLink"
URL_LINK_HIGHLIGHT_GROUPS = {"mkdURL", "mkdLink"}
ALLOWED_CHARS_PATTERN = re.compile(r"[^-a-z0-9\.]+")
DEFAULT_SEPARATOR = "-"

WIKILINK_EXISTS = "WikiLinkExisting"
WIKILINK_NOT_EXISTS = "WikiLinkNotExisting"

WIKILINK_EXISTS_COLOR = "#98971a"
WIKILINK_NOT_EXISTS_COLOR = "#fb4934"

LINK_SUGGESTION_SINK_FIND_AND_REPLACE_NOTE = "KBLinkSuggestionSinkFindAndReplaceNote"
LINK_SUGGESTION_SINK_INSERT_NOTE = "KBLinkSuggestionSinkInsertNote"

SPELL_SUGGESTION_SINK = "KBSpellSuggestionSink"


class Config:
    def __init__(self, nvim: Nvim):
        self.nvim = nvim

    @property
    def note_folder(self):
        try:
            return self.nvim.eval("g:kb_notes_path")
        except NvimError:
            raise PathIsNotDefined

    @property
    def template(self):
        try:
            template_path = self.nvim.eval("g:kb_notes_template_path")
        except NvimError:
            template = "# {note_name}\n\n## References\n\n## Links\n\n## Notes\n\n"
        else:
            with open(template_path) as f:
                template = f.read()

        return template
