class ApplicationException(Exception):
    ...


class NoteExists(ApplicationException):
    ...


class InputError(ApplicationException):
    ...


class ActionAborted(ApplicationException):
    ...


class PathIsNotDefined(ApplicationException):
    def __init__(self):
        super().__init__(
            "Path to notes is not defined. Please add let g:kb_notes_path to your config file"
        )
