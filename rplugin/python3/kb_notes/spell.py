from kb_notes.application import Application
from kb_notes.config import SPELL_SUGGESTION_SINK


class Spell:
    def __init__(self, app: Application):
        self.app = app

    def command_spell_suggestion_sink(self, args):
        word = "".join(args).replace("\\", "")
        self.app.nvim.command(f'normal "_ciw{word}')

    def command_spell_suggestion(self):
        suggestions = self.app.nvim.eval("spellsuggest(expand('<cword>'))")

        if suggestions:
            self.app.nvim.call(
                "fzf#run",
                {
                    "source": suggestions,
                    "sink": SPELL_SUGGESTION_SINK,
                    "window": {"width": 0.4, "height": 0.4},
                },
            )
