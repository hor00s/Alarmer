#!/bin/env python3
import os
import sys
import pygame as pg
from datetime import datetime as dt
from event.event import Event
from mainwindow.constants import (
    RINGERUI,
    SOUND,
    APP_IMAGE
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
)
from PyQt5 import uic, QtGui


class Ringer(QMainWindow):
    def __init__(self, event: Event):
        super(Ringer, self).__init__()
        uic.loadUi(RINGERUI, self)
        self.prev = dt.now()
        self.hour, self.min = prev.strftime("%H:%M").split(':')
        self.setWindowTitle(event.name)
        self.setWindowIcon(QtGui.QIcon(APP_IMAGE))
        
        self.name_lbl = self.findChild(QLabel, 'event_name')
        self.type_lbl = self.findChild(QLabel, 'event_type')

        self.postpone_btn = self.findChild(QPushButton, 'postpone_btn')
        self.ok_btn = self.findChild(QPushButton, 'ok_btn')
        self.ok_btn.clicked.connect(self.ok)
        
        self.postpone_btn.clicked.connect(lambda: event.edit(
            event.name,
            postpone_event(int(self.hour), int(self.min), self),
            event.date,
            event.category
        ))

        pg.mixer.music.load(SOUND)
        pg.mixer.music.play(-1)

        self.name_lbl.setText(event.name)
        self.type_lbl.setText(event.category)

        self.show()

    def ok(self):
        self.close()
        pg.mixer.quit()
        os.remove(os.path.join(Event.FILE, event.file_name))


def time_to_string(hour, minute):
    h = None
    m = None
    if len(str(hour)) == 1:
        h = f"0{hour}"
    else:
        h = f"{hour}"
    if len(str(minute)) == 1:
        m = f"0{minute}"
    else:
        m = f"{minute}"
    return f"{h}:{m}"

def postpone_event(hour, minute, self):
    if minute < 55:
        minute += 5
    elif minute >= 55 and hour == 23:
        minute += 5
        minute = str(minute)[1]
        hour = 0
    elif minute >= 55 and hour < 23:
        minute += 5
        minute = str(minute)[1]
        hour += 1
    pg.mixer.quit()
    self.close()
    return time_to_string(hour, minute)

def check_events(current_time, date):
    for event in os.listdir(Event.FILE):
        e = Event.load(event[:-5])
        if e.time == current_time and e.date == date:
            return e
        

if __name__ == '__main__':
    event = None
    if event is None:
        prev = dt.now()
        current_time = prev.strftime("%H:%M")
        date = prev.strftime('%d-%m-%Y')
        event = check_events(current_time, date)

    if event:
        pg.mixer.init()
        app = QApplication(sys.argv)
        ringer = Ringer(event)
        app.exec_()
