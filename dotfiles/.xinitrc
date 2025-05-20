export GTK_IM_MODULE="fcitx"
export QT_IM_MODULE="fcitx"
export XMODIFIERS="@im=fcitx"
export INPUT_METHOD="fcitx"
export XIM="fcitx"
export XIM_PROGRAM="fcitx"
export SDL_IM_MODULE="fcitx"
export GLFW_IM_MODULE="ibus"

[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

slstatus & fcitx5 & nm-applet & dunst & conky & blueman-applet &
conky -c $HOME/.config/conky/conky-note.conf
exec ~/.scripts/X11/restartdwm
