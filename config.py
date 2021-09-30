import os
import socket
import subprocess
from datetime import datetime
from random import randrange

from libqtile import layout, bar, hook
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.widget.clock import Clock
from libqtile.widget.currentlayout import CurrentLayout
from libqtile.widget.graph import CPUGraph
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.net import Net
from libqtile.widget.prompt import Prompt
from libqtile.widget.sep import Sep
from libqtile.widget.spacer import Spacer
from libqtile.widget.systray import Systray
from libqtile.widget.textbox import TextBox
from libqtile.widget.windowname import WindowName

from headset_battery import HeadsetBattery
from radio import Radio
from task_log import TaskLog

# mod4 or mod = super key1
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [

    # FUNCTION KEYS

    Key([], "F12", lazy.spawn('xfce4-terminal --drop-down')),

    # SUPER + FUNCTION KEYS

    # Key([mod], "e", lazy.spawn('atom')),
    Key([mod], "c", lazy.spawn('conky-toggle')),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawn('rofi-theme-selector')),
    Key([mod], "t", lazy.spawn('urxvt')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "x", lazy.spawn('arcolinux-logout')),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn('xfce4-terminal')),
    Key([mod], "KP_Enter", lazy.spawn('xfce4-terminal')),
    # Key([mod], "F1", lazy.spawn('vivaldi-stable')),
    # Key([mod], "F2", lazy.spawn('atom')),
    # Key([mod], "F3", lazy.spawn('inkscape')),
    # Key([mod], "F4", lazy.spawn('gimp')),
    # Key([mod], "F5", lazy.spawn('meld')),
    # Key([mod], "F6", lazy.spawn('vlc --video-on-top')),
    # Key([mod], "F7", lazy.spawn('virtualbox')),
    # Key([mod], "F8", lazy.spawn('thunar')),
    # Key([mod], "F9", lazy.spawn('evolution')),
    Key([mod], "F10", lazy.spawn("rofi -show ssh")),
    Key([mod], "F11", lazy.spawn('rofi -show')),
    Key([mod], "F12", lazy.spawn('rofi -show run')),

    # SUPER + SHIFT KEYS

    Key([mod, "shift"], "Return", lazy.spawn('thunar')),
    # Key([mod, "shift"], "d", lazy.spawn(
    #    "dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=18'")),
    # Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    # Key([mod, "shift"], "x", lazy.shutdown()),

    # CONTROL + ALT KEYS

    Key(["mod1", "control"], "Next", lazy.spawn('conky-rotate -n')),
    Key(["mod1", "control"], "Prior", lazy.spawn('conky-rotate -p')),
    # Key(["mod1", "control"], "a", lazy.spawn('xfce4-appfinder')),
    Key(["mod1", "control"], "b", lazy.spawn('thunar')),
    # Key(["mod1", "control"], "c", lazy.spawn('catfish')),
    # Key(["mod1", "control"], "e", lazy.spawn('evolution')),
    Key(["mod1", "control"], "f", lazy.spawn('firefox')),
    # Key(["mod1", "control"], "g", lazy.spawn('chromium -no-default-browser-check')),
    Key(["mod1", "control"], "i", lazy.spawn('nitrogen')),
    # Key(["mod1", "control"], "k", lazy.spawn('slimlock')),
    Key(["mod1", "control"], "m", lazy.spawn('xfce4-settings-manager')),
    Key(["mod1", "control"], "o", lazy.spawn(home + '/.config/qtile/scripts/compton-toggle.sh')),
    Key(["mod1", "control"], "p", lazy.spawn('pamac-manager')),
    Key(["mod1", "control"], "r", lazy.spawn('rofi-theme-selector')),
    # Key(["mod1", "control"], "s", lazy.spawn('spotify')),
    Key(["mod1", "control"], "t", lazy.spawn('termite')),
    Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),
    Key(["mod1", "control"], "v", lazy.spawn('vivaldi-stable')),
    Key(["mod1", "control"], "w", lazy.spawn('atom')),
    Key(["mod1", "control"], "Return", lazy.spawn('termite')),

    # ALT + ... KEYS

    Key(["mod1"], "k", lazy.spawn('slimlock')),
    Key(["mod1"], "f", lazy.spawn('variety -f')),
    # Key(["mod1"], "h", lazy.spawn('urxvt -e htop')),
    Key(["mod1"], "n", lazy.spawn('variety -n')),
    Key(["mod1"], "p", lazy.spawn('variety -p')),
    Key(["mod1"], "t", lazy.spawn('variety -t')),
    Key(["mod1"], "Up", lazy.spawn('variety --pause')),
    Key(["mod1"], "Down", lazy.spawn('variety --resume')),
    Key(["mod1"], "Left", lazy.spawn('variety -p')),
    Key(["mod1"], "Right", lazy.spawn('variety -n')),
    # Key(["mod1"], "F2", lazy.spawn('gmrun')),
    # Key(["mod1"], "F3", lazy.spawn('xfce4-appfinder')),

    # VARIETY KEYS WITH PYWAL

    Key(["mod1", "shift"], "f", lazy.spawn(home + '/.config/qtile/scripts/set-pywal.sh -f')),
    Key(["mod1", "shift"], "p", lazy.spawn(home + '/.config/qtile/scripts/set-pywal.sh -p')),
    Key(["mod1", "shift"], "n", lazy.spawn(home + '/.config/qtile/scripts/set-pywal.sh -n')),
    Key(["mod1", "shift"], "u", lazy.spawn(home + '/.config/qtile/scripts/set-pywal.sh -u')),

    # CONTROL + SHIFT KEYS

    Key([mod2, "shift"], "Escape", lazy.spawn('xfce4-taskmanager')),

    # SCREENSHOTS

    Key([], "Print", lazy.spawn('flameshot gui')),
    # Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

    # MULTIMEDIA KEYS

    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], 'm', lazy.layout.maximize()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up(), lazy.layout.maximize()),
    Key([mod], "Down", lazy.layout.down(), lazy.layout.maximize()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "mod1"], "space", lazy.window.toggle_floating()), ]

