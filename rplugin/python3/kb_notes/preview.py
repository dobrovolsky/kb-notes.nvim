from typing import Optional

from kb_notes.application import Application


class Preview:
    def __init__(self, app: Application):
        self.app = app

    def fzf_with_preview(
        self,
        source: list,
        sink: str,
        location: str,
        search_term: Optional[str] = None,
    ):
        options = self.app.config.fzf_options

        if search_term:
            options = f"{options} -q {search_term}"

        self.app.nvim.call(
            "fzf#run",
            self.app.nvim.call(
                "fzf#wrap",
                {
                    "source": source,
                    "sink": sink,
                    "dir": location,
                    "options": options,
                },
            ),
        )
