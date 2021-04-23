from typing import NamedTuple


class WikiLinkRegexMatch(NamedTuple):
    name: str
    reference: str
    alias: str
    block_reference: str
    original: str


class RenameNote(NamedTuple):
    old_note_name: str
    new_note_name: str