# GROUPS
groups = []

dict_groups = {
    "1": {'label': '',
          'matches': [Match(wm_class='Brave'), Match(wm_class='Brave-browser'), Match(wm_class='brave-browser')],
          'layout': "侀 Tile"},

    "2": {'label': '{}', 'matches': [Match(wm_class='et'), Match(wm_class='Et')], 'layout': "侀 Tile"},

    "3": {'label': '', 'matches': [Match(wm_class='jetbrains-pycharm')], 'layout': " Tree"},

    "4": {'label': '',
          'matches': [Match(wm_class='robo3t'), Match(wm_class='vstudio'), Match(wm_class='Valentina Studio')],
          'layout': " Tree"},
    "5": {'label': '', 'matches': [], 'layout': "侀 Tile"},

    "6": {'label': '',
          'matches': [Match(wm_class='Vlc'), Match(wm_class='vlc'),
                      Match(wm_class='Mpv'), Match(wm_class='mpv'), Match(wm_class='zoom'), Match(wm_class='Zoom')],
          'layout': "侀 Tile"},
    "7": {'label': '', 'matches': [], 'layout': "侀 Tile"},

    "8": {'label': '', 'matches': [], 'layout': "侀 Tile"},

    "9": {'label': '',
          'matches': [Match(wm_class='whatsapp-nativefier-d40211'), Match(wm_class='Discord'), Match(wm_class='Slack'),
                      Match(wm_class='slack'), Match(wm_class='microsoft teams - preview'),
                      Match(wm_class='Microsoft Teams - Preview')
                      ],
          'layout': " Tree"},
    "0": {'label': '', 'matches': [], 'layout': " Tree"},

    "XF86Calculator": {'label': '', 'matches': [], 'layout': "侀 Tile"},

    "XF86HomePage": {'label': '',
                     'matches': [Match(wm_class='org.remmina.Remmina'), Match(wm_class='VirtualBox Manager'),
                                 Match(wm_class='VirtualBox Machine'), Match(wm_class='Vmplayer'),
                                 Match(wm_class='virtualbox manager'), Match(wm_class='virtualbox machine'),
                                 Match(wm_class='vmplayer')
                                 ],
                     'layout': " Max"},

    "XF86AudioMute": {'label': '', 'matches': [], 'layout': "侀 Tile"},
}

