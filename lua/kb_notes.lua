local M = {}
local config = {}

--- utils
local function split(str, sep)
    local result = {}
    local regex = ("([^%s]+)"):format(sep)
    for each in str:gmatch(regex) do
        table.insert(result, each)
    end
    return result
end

local function notify(text)
  require("notify")(text, 2, {render = 'minimal'})
end

function escape_pattern(text)
    return text:gsub("([^%w])", "%%%1")
end

local function get_parent_notes(note_name)
    -- note_name is a string like a.b.c
    -- return list with [a, a.b], not including current note
    -- if note_name is a, return empty list
    local parent_notes = {}
    local note_parts = split(note_name, ".")
    if #note_parts == 1 then
      return parent_notes
    end

    for i = 1, #note_parts - 1 do
      local parent_note = table.concat(note_parts, ".", 1, i)
      table.insert(parent_notes, parent_note)
    end
    return parent_notes
end

local function cursor_on_markdown_link()
    local current_line = line or vim.api.nvim_get_current_line()
    local _, cur_col = unpack(vim.api.nvim_win_get_cursor(0))
    cur_col = col or cur_col + 1 -- nvim_win_get_cursor returns 0-indexed column

    local find_boundaries = function(pattern)
        local open, close = current_line:find(pattern)
        while open ~= nil and close ~= nil do
          if open <= cur_col and cur_col <= close then
            return open, close
          end
          open, close = current_line:find(pattern, close + 1)
        end
    end

    local open, close = find_boundaries("%[%[.-%]%]")

    return open, close
end

local function get_all_notes()
    -- return list with all notes in notes_path
    -- without extension but file should be markdown
    local res = vim.fn.system("ls -t " .. config.notes_path)
    local notes = {}
    for line in string.gmatch(res, "[^\r\n]+") do
        if string.match(line, "%.md$") then
            local note = string.match(line, "^(.+)%..+$")
            table.insert(notes, note)
        end
    end
    return notes
end

local function find_children(note_name)
    -- return list with all children of note_name
    -- for examole programming.python will return all notes with name programming.python.*
    local notes = get_all_notes()
    local children = {}
    for _, note in ipairs(notes) do
        if string.match(note, "^" .. note_name .. "%..+$") then
            table.insert(children, note)
        end
    end
    return children
end

local function create_note(note_path)
    -- TODO: add template to config
    local template = "# {note_name}\n\n## References\n\n## Links\n\n## Notes\n\n"

    -- filename is full path to file but need only filename without extension
    local note_name = string.match(note_path, "^.+/(.+)%..+$")

    local note_file = io.open(note_path, "w")
    local content = string.gsub(template, "{note_name}", note_name)
    note_file:write(content)
    note_file:close()
end

local function get_date_from_filename(filename)
  local date_string = string.match(filename, "%d%d%d%d%.[%d]+%.[%d]+")
  return date_string
end

local function slugify(text)
    text = string.lower(text)
    text = string.gsub(text, " ", "-")
    text = string.gsub(text, "[^a-zA-Z0-9-.]", "-")
    return text
end

local function rename_process_note(old_note_name, new_note_name)
    local function update_links(old_note_name, new_note_name)
        local notes = get_all_notes()
        for _, note in ipairs(notes) do
            local note_path = config.notes_path .. "/" .. note .. ".md"
            local note_file = io.open(note_path, "r")
            local content = note_file:read("*a")
            note_file:close()

            local new_content = string.gsub(content, "%[%[" .. old_note_name .. "%]%]", "[[" .. new_note_name .. "]]")
            if new_content ~= content then
                note_file = io.open(note_path, "w")
                note_file:write(new_content)
                note_file:close()
            end
        end
    end

    local function update_title(old_note_name, new_note_name)
        local note_path = config.notes_path .. "/" .. new_note_name .. ".md"
        local note_file = io.open(note_path, "r")
        local content = note_file:read("*a")
        note_file:close()

        local new_content = string.gsub(content, escape_pattern("# " .. old_note_name), "# " .. new_note_name)
        if new_content ~= content then
            note_file = io.open(note_path, "w")
            note_file:write(new_content)
            note_file:close()
        end
    end

    local function move_note(old_note_name, new_note_name)
        local old_note_path = config.notes_path .. "/" .. old_note_name .. ".md"
        local new_note_path = config.notes_path .. "/" .. new_note_name .. ".md"

        os.rename(old_note_path, new_note_path)
    end

    local children_note = find_children(old_note_name)
    table.insert(children_note, old_note_name)

    local new_children_note = {}
    for _, note in ipairs(children_note) do
        local new_note = string.gsub(note, escape_pattern(old_note_name), new_note_name)
        table.insert(new_children_note, new_note)
    end

    local existing_files = {}
    for _, note in ipairs(new_children_note) do
        local note_path = config.notes_path .. "/" .. note .. ".md"
        if vim.fn.filereadable(note_path) == 1 then
            table.insert(existing_files, note)
        end
    end

    if #existing_files > 0 then
        return false, existing_files, {}
    end

    local processed = {}
    for i, note in ipairs(children_note) do
        local old_note_name = note
        local new_note_name = new_children_note[i]

        update_links(old_note_name, new_note_name)
        move_note(old_note_name, new_note_name)
        update_title(old_note_name, new_note_name)
        table.insert(processed, {old_note_name = old_note_name, new_note_name = new_note_name})
    end

    return true, {}, processed
