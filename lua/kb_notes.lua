local M = {}
local config = {}

local function load_kb_settings()
     -- OpenLink uses this command
     vim.cmd([[syntax match wikiLink /\[\[.\{-}\]\]/ containedin=mkdNonListItemBlock,mkdListItemLine,htmlH1,htmlH2,htmlH3,htmlH4,htmlH5,htmlH6]])

     -- Run user defined post init function
     -- This is useful for setting up mappings
     if config.note_post_init ~= nil then
          config.note_post_init()
     end
end


-- Setup autocmds used by the plugin
-- This is done so that the user doesn't have to
-- setup the autocmds themselves or run the LoadKBSettings command
local function setupAutocmd()
     vim.api.nvim_create_augroup('KbGroup', { clear = true })
     vim.api.nvim_create_autocmd({'BufNewFile', 'BufRead', 'BufEnter'}, {
          group = 'KbGroup',
          pattern = config.notes_path .. '*.md',
          command = 'LoadKBSettings',
     })
     vim.api.nvim_create_autocmd({'BufEnter', 'TextChanged', 'TextChangedI'}, {
          group = 'KbGroup',
          pattern = config.notes_path .. '*.md',
          command = 'KBHighlightWikiLinks',
     })
     vim.api.nvim_create_autocmd('ColorScheme', {
          pattern = '*',
          group = 'KbGroup',
          command = 'KBHighlightWikiLinks',
     })
end

function M.setup(user_config)
     -- Set default configuration values
     local _config = vim.tbl_extend('force', {
          notes_fzf_options = "--bind='ctrl-e:toggle-preview' --preview 'bat --color=always " .. user_config.notes_path .. "/{}.md'", -- FZF options used search for notes
          notes_path = nil,  -- The path to the directory containing the notes
          note_post_init = nil,  -- User defined function to run after the plugin has been setup. Useful for setting up mappings
     }, user_config or {})

     if _config.notes_path == nil then
          error("The 'notes_path' must be provided in the plugin configuration.")
          return
     end
     config = _config

     vim.g.kb_notes_path = config.notes_path
     vim.g.kb_notes_fzf_options = config.notes_fzf_options

     M.load_kb_settings = load_kb_settings

     vim.api.nvim_create_user_command('LoadKBSettings', 'lua require("kb_notes").load_kb_settings()', { nargs = 0 })

     setupAutocmd()
end

return M