import os
from functools import lru_cache

from kb_notes.application import Application
from kb_notes.helpers import (
    find_all,
)
from kb_notes.config import (
    WIKILINK_NOT_EXISTS_COLOR,
    WIKILINK_EXISTS_COLOR,
    WIKILINK_EXISTS,
    WIKILINK_NOT_EXISTS,
    WIKILINK_HIGHLIGHT_GROUP,
    URL_LINK_HIGHLIGHT_GROUPS,
)


class Highlight:
    def __init__(self, app: Application):
        self.app = app

        self.highlight_src = self.app.nvim.new_highlight_source()
        self.current_buffer_wiki_links = []

    @property
    def highlightgroup_under_cursor(self) -> str:
        return self.app.nvim.eval("synIDattr(synID(line('.'), col('.'), 1), 'name')")

    @property
    def is_wikilink_under_cursor(self) -> bool:
        return self.highlightgroup_under_cursor == WIKILINK_HIGHLIGHT_GROUP

    @property
    def is_url_under_cursor(self) -> bool:
        return self.highlightgroup_under_cursor in URL_LINK_HIGHLIGHT_GROUPS

    @lru_cache(maxsize=4096)
    def get_highlights(self, line: int, text: str, note_name: str):
        wikilink = f"[[{note_name}]]".encode()
        highlights = []

        for start in find_all(text.encode(), wikilink):
            end = start + len(wikilink)

            if os.path.isfile(
                self.app.note_finder.get_full_path_for_note(note_name=note_name)
            ):
                highlight_name = WIKILINK_EXISTS
            else:
                highlight_name = WIKILINK_NOT_EXISTS

            highlights.append((highlight_name, line, start, end))

        return highlights

    def highlight_wikilinks(self):
        buf = self.app.nvim.current.buffer

        highlights = []

        for file in self.app.note_finder.find_links_in_lines(
            self.app.nvim.current.buffer
        ):
            note_name = os.path.splitext(file)[0]

            for line, text in enumerate(buf):
                highlights += self.get_highlights(
                    line=line,
                    text=text,
                    note_name=note_name,
                )

        if highlights:
            buf.update_highlights(src_id=self.highlight_src, hls=highlights, clear=True)

            self.app.nvim.command(f"hi {WIKILINK_EXISTS} guifg={WIKILINK_EXISTS_COLOR}")
            self.app.nvim.command(
                f"hi {WIKILINK_NOT_EXISTS} guifg={WIKILINK_NOT_EXISTS_COLOR}"
            )

        self.current_buffer_wiki_links = highlights
