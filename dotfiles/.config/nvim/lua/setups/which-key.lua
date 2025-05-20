local wk = require("which-key")
wk.add({
	{ "<leader>d", group = "debug" }, -- group
	{ "<leader>dd", "<cmd>lua require('dapui').toggle()<cr>", desc = "Display debug UI", mode = "n" },
	{ "<leader>db", "<cmd>lua require('dap').toggle_breakpoint()<cr>", desc = "Toggle breakpoint", mode="n" },
	{ "<leader>d1", "<cmd>lua require('dap').continue()<cr>", desc = "Continue", mode="n" },
	{ "<leader>d2", "<cmd>lua require('dap').disconnect({ terminateDebuggee = true})<cr><cmd>lua require('dap').close()<cr>", desc = "Disconnect", mode="n" },
	{ "<leader>t", "<cmd>NvimTreeToggle<cr>", desc = "Toggle nvim-tree" },
	{ "<leader>f", "<cmd>lua require('fzf-lua').files()<cr>", desc = "Open fzf"}
})
