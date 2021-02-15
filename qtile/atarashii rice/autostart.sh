#!/bin/sh
feh --bg-scale /usr/share/backgrounds/Atarashii.jpg &
vim ~/.config/qtile/config.py &
compton &
xrandr --output DVI-D-0 --off --output HDMI-0 --off --output DP-0 --mode 2560x1440 --pos 0x0 --rotate normal --output DP-1 --off --output DP-2 --off --output DP-3 --off --output USB-C-0 --off --output DP-1-1 --off --output HDMI-1-1 --mode 1920x1080 --pos 2560x360 --rotate normal &
