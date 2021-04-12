from deoplete.base.source import Base

from kb_notes.application import Application


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = "kb_notes"
        self.mark = "[KB]"
        self.min_pattern_length = 1
        self.rank = 500
        self.filetypes = ["markdown"]
        self.app = Application(nvim=vim)

    def get_complete_position(self, context):
        # trigger completion if we"re currently in the [[link]] syntax
        pos = context["input"].rfind("[[")
        return pos if pos < 0 else pos + 2

    def gather_candidates(self, context):
        contents = []

        for file_name in self.app.note_finder.find_notes():
            base_file_name = file_name[:-3]
            contents.append({"word": base_file_name + "]]", "abbr": base_file_name})

        return contents
