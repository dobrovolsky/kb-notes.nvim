# Change Log

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project DOES NOT adhere
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.0.12

## Added

New optional parameter `template` to override default template

## 0.0.11

Rewrite plugin code in lua.

### Updated:

New list of commands:

#### General commands

- `:LoadKBSettings` - is executed on BufEnter and loads all settings for the current buffer
- `:KBGoToParentNote` - opens parent note
- `:KBLinkSuggestion` - shows suggestions for wikilink
- `:KBNewNote` - creates new note
- `:KBRandomNote` - opens random note
- `:KBRenameNote` - renames current note
- `:KBSearchNoteWithPrefix` - searches note with a predefined query and prefix
- `:KBSearchNote` - searches note with a predefined query
- `:KBShowBacklinks` - shows all backlinks for current note
- `:KBSpellSuggest` - shows suggestions for word under cursor
- `:KBUpdateNoteHeader` - updates note header with filename and prettifies markdown

#### Additional commands

This is a very specific command that I use for my own notes.

- `:KBOpenLink` - opens link under cursor
- `:KBOpenMap` - opens current note as a mind map in browser
- `:KBPasteImg` - pastes image from clipboard to current note
- `:KBPrevDay` - opens previous daily note

## 0.0.10

### Fixed:

- `KBLinkSuggestion` working when deoplete is uninstalled

## 0.0.9

### Added:

- Add `KBShowParentNotes` command
 
## 0.0.8

### Added:

- Drop `fd` as dependency

## 0.0.7

### Added:

- Show dialog to inform user if parent note doesn't exist for create new note and rename actions

## 0.0.6

### Fixed:

- Slugify note name when renaming

## 0.0.5

### Changed:

- Display all parent notes with `KBGetLinks`, not only direct parent

### Fixed

- Regex for getting backlinks

## 0.0.4

### Fixed

- Renaming not related note that starts with prefix as note

## 0.0.3

### Added:

- Add caching for deoplate input

### Changed:

- Use `matcher_full_fuzzy` for finding notes with deoplate
- Show deoplate panel right after `[[` is typed

### Fixed

- Note insertion with deoplate plugin

## 0.0.2

### Added:

- Support note alias (`|`) and content reference (`#`)

### Fixed

- Accessing old buffers after rename

## 0.0.1

### Added:

- Initial release
