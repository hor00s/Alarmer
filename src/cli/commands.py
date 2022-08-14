import os
import sys
import shutil
from colorama import Fore
from colormap import hex2rgb
from datetime import datetime as dt
sys.path.append('.')
from event.event import Event
from mainwindow.actions import check_event_exists
from mainwindow.constants import BG, SOUND, REPO
from mainwindow.settings import (
    _validate_rgb,
    _validate_hex,
    set_configuration
)
import webbrowser

help_prompt = """
Argumens: -n (Name) | -d (Date) | -t (Time) | -c (Category) | -f (Find) | -c (Color) | -p (Path)
Commands: ad | rm | delall | peek | help | edit | showall | delall | bg | sound | textclr | code

Command: delall ~ None
    Example:
    - $ alarmc delall
    Usage:
    - Deletes all the events

Command: ad ~ Arguments: -n -d -t -c
    Example:
    - $ alarmc ad -n workout -d 15-05-2022 -t 18:00 -c Important
    Usage:
    - Adds an event
    - EXTRA: Setting `-d today` will translate as the today's date

Command: rm ~ Arguments: -n -d -t -c
    Example:
    - $ alarmc rm -n workout (It will delete the event by name)
    - $ alarmc rm -d 15-05-2022 (It will delete all the events assigned at a certain date (15-05-2022 in this case))
    Usage:
    - Removes an event by the given name / date / time / category (Unrecoverable)

Command edit ~ Arguments: (Required) -f Optional (-n -d -t -c)
    Example:
    - $ alarmc edit -f workout -t 16:45
    - $ alarmc edit -f workout -d 16-05-2022
    Usage:
    - Edits one or more properties of an event
    - EXTRA: Setting `-d today` will translate as the today's date

Command peek ~ Arguments: -n
    Example:
    - $ alarmc peek -n workout
    Usage:
    - Prints out details of an event

Command showall ~ Arguments: None
    Example:
    - $ alarmc showall ~ Arguments: (Optional) -v
    Example:
    - $ alarmc showall -v 1 (For verbose result)
    - $ alarmc showall -v 0 (For quiet result)
    Note:
    - -v Defaults to '0' or 'quiet'
    Usage:
    - Shows all the saved events along with the details

Command delall ~ Arguments: None
    Example:
    - $ alarmc delall
    Usage:
    - Deletes all the saved events from the file. (Unrecoverable)

Command help ~ Arguments: None
    Example:
    - $ alarmc help
    Usage:
    - Prints the help prompt

Command bg ~ Arguments: -p
    Example:
    - $ alarmc -p path/to/file.jpg
    Usage:
    - Changes the UI's background

Command sound ~ Arguments: -p
    Example:
    - $ alarmc -p path/to/sound.jpg
    Usage:
    - Changes the notification sound

Command textclr ~ Arguments -c
    Example:
    - $ alarmc -c 125,125,125
    - $ alarmc -c \#FF0000 (Make sure to use the `\` backslash before the `#` hash)
    Usage:
    - Changes the UI's text color

Command code ~ Arguments None
    Example:
    - $ alarmc code
    Usage:
    - Prompts you to the project's source code
"""
prev = dt.now()

def setup_event(name, time, date, category) -> Event:
    try:
        return Event(
            name=name,
            time=time,
            date=date,
            category=category,
        )
    except Exception as e:
        print(f"{Fore.RED}{e}")
        sys.exit(0)


def ad(arguments: dict):
    if arguments['-d'] == 'today':
        arguments['-d'] = prev.strftime('%d-%m-%Y')

    e = setup_event(arguments['-n'], arguments['-t'], arguments['-d'], arguments['-c'])
    if check_event_exists(e):
        print(f"{Fore.RED}An event with this name already exists. Change name or choose the `edit` option")
    else:
        e.save()
        print(f"{Fore.GREEN}Event: `{arguments['-n']}` has been saved")


