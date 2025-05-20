local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable", -- latest stable release
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
	{ "ellisonleao/gruvbox.nvim", priority = 1000 , config = true, opts = ...},
	{ "catppuccin/nvim", name = "catppuccin", priority = 1000 },
	{ "folke/neodev.nvim", dependencies = {"neovim/nvim-lspconfig"} , opts={} },
	{ "rcarriga/nvim-dap-ui", dependencies = {"mfussenegger/nvim-dap", "nvim-neotest/nvim-nio", "folke/neodev.nvim"} },
	{ "mfussenegger/nvim-dap-python" },
	{
		"nvim-tree/nvim-tree.lua",
		version = "*",
		lazy = false,
		dependencies = {"nvim-tree/nvim-web-devicons",},
		config = function()
		require("nvim-tree").setup {}
		end,
	},
	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {
			-- your configuration comes here
			-- or leave it empty to use the default settings
			-- refer to the configuration section below
		},
		keys = {
			{
				"<leader>?",
				function()
					require("which-key").show({ global = false })
				end,
				desc = "Buffer Local Keymaps (which-key)",
			},
		},
	},
	{
		'dense-analysis/ale',
		config = function()
			-- Configuration goes here.
			local g = vim.g

			g.ale_ruby_rubocop_auto_correct_all = 1

			g.ale_linters = {
				c = {'clang'},
				cpp = {'g++', 'clang'},
				python = {'flake8'},
				ruby = {'rubocop', 'ruby'},
				lua = {'lua_language_server'}
			}
		end
	},
	{
	  "ibhagwan/fzf-lua",
	  -- optional for icon support
	  dependencies = { "nvim-tree/nvim-web-devicons" },
	  -- or if using mini.icons/mini.nvim
	  -- dependencies = { "echasnovski/mini.icons" },
	  opts = {}
	},
})

require("mycolorscheme")
require("setups/nvim-tree")
require("setups/neodev")
require("setups/dap")
require("setups/which-key")


vim.cmd.source("$HOME/.config/nvim/nvimrc.vim")