end

--- commands
local function command_create_note()
    local note_name = vim.fn.input("Enter note name: ")
    local note_name_normalized = slugify(note_name)

    local not_existing_parents = get_parent_notes(note_name_normalized)
    if #not_existing_parents > 0 then
        local confirmed = vim.fn.confirm("Notes: [" .. table.concat(not_existing_parents, ", ") .. "] do not exist", "&Yes\n&No", 2)
        if confirmed ~= 1 then
            return
        end
    end

    local note_path = config.notes_path .. "/" .. note_name_normalized .. ".md"
    if vim.fn.filereadable(note_path) == 0 then
      create_note(note_path)
    end

    vim.cmd("edit " .. note_path)
end



local function command_note_rename()
    local current_note = vim.fn.expand("%:t:r")
    local new_note_name = vim.fn.input("Enter note name: ", current_note)
    local new_note_name_normalized = slugify(new_note_name)

    if current_note == new_note_name_normalized then
        notify("Same name")
        return
    end
    if #new_note_name_normalized == 0 then
        notify("Empty name")
        return
    end

    local parents = get_parent_notes(new_note_name_normalized)
    local not_existing_parents = {}
    for _, parent in ipairs(parents) do
        local note_path = config.notes_path .. "/" .. parent .. ".md"
        if vim.fn.filereadable(note_path) == 0 then
            table.insert(not_existing_parents, parent)
        end
    end
    if #not_existing_parents > 0 then
        local confirmed = vim.fn.confirm("Notes: [" .. table.concat(not_existing_parents, ", ") .. "] do not exist", "&Yes\n&No", 2)
        if confirmed ~= 1 then
            return
        end
    end

    -- save current buffer
    vim.cmd("w")

    local success, existing_files, renamed = rename_process_note(current_note, new_note_name_normalized)

    if #existing_files > 0 then
        notify("Notes: [" .. table.concat(existing_files, ", ") .. "] already exist")
        return
    end

    vim.cmd("e " .. config.notes_path .. "/" .. new_note_name_normalized .. ".md")

    -- close all buffers but not current one
    vim.cmd("w | %bd | e#")

    for _, note in ipairs(renamed) do
        notify("Note " .. note.old_note_name .. " renamed to " .. note.new_note_name)
    end
end


local function command_open_daily_note()
  local current_date = os.date("%Y.%m.%d")
  local file_path = config.notes_path .. "/notes.journaling." .. current_date .. ".md"

  -- Open the daily note file
  vim.cmd("edit " .. vim.fn.fnameescape(file_path))

  local current_title = vim.fn.getline(1)
  local expected_title = "# " .. vim.fn.expand("%:r")

  if current_title == "" then
    vim.fn.setline(1, expected_title)
    vim.fn.setline(2, "")
    vim.fn.setline(3, "## Вдячність [[life.happiness.gratitude.log]]")
    vim.fn.setline(4, "")
    vim.fn.setline(5, "- ")
    vim.fn.setline(6, "- ")
    vim.fn.setline(7, "- ")
    vim.fn.setline(8, "")
    vim.fn.setline(9, "## День")
    vim.fn.setline(10, "")
  end

  vim.cmd("normal! G")
end

-- Updates header in file if it matches with filename
local function command_update_note_header()
  local current_title = vim.fn.getline(1)
  local expected_title = "# " .. vim.fn.expand("%:r")
  if current_title ~= expected_title and string.match(current_title, "^# ") then
    vim.fn.setline(1, expected_title)
  end
end

