# kb-notes.nvim

Yet another note management system for neovim.

Inspired by [Dendron](https://wiki.dendron.so/)

Supports:

- linking notes with `[[note-name]]`. Also supports:
  - pipes: `[[note-name|note alias]]` - follow a link and ignores alias.
  - block reference: `[[note-name#Reference text]]` - follow a link and performs search for `Reference text`
- highlighting existing and not existing links
- discovering backlinks
- note renaming, updates backlinks, child notes
- [deoplete](https://github.com/Shougo/deoplete.nvim) integration
- hierarchy in notes using `.` Example: `aws`, `aws.ec2`, `aws.ec2.security-groups`

## Installation

Internally uses following tools:

- [nvim](https://neovim.io/)
- [pynvim](https://github.com/neovim/pynvim)
- [fzf](https://github.com/junegunn/fzf)
- [rg](https://github.com/BurntSushi/ripgrep)

Make sure you have installed these dependencies.

For vim-plug:

```viml
call plug#begin('$HOME/.vim/vim-plug')
  Plug 'dobrovolsky/kb_notes', { 'do': ':UpdateRemotePlugins' }

  Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
  Plug 'junegunn/fzf.vim'
  " (Optional) to open markdown url in browser
  Plug 'plasticboy/vim-markdown'

call plug#end()

" Replace with your own directory or create new one
" mkdir ~/notes
" touch ~/notes/index.md
let g:kb_notes_path=expand('~/notes')
map <leader>kb :KBGetLinks<cr>
```

## Settings

#### Note path

`g:kb_notes_path`

Change path to your notes

```viml
let g:kb_notes_path=expand('~/notes')
```

#### Template

`g:kb_notes_template_path`

Override default template for new note.

```viml
let g:kb_notes_template_path=expand('~/notes/templates/main.md')
```

Pattern `{note_name}` will be replaced with note name

#### FZF options

`g:kb_notes_fzf_options`

Define your own options for fzf preview window

```viml
let g:kb_notes_fzf_options="--bind='ctrl-e:toggle-preview' --preview 'bat --color=always " . g:kb_notes_path . "/{}.md'"
```

#### Post init hook

`g:kb_note_post_init`

Allows you to execute function as callback when note loaded in buffer.

Can be used to define `<buffer>` related mappings and local settings

Example define mappings only when editing your notes:

```viml
let g:kb_note_post_init = "Kb_note_post_init"

function! Kb_note_post_init()
  " insert wikilink
  nnoremap <buffer><c-e> <esc>:KBLinkSuggestion<cr>
  inoremap <buffer><c-e> <esc>:KBLinkSuggestion<cr>
  " find suggestion for word under cursor
  nnoremap <buffer> zf :KBSpellSuggestion<CR>
  " create new note
  nnoremap <buffer> <leader>nn :KBNewNote<cr>
  " rename note
  nnoremap <buffer> <leader>re :KBRenameNote<cr>
  " go to pattent of current note
  nnoremap <leader>u :KBGoToParentNote<cr>
  " open random note
  nnoremap <buffer> <leader>or :KBRandomNote<cr>
  " follow via wikilink
  nnoremap <buffer> gd :KBOpenLink<cr>
  " find all links from and to current buffer
  nnoremap <buffer> <leader>nl :KBGetLinks<cr>
  " search note with predifined query
  nnoremap <buffer> <leader>sl :KBSearchNoteWithPrefix<cr>
endfunction
```

## Commands

- `KBGetLinks` - finds all connected notes (links from current file, backlinks, children notes)
- `KBGoToParentNote` - navigates to parent note
- `KBLinkSuggestion` - inserts wikilink
- `KBNewNote` - creates new note in root folder
- `KBOpenLink` - follows via wikilink reference or markdown url
- `KBRandomNote` - opens random note
- `KBRenameNote` - renames note (updates child notes and backlinks)
- `KBSearchNoteWithPrefix` - initiates search with current note name as query
- `KBSearchNote` - initiates search of notes
- `KBShowConnectedNotesForLink` - finds links for link under cursor (links from current file, backlinks, children notes)
- `KBShowParentNotes` - finds all parent notes

Use `ctrl-e` to toggle preview in fzf.
