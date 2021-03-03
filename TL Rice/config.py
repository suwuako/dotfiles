# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import psutil
from typing import List  # noqa: F401
from libqtile.config import Screen
from libqtile import hook
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod1"
terminal = guess_terminal()

#colors
lightBlue = '#90d4ed'
lightOrange = '#f4cd9a'

normalBlue = '#0453db'
normalOrange = '#c65600'

pastelBlurple = '#a697ed'
pastelOrange = '#ffcc33'
pastelYellow = '#ffff99'
pastelBlue = '#AEC6CF'

darkOrange = '#ff8c00'
darkBlue = '#00008B'

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
   
    # Launch applications
    Key([mod], "r", lazy.spawn('rofi -show run -font "Roboto Mono Regular 12" -lines 10 -width 25 -theme DarkBlue'),
        desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "s", lazy.spawn('flameshot gui'), desc='open screenshot launcher'),


]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

margin = 20
border_width = 7

layouts = [

    layout.Tile(
        margin = margin, 
        border_width = border_width,
        border_focus = lightBlue,
        border_normal = lightOrange,
        name = 'Main/Slaves - Tile'
        ),

    layout.TreeTab(
        sections = ['Primary','Secondary','Tertiary'],
        active_bg = lightBlue,
        active_fg = normalBlue,
        bg_color = pastelBlurple,
        inactive_bg = lightOrange,
        inactive_fg = normalOrange, 

        font = 'Roboto Mono',
        panel_width = 180,
        section_fontsize = 12,

        name = 'Stack - TreeTab'
        ),

    layout.RatioTile(
        margin = margin,
         border_width = border_width,
         border_focus = lightBlue,
         border_normal = lightOrange,
         
         fancy = True,
         name = 'FlexTile - RatioTile'

        ),
    #layout.Columns(border_focus_stack='#d75f5f'),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Roboto Mono',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

background = '#8b8dfa'
font = 'Roboto Mono'



widgets = [
widget.Sep(
    background = background,
    foreground = background,
    linewidth = 5,
    size_percent = 100

    ),
widget.GroupBox(
    background = background,
    active = darkBlue,
    inactive = '#4d4c66',

    font = 'Roboto Mono',
    fontsize = 16,
    borderwidth = 5,
    padding = 5,
    margin = 5,

    highlight_method = 'block',
    this_screen_border = '#05ffb7',
    this_current_screen_border = '#b6ffea',
    other_screen_border = pastelYellow,
    other_current_screen_border = pastelYellow
    ),

widget.Prompt(),
widget.WindowName(
    background = background,
    foreground = '#9cf196',
    for_current_screen = True,
    fontsize = 14,
    max_chats = 10,
    padding = 5,
    font = font,


    ),

widget.TextBox(
    background = background,
    font = font,
    text = '|',
    fontsize = 20

    ),

widget.Clock(
    background = background,
    foreground = '#fce2ae', 
    format= '%I:%M %p',
    fontsize = 15 
    ),

widget.TextBox(
     background = background,
     font = font,
     text = '|',
     fontsize = 20
 
     ),

widget.Memory(
        background = background,
        font=font,
        fontsize = 15,
        foreground = '#b6ffea'
        ),

widget.TextBox(
    background = background,
    font = font,
    text = '|',
    fontsize = 20

    ),


widget.CurrentLayout(
    background = background,
    font = font,
    fontsize = 15,
    foreground = '#ffb3b3'
    )
        ]


screens = [
    Screen(
        top=bar.Bar(
            widgets,
            
            37,
            
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
