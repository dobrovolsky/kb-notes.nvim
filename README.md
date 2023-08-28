# kb-notes.nvim

Yet another note management system for neovim.

Supports:

- linking notes with `[[note-name]]`
- hierarchy in notes using `.` Example: `aws`, `aws.ec2`, `aws.ec2.security-groups`
- discovering backlinks
- note renaming: updates backlinks, update child notes names and titles

## Known issues

- Not garanteed to work for anybody except me. I use it for my own notes.
- Support only `AZaz09.-` in note names
- Works only for notes in the same directory
- Following a url link does not work without [treesitter](https://github.com/nvim-treesitter/nvim-treesitter)

## Installation

Install with your favorite plugin manager.

Example for [lazy.nvim](https//github.com/folke/lazy.nvim)

```lua
require("lazy").setup({
  { 
    dir = '~/projects/kb_notes',
    dependencies = {
      'ibhagwan/fzf-lua',
      -- open markdown link
      'jghauser/follow-md-links.nvim',
      -- nice notifcaitons
      'rcarriga/nvim-notify',
    },
  },
}

require('kb_notes').setup {
  -- Required: path to your notes
  notes_path = '/Users/s/kb/notes/',
  -- Optinal: use a custom post init function
  note_post_init = KBPostInit
}

-- Example post init function
function KBPostInit()
  -- set spelling
  vim.opt_local.spell = true
  vim.opt_local.spelllang = "uk,en,ru"

  -- insert wikilink
  vim.api.nvim_buf_set_keymap(0, 'i', '<c-e>', '<esc>:KBLinkSuggestion<cr>', {})
  vim.api.nvim_buf_set_keymap(0, 'n', '<c-e>', ':KBLinkSuggestion<cr>', {})
  -- find suggestion for word under cursor
  vim.api.nvim_buf_set_keymap(0, 'n', 'zf', ':KBSpellSuggest<cr>', {})
  -- create new note
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>nn', ':KBNewNote<cr>', {})
  -- rename note
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>re', ':KBRenameNote<cr>', {})
  -- go to parent of current note
  vim.api.nvim_set_keymap('n', '<leader>u', ':KBGoToParentNote<cr>', {})
  -- search for parent notes
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>U', ':KBShowParentNotes<cr>', {})
  -- open random note
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>or', ':KBRandomNote<cr>', {})
  -- follow via wikilink
  vim.api.nvim_buf_set_keymap(0, 'n', 'gd', ':KBOpenLink<cr>', {})
  -- find all links from and to current buffer
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>nl', ':KBGetLinks<cr>', {})
  -- search note with predefined query
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>sl', ':KBSearchNoteWithPrefix<cr>', {})
  -- search connected links for link under cursor
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>sc', ':KBShowConnectedNotesForLink<cr>', {})

  -- use prettier and update title with filename for w and q
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>q', ':Neoformat<cr>:KBUpdateNoteHeader<cr>:wq<cr>', {})
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>w', ':Neoformat<cr>:KBUpdateNoteHeader<cr>:w<cr>', {})
  --vim.api.nvim_buf_set_keymap(0, 'n', '<leader>q', ':KBUpdateNoteHeader()<cr>:wq<cr>', {})
  --vim.api.nvim_buf_set_keymap(0, 'n', '<leader>w', ':KBUpdateNoteHeader()<cr>:w<cr>', {})

  -- find all backlinks
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>bl', ':KBShowBacklinks<cr>', {})
  -- open file as mind map in browser
  vim.api.nvim_buf_set_keymap(0, 'n', '<leader>fs', ':KBOpenMap<cr>', {})
```

## List of commands

### General commands

- `:LoadKBSettings` - is executed on BufEnter and loads all settings for the current buffer
- `:KBGoToParentNote` - opens parent note
- `:KBLinkSuggestion` - shows suggestions for wikilink
- `:KBNewNote` - creates new note
- `:KBRandomNote` - opens random note
- `:KBRenameNote` - renames current note
- `:KBSearchNoteWithPrefix` - searches note with predefined query and prefix
- `:KBSearchNote` - searches note with predefined query
- `:KBShowBacklinks` - shows all backlinks for current note
- `:KBSpellSuggest` - shows suggestions for word under cursor
- `:KBUpdateNoteHeader` - updates note header with filename and prettifies markdown

### Additional commands

This is very specific commands that I use for my own notes.

- `:KBOpenLink` - opens link under cursor
- `:KBOpenMap` - opens current note as mind map in browser
- `:KBPasteImg` - pastes image from clipboard to current note
- `:KBPrevDay` - opens previous daily note
