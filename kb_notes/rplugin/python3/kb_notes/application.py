import pynvim

from kb_notes.config import Config
from kb_notes.note_finder import NoteFinder


class Application:
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim
        self.config = Config(self.nvim)
        self.note_finder = NoteFinder(self.config)
