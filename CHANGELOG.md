# Change Log

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project DOES NOT adhere
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
