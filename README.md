# KB Notes

Yet another note management system for neovim.

Supports:

- linking notes with `[[note-name]]`
- discovering backlinks
- hierarchy in notes using `.` Example: `aws`, `aws.ec2`, `aws.ec2.security-groups`
  See [Dendron](https://wiki.dendron.so/notes/c6fd6bc4-7f75-4cbb-8f34-f7b99bfe2d50.html#hierarchies)
- note renaming, updates backlinks, child notes

## Installation

Internally uses following tools:

- [nvim](https://neovim.io/)
- [pynvim](https://github.com/neovim/pynvim)
- [fzf](https://github.com/junegunn/fzf)
- [fd](https://github.com/sharkdp/fd)
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

`g:kb_notes_path` - path to your notes.

`g:kb_notes_template_path` - override default template for new note.

String `{note_name}` will be replaced with note name

`g:kb_note_post_init` - allows you to execute function as callback when note loaded in buffer.

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

- `KBNewNote` - creates new note in root folder
- `KBSearchNote` - initiates search of notes
- `KBSearchNoteWithPrefix` - initiates search with current note name as query
- `KBOpenLink` - follows via wikilink reference or markdown url
- `KBGetLinks` - finds all connected notes (links from current file, backlinks, children notes)
- `KBGoToParentNote` - navigates to parent note
- `KBLinkSuggestion` - inserts wikilink
- `KBRenameNote` - renames note (updates child notes and backlinks)
- `KBRandomNote` - opens random note
- `KBSpellSuggestion` - replaces word with correct spelling

Use `ctrl-e` to toggle preview in fzf.
