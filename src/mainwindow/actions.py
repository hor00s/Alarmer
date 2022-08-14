import os
import time
import threading as thr
from typing import Callable
from PyQt5.QtWidgets import QLineEdit, QComboBox
from event.event import (
    EventSetupError,
    Event,
)


def _pop_up_lbl(lbl, msg: str, seconds: int=3):
    """# Template for the threaded function.
    # Do not use directly
    """    
    lbl.setText(msg)
    time.sleep(seconds)
    lbl.setText('')


def pop_up(lbl, msg, seconds: int=3):
    """Show the error message in the window's pop up label

    :param QLabel lbl: THe pop up label
    :param str msg: The message to be show to the user
    :param int seconds: The seconds which the label will be displayed, defaults to 3
    """    
    pop = thr.Thread(target=_pop_up_lbl, args=(lbl, msg, seconds))
    pop.start()


def form_event(name, time, date, category, pop_lbl) -> Event:
    """Form the event taken from the UI

    :param QLineEdit name: Name of the event
    :param QLineEdit time: Time of the event
    :param QLineEdit date: Date of the event
    :param QLineEdit category: Category of the event
    :param QLabel pop_lbl: The pop up label
    :return Event:
    """    
    try:
        return Event(
            name=name,
            time=time,
            date=date,
            category=category,
        )
    except EventSetupError as e:
        pop_up(pop_lbl, str(e))


def reset_alarm_values(*values):
    """Resets all the defined values from boxes and entries
        in the main window
    """
    for v in values:
        if isinstance(v, QLineEdit):
            v.setText('')
        elif isinstance(v, QComboBox):
            v.setCurrentText([v.itemText(i) for i in range(v.count())][0])


def update_list(list_widget):
    """Clear the list, iterate the .events file and add all the events is the UI

    :param QListWidget list_widget:
    """    
    list_widget.clear()
    for event in os.listdir(Event.FILE):
        e = Event.load(event[:-5])
        text = f"  Name: {e.name} | Date: {e.date} | Time: {e.time} | Type: {e.category}"
        list_widget.addItem(text)


def delete_all_events(list_widget, pop_up_lbl, msgbox: Callable):
    """Delete all the events from the .events folder

    :param QListWidget list_widget:
    :param Callable pop_up: _description_
    :param QLabel pop_lbl: The pop up label
    :param Callable msgbox: _description_
    """    
    q = msgbox("Delete all", "Are you sure you want to proceed?")
    if q:
        for event in os.listdir(Event.FILE):
            os.remove(os.path.join(Event.FILE, event))
        pop_up(pop_up_lbl, "All events have been deleted!")
        update_list(list_widget)
    else:
        pop_up(pop_up_lbl, "`Delete all` Aborted!")


def _get_selected_event(list_widget) -> str:
    """Get the selected event from the list

    :param QListWidget list_widget:
    :return str: Name of the selected event
    """    
    clicked = list_widget.currentRow()
    text = list_widget.takeItem(clicked).text().split('|')
    name = text[0].split(':')
    event_name = name[1].rstrip().lstrip()
    return event_name


def delete_selected_event(list_widget, pop_up_lbl):
    """Deleted one selected event

    :param QListWidget list_widget:
    """    
    name = _get_selected_event(list_widget)
    for event in os.listdir(Event.FILE):
        e = Event.load(event[:-4])
        if e.name == name:
            os.remove(os.path.join(Event.FILE, e.file_name))
    pop_up(pop_up_lbl, f"Event `{name}` has been deleted!")


def check_event_exists(name):
    for f in os.listdir(Event.FILE):
        event = Event.load(f[:-5])
        if event == name:
            return True
    return False
