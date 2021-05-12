import time

from deoplete.base.source import Base

from kb_notes.application import Application


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = "kb_notes"
        self.mark = "[KB]"
        self.min_pattern_length = 0
        self.rank = 500
        self.filetypes = ["markdown"]
        self.matchers = ["matcher_full_fuzzy"]
        self.app = Application(nvim=vim)

        self.MAX_CACHE_AGE_SECONDS = 5
        self.last_update = None
        self.results = None

    def _get_notes(self):
        if (
            not self.last_update
            or time.time() - self.last_update > self.MAX_CACHE_AGE_SECONDS
        ):
            self.results = []

            for file_name in self.app.note_finder.find_notes():
                self.results.append({"word": file_name + "]]", "abbr": file_name})

            self.last_update = time.time()
        return self.results

    def get_complete_position(self, context):
        pos = context["input"].rfind("[[")
        return pos if pos < 0 else pos + 2

    def gather_candidates(self, context):
        return self._get_notes()