def rm(arguments: dict):
    by_name = arguments.get('-n')
    by_date = arguments.get('-d')
    by_time = arguments.get('-t')
    by_category = arguments.get('-c')
    for e in os.listdir(Event.FILE):
        event = Event.load(e[:-5])
        if by_name:
            name = arguments['-n']
            os.remove(os.path.join(Event.FILE, name + Event.EXTENSION))
            print(f"{Fore.RED}Event: `{name}` has been deleted")
            break
        elif by_date:
            if event.date == arguments['-d']:
                os.remove(os.path.join(os.path.join(Event.FILE, event.name + Event.EXTENSION)))
                print(f"{Fore.RED}Event: `{event.name}` has been deleted")
        elif by_time:
            if event.time == arguments['-t']:
                os.remove(os.path.join(os.path.join(Event.FILE, event.name + Event.EXTENSION)))
                print(f"{Fore.RED}Event: `{event.name}` has been deleted")
        elif by_category:
            if event.category == arguments['-c']:
                os.remove(os.path.join(os.path.join(Event.FILE, event.name + Event.EXTENSION)))
                print(f"{Fore.RED}Event: `{event.name}` has been deleted")

def edit(arguments: dict): # TODO: Edit name bug
    to_edit = arguments['-f']
    e = Event.load(to_edit)
    if not '-n' in arguments:
        arguments['-n'] = e.name
    if not '-d' in arguments:
        arguments['-d'] = e.date
    if not '-t' in arguments:
        arguments['-t'] = e.time
    if not '-c' in arguments:
        arguments['-c'] = e.category
    if arguments['-d'] == 'today':
        arguments['-d'] = prev.strftime('%d-%m-%Y')

    print(f"{Fore.RED}Edited:\t{Event.load(to_edit)}")
    e.edit(arguments['-n'], arguments['-t'], arguments['-d'], arguments['-c'])
    print(f"{Fore.GREEN}To:\t{Event.load(e.name)}")
    

def peek(arguments: dict):
    name = arguments['-n']
    e = Event.load(name)

    for key, value in e.items():
        print(f"{Fore.GREEN}{key}:  {value}")


def showall(arguments: dict):
    verbose = arguments.get('-v')
    for i, e in enumerate(os.listdir(Event.FILE)):
        event = Event.load(e[:-5])
        if verbose is None or verbose == '0':
            print(f"{i}. {event.name}")
        elif verbose == '1':
            print(f"{i}. {event}")


def delall(*args):
    for e in os.listdir(Event.FILE):
        os.remove(os.path.join('..', '.events', e))
    print(f"{Fore.RED}All events have beed deleted")


def help(*args):
    print(help_prompt)

def bg(arguments: dict):
    file_name = arguments['-p'].split(os.sep)[-1]
    ext = file_name[-3:]
    shutil.copy(arguments['-p'], 'components')
    os.remove(BG)
    os.rename(os.path.join('components', file_name), os.path.join('components', f'bg.{ext}'))
    print(f"{Fore.GREEN}Background changed succesfuly")

def sound(arguments: dict):
    file_name = arguments['-p'].split(os.sep)[-1]
    ext = file_name[-3:]
    if os.path.exists(arguments['-p']) and ext == 'mp3':
        os.remove(SOUND)
        shutil.copy(arguments['-p'], 'components')
        print(f"{Fore.GREEN}Notification sound changed succesfuly")
    else:
        print(f"{Fore.RED}Something went wrong. Sound was not changed")

def textclr(arguments: dict):
    color = arguments['-c']
    if color.startswith('#') and _validate_hex(color):
        set_configuration('text_tab1_color', list(hex2rgb(color)))
        print(f"{Fore.GREEN}Color changed succesfuly")
        return
    else:
        color = color.split(',')
    color = list(map(lambda i: int(i), color))
    if _validate_rgb(color):
        set_configuration('text_tab1_color', color)
        print(f"{Fore.GREEN}Color changed succesfuly")
        return

def code(*args):
    webbrowser.open(REPO)


commands = {
    'ad': ad,
    'rm': rm,
    'delall': delall,
    'edit': edit,
    'peek': peek,
    'showall': showall,
    'help': help,
    'bg': bg,
    'sound': sound,
    'textclr': textclr,
    'code': code,
}
