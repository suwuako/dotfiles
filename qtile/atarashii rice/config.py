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
import time
import subprocess
import psutil
from typing import List  # noqa: F401
from libqtile.config import Screen
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from libqtile.widget import Wallpaper

mod = "mod1"
terminal = guess_terminal()

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
    Key([mod], "r", lazy.spawn('rofi -show run -lines 10 -width 30 -font "Roboto Mono Regular 12" -theme "Arc-Dark"'),
        desc="Spawn a command using a prompt widget"),
    
    # Launch applications
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
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
    #shit that might have use in the future
    '''layout.Columns(
        border_focus='#f289ff',
        border_focus_stack='#e5e5e5',
        border_normal='FFFFFF',
        border_normal_stack='#f9c5ff',
        border_width=6, 
        margin=15),'''

border_width = 3
margin = 25
border_focus = '#f289ff'
border_focus_stack='#e5e5e5'
border_normal='FFFFFF'
border_normal_stack='#f9c5ff'

layouts = [
        
    layout.Tile(border_focus=border_focus,
        border_focus_stack=border_focus_stack,
        border_normal=border_normal,
        border_normal_stack=border_normal_stack,
        border_width=border_width, 
        margin=margin),
                
    layout.MonadWide(border_focus=border_focus,
        border_focus_stack=border_focus_stack,
        border_normal=border_normal,
        border_normal_stack=border_normal_stack,
        border_width=border_width,
        margin=margin),

    
    layout.RatioTile(border_focus=border_focus,
        border_focus_stack=border_focus_stack,
        border_normal=border_normal,
        border_normal_stack=border_normal_stack,
        border_width=border_width,
        margin=margin),

     
    layout.TreeTab(
        active_bg=border_focus,
        active_fg='#6e027c',
        bg_color = '#1d0b21',
        border_width = 2,
        font = 'Roboto Mono Regular',
        panel_width = 180,
        sections = ['Primary', 'Secondary', 'Misc'],
        vpsace = 3,
        ),
    
    #layout.Tile(),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    
    # layout.MonadTall(),
    
    
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

colors = {
        'background' : '#1d0b21',
        'foreground' : '#ff8e71',
        'darkbackground' : '#4E2C5D',
        'altdarkbackground' : '#301f7c',
        'darkforeground' : '#75105f',
        'active' : '#ff9b9b',
        'inactive' : '#f6f5f5',
        'pastelYellow' : '#fcf2a9',
        'pastelRed' : '#ff9b9b',
        'pastelBlue' : '#9abeff',
        'pastelGreen' : '#d1ffc2',
        'pastelPurple' : '#f4b7d8',
        'pastelPink' : '#ffe7e7'
        }

fontS = 15

screens = [
    Screen(
        top=bar.Bar(
            
            [
                widget.Sep(
                    linewidth = 6,
                    padding = 6,
                    foreground = colors['background'],
                    background = colors['background']
                    ),
               

                widget.GroupBox(
                    font='Roboto Mono Regular',
                    fontsize = 14, 
                    active = colors['active'],
                    inactive = colors['inactive'],
                    
                    borderwidth = 8,

                    this_current_screen_border = colors['altdarkbackground'],
                    this_screen_border = colors['darkforeground'],
                    other_current_screen_border = colors['darkbackground'],
                    other_screen_border = colors['darkbackground'],
                    highlight_method = 'block',
                    rounded = True,
                    
                    foreground = colors['foreground'],
                    background = colors['background'],
                    
                    ),

                widget.TextBox(
                    text = ' ',
                    background = colors['background']
                    ),

                widget.Prompt(
                    foreground = colors['foreground'],
                    background = colors['background']

                    ),
                widget.WindowName(
                    foreground = colors['pastelPurple'],
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'

                    ),

                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),

                widget.Clock(
                    format = '%I:%M %p',
                    foreground = colors['pastelBlue'],
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),
                        
                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),
                        
                widget.Clock(
                    format = '%D, %A',
                    foreground = colors['pastelBlue'],
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),

                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),

                widget.Memory(
                        foreground = colors['pastelYellow'],
                        background = colors['background'],
                        format = '{MemUsed} MB',
                        fontsize = fontS,
                        font = 'Roboto Mono Regular'
                        ),
            
                
                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),

                widget.CPU(
                        background = colors['background'],
                        fontsize = fontS,
                        font = 'Roboto Mono Regular'
                        ),

                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),


                widget.TextBox(
                        text = 'Volume:',
                        foreground = colors['pastelRed'],
                        background = colors['background'],
                        fontsize = fontS,
                        font = 'Roboto Mono Regular'
                        ),

                widget.Volume(
                       foreground = colors['pastelRed'],
                       background = colors['background'],
                       fontsize = fontS,
                       font = 'Roboto Mono Regular'
                        ),
                
                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),


                widget.Wlan(
                    foreground = colors['pastelGreen'],
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular',
                    
                    ),

                widget.TextBox(
                    text = '|',
                    background = colors['background'],
                    fontsize = fontS,
                    font = 'Roboto Mono Regular'
                    ),

                widget.CurrentLayout(
                        foreground = colors['pastelPurple'],
                        background = colors['background'],
                        fontsize = fontS,
                        font = 'Roboto Mono Regular'
    
                        ),

                widget.Sep(
                    linewidth = 6,
                    padding = 6,
                    foreground = colors['background'],
                    background = colors['background']
                    ), 
            ],
            30,
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