for k, i in dict_groups.items():
    if 'name' not in i.keys():
        i['name'] = k
    groups.append(Group(**i))

for i in groups:
    keys.extend([
        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "mod1"], "Right", lazy.screen.next_group()),
        Key([mod, "mod1"], "Left", lazy.screen.prev_group()),
        Key([mod], "Tab", lazy.screen.toggle_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),
    ])

layouts = [
    layout.Tile(border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name="侀 Tile"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name="⬓ Wide"),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    #  layout.Floating(margin=5, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Float"),
    layout.RatioTile(margin=5, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name="全 Bsp"),
    layout.Zoomy(name=" Zoomy", columnwidth=600),
    layout.TreeTab(name=" Tree"),
    #    layout.Slice(**layout_theme),
    layout.Max(margin=5, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Max"),
    # layout.VerticalTile(border_focus="#5e81ac", border_normal="#4c566a", name="VT"),
]


# COLORS FOR THE BAR

def init_colors():
    return [["#2F343F", "#2F343F"],  # color 0
            ["#2F343F", "#2F343F"],  # color 1
            ["#c0c5ce", "#c0c5ce"],  # color 2
            ["#fba922", "#fba922"],  # color 3
            ["#3384d0", "#3384d0"],  # color 4
            ["#f3f4f5", "#f3f4f5"],  # color 5
            ["#cd1f3f", "#cd1f3f"],  # color 6
            ["#62FF00", "#62FF00"],  # color 7
            ["#6790eb", "#6790eb"],  # color 8
            ["#a9a9a9", "#a9a9a9"]]  # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize=12,
                padding=2,
                background=colors[1])


widget_defaults = init_widgets_defaults()

random_bar = lambda: "▁▂▃▄▅▆▇█"[randrange(0, 8)]