-- Paste img from clipboard copied as path
local function command_paste_img()
  local script_path = vim.fn.expand("~/.dotfiles/bin/_command_paste_img")
  local command = "python3 " .. script_path

  -- Execute the command and capture the output and error messages
  local output = vim.fn.system(command .. " 2>&1")

  -- Check if the command was successful
  if vim.v.shell_error == 0 then
    -- Remove trailing newline character from the output
    local image_file = string.gsub(output, "\n", "")

    -- Check if the output is not empty
    if image_file ~= "" then
      -- Create the Markdown image link
      local image_link = "![](" .. image_file .. ")"

      -- Insert the Markdown image link at the current cursor position
      vim.cmd("normal! a" .. image_link)
    else
      notify("Failed to paste image.")
    end
  else
    -- Print the error message from stderr
    notify("Failed to paste image: " .. output)
  end
end

-- Next/Prev daily note
local function command_next_day()
  local current_buffer = vim.fn.bufname()
  local current_date = get_date_from_filename(current_buffer)

  if current_date then
    local year, month, day = current_date:match("(%d%d%d%d)%.(%d%d)%.(%d%d)")
    local next_day = os.time({year = tonumber(year), month = tonumber(month), day = tonumber(day)}) + 86400 -- Add one day (86400 seconds)
    local next_date = os.date("%Y.%m.%d", next_day)
    local next_file = string.gsub(current_buffer, current_date, next_date)
    if vim.fn.filereadable(next_file) == 1 then
      vim.cmd("edit " .. next_file)
    else
      notify("File does not exist: " .. next_file)
    end
  else
    command_open_daily_note()
  end
end

local function command_prev_day()
  local current_buffer = vim.fn.bufname()
  local current_date = get_date_from_filename(current_buffer)

  if current_date then
    local year, month, day = current_date:match("(%d%d%d%d)%.(%d%d)%.(%d%d)")
    local prev_day = os.time({year = tonumber(year), month = tonumber(month), day = tonumber(day)}) - 86400 -- Subtract one day (86400 seconds)
    local prev_date = os.date("%Y.%m.%d", prev_day)
    local prev_file = string.gsub(current_buffer, current_date, prev_date)
    if vim.fn.filereadable(prev_file) == 1 then
      vim.cmd("edit " .. prev_file)
    else
      notify("File does not exist: " .. prev_file)
    end
  else
    command_open_daily_note()
  end
end

local function command_spell_suggest()
  require('fzf-lua').spell_suggest()
end

local function command_show_backlinks()
  local current_note = vim.fn.expand('%:t:r')
  require('fzf-lua').grep({search = '[['.. current_note .. ']]'}, {})
end

local function command_open_map()
  local filepath = vim.fn.expand('%:p')
  io.popen('markmap ' .. filepath .. ' -o /tmp/map.html')
end

