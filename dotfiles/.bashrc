# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
alias atcl='paru -Scc; paru -Rs $(pacman -Qdtq)'
alias vi='nvim'
alias neofetch='fastfetch'
alias pacinstall='sudo pacman -S --needed'
alias pacuninstall='sudo pacman -Rsnu'
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias activate='source $HOME/.venv/bin/activate'
alias nnn='tmux new-session nnn -a'
export NNN_OPENER="${XDG_CONFIG_HOME}/nnn/plugins/nuke"
export NNN_PLUG='f:finder;z:fzcd;o:fzopen;p:preview-tui;d:diffs;t:nmount;v:imgview'
export BAT_THEME='gruvbox-dark'
eval "$(fzf --bash)"

# Created by `pipx` on 2024-08-03 23:44:17
export PATH="$PATH:/home/jkwon/.local/bin"
