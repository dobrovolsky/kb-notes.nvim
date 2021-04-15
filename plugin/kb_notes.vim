let $KB_NOTES_SOURCE = g:kb_notes_path

let g:kb_notes_fzf_options = get(g:, 'kb_notes_fzf_options', "--bind='ctrl-e:toggle-preview' --preview 'bat --color=always " . g:kb_notes_path . "/{}.md'")

if exists("g:loaded_kb")
  finish
endif

" define autocmd for plugin
augroup KbGroup
  autocmd!
  autocmd BufNewFile,BufRead,BufEnter $KB_NOTES_SOURCE/*.md call s:load_kb_settings()
  autocmd BufEnter,TextChanged,TextChangedI $KB_NOTES_SOURCE/*.md KBHighlightWikiLinks
  autocmd ColorScheme * KBHighlightWikiLinks
augroup END

function! s:load_kb_settings()
  " OpenLink uses this command
  syntax match wikiLink /\[\[.\{-}\]\]/ containedin=mkdNonListItemBlock,mkdListItemLine

  if exists("g:kb_note_post_init")
    let FuncRef = function(g:kb_note_post_init)
    call FuncRef()
  endif
endfunction

let g:loaded_kb = 1