local function command_go_to_parent_note()
    local current_note = vim.fn.expand("%:t:r")
    local current_file_path = vim.fn.expand("%:p:h")
    local current_file_extension = vim.fn.expand("%:e")

    if current_file_extension ~= "md" then
      KBNotify("Not a markdown file")
      return
    end

    local parent_notes = get_parent_notes(current_note)
    if #parent_notes == 0 then
      notify("Current note is the root")
      return
    end

    local parent_note_path = current_file_path .. "/" .. parent_notes[#parent_notes] .. ".md"
    if vim.fn.filereadable(parent_note_path) == 0 then
      create_note(parent_note_path)
    end

    vim.cmd("edit " .. parent_note_path)
end


local function command_open_link()
    local open, close = cursor_on_markdown_link() -- get cursor position
    local current_line = vim.api.nvim_get_current_line()

    if open == nil or close == nil then
        require('follow-md-links').follow_link()
        return
    end

    local note_name = current_line:sub(open, close)
    note_name = note_name:sub(3, -3) -- remove [[ and ]]

    local note_path = config.notes_path .. "/" .. note_name .. ".md"

    if vim.fn.filereadable(note_path) == 0 then
        create_note(note_path)
    end

    vim.cmd("edit " .. note_path)
end

local function command_link_suggestion()
    require('fzf-lua').fzf_exec(
        get_all_notes(),
        {
            previewer = false,
            preview = require'fzf-lua'.shell.raw_preview_action_cmd(function(items)
                return "bat --color=always " .. config.notes_path .. "/" .. items[1] .. ".md"
            end),
            actions = {
                ["default"] = function(selected)
                    local note_name = selected[1]
                    local open, close = cursor_on_markdown_link() -- get cursor position

                    if open == nil or close == nil then
                        -- insert new link
                        vim.api.nvim_feedkeys('i[[' .. note_name .. ']]', "n", true)
                        vim.cmd("stopinsert")
                        return
                    end

                    local char_under_cursor = function()
                        return vim.api.nvim_eval("getline('.')[col('.')-1]")
                    end
                    local char_after_cursor = function()
                        return vim.api.nvim_eval("getline('.')[col('.')]")
                    end

                    if char_under_cursor() == "[" and char_after_cursor() == "[" then
                        -- if fist bracket
                        vim.api.nvim_feedkeys("f[", "n", true)
                    end
                    if char_under_cursor() == "]" then
                        -- if second bracket
                        vim.api.nvim_feedkeys("F[", "n", true)
                    end
                    vim.api.nvim_feedkeys('"_ci[' .. note_name, "n", true)
                    vim.cmd("stopinsert")
                end
            }
        }
    )


end

local function command_random_note()
    -- Open a random note
    local notes = get_all_notes()
    local random_note = notes[math.random(#notes)]
    local note_path = config.notes_path .. "/" .. random_note .. ".md"

    vim.cmd("edit " .. note_path)
end

local function command_search_notes()
    require('fzf-lua').fzf_exec(
        get_all_notes(),
        {
            previewer = false,
            preview = require'fzf-lua'.shell.raw_preview_action_cmd(function(items)
                return "bat --color=always " .. config.notes_path .. "/" .. items[1] .. ".md"
            end),
            actions = {
                ["default"] = function(selected)
                    vim.cmd("edit " .. config.notes_path .. '/' .. selected[1] .. ".md")
                end
            },
        }
    )
end

local function command_search_notes_with_prefix()
    local current_note = vim.fn.expand("%:t:r")

    require('fzf-lua').fzf_exec(
        get_all_notes(),
        {
            previewer = false,
            preview = require'fzf-lua'.shell.raw_preview_action_cmd(function(items)
                return "bat --color=always " .. config.notes_path .. "/" .. items[1] .. ".md"
            end),
            actions = {
                ["default"] = function(selected)
                    vim.cmd("edit " .. config.notes_path .. '/' .. selected[1] .. ".md")
                end
            },
            fzf_opts = {
                ["--query"] = current_note,
            },
        }
    )
end


--- extras
local function load_kb_settings()
     -- OpenLink uses this command
     --vim.cmd([[syntax match wikiLink /\[\[.\{-}\]\]/ containedin=mkdNonListItemBlock,mkdListItemLine,htmlH1,htmlH2,htmlH3,htmlH4,htmlH5,htmlH6]])

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

     M.command_open_daily_note = command_open_daily_note
     M.command_update_note_header = command_update_note_header
     M.command_paste_img = command_paste_img
     M.command_next_day = command_next_day
     M.command_prev_day = command_prev_day
     M.command_spell_suggest = command_spell_suggest
     M.command_show_backlinks = command_show_backlinks
     M.command_open_map = command_open_map
     M.command_go_to_parent_note = command_go_to_parent_note
     M.command_open_link = command_open_link
     M.command_random_note = command_random_note
     M.command_search_notes = command_search_notes
     M.command_search_notes_with_prefix = command_search_notes_with_prefix
     M.command_link_suggestion = command_link_suggestion
     M.command_create_note = command_create_note
     M.command_note_rename = command_note_rename

     vim.api.nvim_create_user_command('LoadKBSettings', 'lua require("kb_notes").load_kb_settings()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBOpenDailyNote', 'lua require("kb_notes").command_open_daily_note()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBUpdateNoteHeader', 'lua require("kb_notes").command_update_note_header()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBPasteImg', 'lua require("kb_notes").command_paste_img()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBNextDay', 'lua require("kb_notes").command_next_day()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBPrevDay', 'lua require("kb_notes").command_prev_day()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBSpellSuggest', 'lua require("kb_notes").command_spell_suggest()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBShowBacklinks', 'lua require("kb_notes").command_show_backlinks()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBOpenMap', 'lua require("kb_notes").command_open_map()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBGoToParentNote', 'lua require("kb_notes").command_go_to_parent_note()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBOpenLink', 'lua require("kb_notes").command_open_link()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBRandomNote', 'lua require("kb_notes").command_random_note()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBSearchNote', 'lua require("kb_notes").command_search_notes()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBSearchNoteWithPrefix', 'lua require("kb_notes").command_search_notes_with_prefix()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBLinkSuggestion', 'lua require("kb_notes").command_link_suggestion()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBNewNote', 'lua require("kb_notes").command_create_note()', { nargs = 0 })
     vim.api.nvim_create_user_command('KBRenameNote', 'lua require("kb_notes").command_note_rename()', { nargs = 0 })

     setupAutocmd()
end

return M