def status_getter(p: int):
    if p >= 90:
        return ':'
    elif p >= 70:
        return ':'
    elif p >= 40:
        return ':'
    elif p >= 20:
        return ':'
    else:
        return ':'


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        GroupBox(font="FontAwesome",
                 fontsize=16,
                 margin_y=-1,
                 margin_x=0,
                 padding_y=6,
                 padding_x=5,
                 borderwidth=0,
                 disable_drag=True,
                 active=colors[5],
                 inactive=colors[9],
                 rounded=False,
                 highlight_method="text",
                 this_current_screen_border=colors[8],
                 foreground=colors[2],
                 background=colors[1]
                 ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        CurrentLayout(
            font="MesloLGS NF Bold",
            foreground=colors[5],
            background=colors[1]
        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        WindowName(font="Noto Sans",
                   fontsize=12,
                   foreground=colors[5],
                   background=colors[1],
                   ),
        Prompt(name="my_prompt"),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        HeadsetBattery(font="MesloLGS NF",
                       charging_charts=[':'],
                       battery_level_format=lambda x: f':{x}%',
                       # battery_level_format=status_getter,
                       disconnected_chart=''),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        Radio(playlist={"R Nacional": "http://198.15.107.53:8090/;"},
              playing_spinner=[random_bar() + random_bar() + random_bar() + random_bar() for e in range(10)],
              font="MesloLGS NF",
              mute_string="婢",
              stopped_spinner=[""]),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        TaskLog(
            line_saved="\nFecha: {date}     min: {time}     Tarea: {task}",
            prompt_name="my_prompt",
            file_path="~/tiempos.log",
            format="min: {time}",
            get_time=lambda start_date: round((datetime.now() - start_date).seconds / 60, 1)
        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        Net(
            font="MesloLGS NF Blond",
            fontsize=12,
            # interface=["enp24s0", "wlp26s0"],
            foreground=colors[2],
            background=colors[1],
            padding=0,
            format="{down}  {up}"
        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        # NetGraph(
        #          font="Noto Sans",
        #          fontsize=12,
        #          bandwidth="down",
        #          interface="auto",
        #          fill_color = colors[8],
        #          foreground=colors[2],
        #          background=colors[1],
        #          graph_color = colors[8],
        #          border_color = colors[2],
        #          padding = 0,
        #          border_width = 1,
        #          line_width = 1,
        #          ),
        # Sep(
        #          linewidth = 1,
        #          padding = 10,
        #          foreground = colors[2],
        #          background = colors[1]
        #          ),
        TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[6],
            background=colors[1],
            padding=0,
            fontsize=16
        ),
        CPUGraph(
            border_color=colors[2],
            fill_color=colors[8],
            graph_color=colors[8],
            background=colors[1],
            border_width=1,
            line_width=1,
            core="all",
            type="box"
        ),
        # do not activate in Virtualbox - will break qtile
        # ThermalSensor(
        #                        foreground = colors[5],
        #                        foreground_alert = colors[6],
        #                        background = colors[1],
        #                        metric = True,
        #                        padding = 3,
        #                        threshold = 80
        #                        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[4],
            background=colors[1],
            padding=0,
            fontsize=16
        ),
        Memory(
            font="FontAwesome",
            foreground=colors[2],
            background=colors[1],
            padding=0,
            fontsize=12,
            format="{MemUsed: .0f}/{MemTotal: .0f}"
        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[3],
            background=colors[1],
            padding=0,
            fontsize=16
        ),
        Clock(
            foreground=colors[5],
            background=colors[1],
            fontsize=12,
            format="%Y-%m-%d %H:%M",
            mouse_callbacks={'Button1': lambda qtile: qtile.cmd_spawn("xfce4-terminal cal -3")}
        ),
        # WidgetBox(widgets=[
        #    TextBox(text="This widget is in the box"),
        #    Memory()
        # ],background=colors[1]),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        Systray(
            background=colors[1],
            icon_size=20,
            padding=4
        ),
    ]
    return widgets_list


def init_widgets_list_2():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        GroupBox(font="FontAwesome",
                 fontsize=18,
                 margin_y=-1,
                 margin_x=0,
                 padding_y=6,
                 padding_x=5,
                 borderwidth=0,
                 disable_drag=True,
                 active=colors[5],
                 inactive=colors[9],
                 rounded=True,
                 highlight_method="text",
                 this_current_screen_border=colors[3],
                 other_current_screen_border=colors[8],
                 foreground=colors[2],
                 background=colors[1]
                 ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        CurrentLayout(
            font="Noto Sans Bold",
            foreground=colors[5],
            background=colors[1]
        ),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        # WindowName(font="Noto Sans",
        #           fontsize=12,
        #           foreground=colors[5],
        #           background=colors[1],
        #           ),
        Spacer(opacity=0),
        Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[1]
        ),
        # TaskList(),
        Net(
            font="FontAwesome",
            fontsize=12,
            interface="wlp26s0",
            foreground=colors[2],
            background=colors[1],
            padding=0,
            format="{down} ↓↑ {up}"
        ),
    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list_2()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8)),
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)), ]


screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Click([mod], "Button2", lazy.window.toggle_floating(), start=lazy.window.get_size()),
    # Click([mod], "Button3", lazy.window.bring_to_front()),
    Click([mod], "Button8", lazy.prev_layout()),
    Click([mod], "Button9", lazy.next_layout())

]

dgroups_key_binder = None
dgroups_app_rules = []

main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]

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
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='arcolinux-logout'),
    # Match(wm_class='xfce4-terminal'),
    Match(title='Picture in picture'),

], fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
