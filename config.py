import os
import socket
import subprocess
from datetime import datetime

from libqtile import layout, bar, hook
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.widget.clock import Clock
from libqtile.widget.currentlayout import CurrentLayout
from libqtile.widget.graph import CPUGraph
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.net import Net
from libqtile.widget.prompt import Prompt
from libqtile.widget.sep import Sep
from libqtile.widget.systray import Systray
from libqtile.widget.textbox import TextBox
from libqtile.widget.windowname import WindowName

from task_log import TaskLog

# mod4 or mod = super key
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
    Key([mod], "m", lazy.spawn('pragha')),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawn('rofi-theme-selector')),
    Key([mod], "t", lazy.spawn('urxvt')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    # Key([mod], "w", lazy.spawn('vivaldi-stable')), TODO TEST vivaldi
    Key([mod], "x", lazy.spawn('oblogout')),
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

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
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
    Key([mod, "shift"], "space", lazy.window.toggle_floating()), ]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "XF86Calculator", "XF86HomePage", "XF86AudioMute"]

group_labels = ["", "", "", "", "", "", "", "", "", "", "", "", ""]

group_layouts = [" Tall", " Tall", " Tree", " Tree", " Tall", " Tall", " Tall", " Tall",
                 " Zoomy", " Zoomy", "monadwide", " Max", " Tall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i],
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin": 5,
            "border_width": 2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }


#layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Tall"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Wide"),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    #  layout.Floating(margin=5, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Float"),
    # layout.RatioTile(**layout_theme),
    layout.Zoomy(name=" Zoomy", columnwidth=600,),
    layout.TreeTab(name=" Tree"),
    #    layout.Slice(**layout_theme),
    layout.Max(margin=5, border_width=2, border_focus="#5e81ac", border_normal="#4c566a", name=" Max")
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
            font="FontAwesome",
            fontsize=12,
            interface="enp24s0",
            foreground=colors[2],
            background=colors[1],
            padding=0,
            format="{down} ↓↑ {up}"
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
            format="{MemUsed}/{MemTotal}"
        ),
        # # battery option 1  or ArcoLinux Horizontal icons by default
        # Sep(
        #          linewidth = 1,
        #          padding = 10,
        #          foreground = colors[2],
        #          background = colors[1]
        #          ),
        # arcobattery.BatteryIcon(
        #          padding=0,
        #          scale=0.7,
        #          y_poss=2,
        #          theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
        #          update_interval = 5,
        #          background = colors[1]
        #          ),
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
                 this_current_screen_border=colors[3],
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
        WindowName(font="Noto Sans",
                   fontsize=12,
                   foreground=colors[5],
                   background=colors[1],
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
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=36))]


screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod], "Button8", lazy.prev_layout()),
    Click([mod], "Button9", lazy.next_layout())

]

dgroups_key_binder = None
dgroups_app_rules = []


# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
@hook.subscribe.client_new
def assign_app_group(client):
    # Group_name:[apps names(WM_CLASS)] get apps_names with xprop on terminal
    d = {"1": ["Brave", "Brave-browser", "brave-browser"],
         "4": ["robo3t", "vstudio", "Valentina Studio"],
         "6": ["Vlc", "vlc", "Mpv", "mpv"],

         "XF86HomePage": ["org.remmina.Remmina", "VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
                          "virtualbox manager", "virtualbox machine", "vmplayer", ],

         "9": ["whatsapp-nativefier-d52542", "whatsapp-nativefier-d52542", "Discord", "discord","Slack", "slack"],

         "0": []
         }
    wm_class = client.window.get_wm_class()[0]
    #
    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen()


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
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'Oblogout'},
    ##{'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},

], fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart focus

wmname = "LG3D"

#  LIST OF XF86 bindings
"""
XF86AddFavorite
XF86ApplicationLeft
XF86ApplicationRight
XF86AudioMedia
XF86AudioMute
XF86AudioNext
XF86AudioPause
XF86AudioPlay
XF86AudioPrev
XF86AudioLowerVolume
XF86AudioRaiseVolume
XF86AudioRecord
XF86AudioRewind
XF86AudioStop
XF86Away
XF86Back
XF86Book
XF86BrightnessAdjust
XF86CD
XF86Calculator
XF86Calendar
XF86Clear
XF86ClearGrab
XF86Close
XF86Community
XF86ContrastAdjust
XF86Copy
XF86Cut
XF86DOS
XF86Display
XF86Documents
XF86Eject
XF86Excel
XF86Explorer
XF86Favorites
XF86Finance
XF86Forward
XF86Game
XF86Go
XF86History
XF86HomePage
XF86HotLinks
XF86Launch0
XF86Launch1
XF86Launch2
XF86Launch3
XF86Launch4
XF86Launch5
XF86Launch6
XF86Launch7
XF86Launch8
XF86Launch9
XF86LaunchA
XF86LaunchB
XF86LaunchC
XF86LaunchD
XF86LaunchE
XF86LaunchF
XF86LightBulb
XF86LogOff
XF86Mail
XF86MailForward
XF86Market
XF86Meeting
XF86Memo
XF86MenuKB
XF86MenuPB
XF86Messenger
XF86MonBrightnessUp
XF86MonBrightnessDown
XF86Music
XF86MyComputer
XF86MySites
XF86New
XF86News
XF86Next_VMode
XF86Prev_VMode
XF86OfficeHome
XF86Open
XF86OpenURL
XF86Option
XF86Paste
XF86Phone
XF86Pictures
XF86PowerDown
XF86PowerOff
XF86Next_VMode
XF86Prev_VMode
XF86Q
XF86Refresh
XF86Reload
XF86Reply
XF86RockerDown
XF86RockerEnter
XF86RockerUp
XF86RotateWindows
XF86RotationKB
XF86RotationPB
XF86Save
XF86ScreenSaver
XF86ScrollClick
XF86ScrollDown
XF86ScrollUp
XF86Search
XF86Send
XF86Shop
XF86Sleep
XF86Spell
XF86SplitScreen
XF86Standby
XF86Start
XF86Stop
XF86Support
XF86Switch_VT_1
XF86Switch_VT_10
XF86Switch_VT_11
XF86Switch_VT_12
XF86Switch_VT_2
XF86Switch_VT_3
XF86Switch_VT_4
XF86Switch_VT_5
XF86Switch_VT_6
XF86Switch_VT_7
XF86Switch_VT_8
XF86Switch_VT_9
XF86TaskPane
XF86Terminal
XF86ToDoList
XF86Tools
XF86Travel
XF86Ungrab
XF86User1KB
XF86User2KB
XF86UserPB
XF86VendorHome
XF86Video
XF86WWW
XF86WakeUp
XF86WebCam
XF86WheelButton
XF86Word
XF86XF86BackForward
XF86Xfer
XF86ZoomIn
XF86ZoomOut
XF86iTouch
"""