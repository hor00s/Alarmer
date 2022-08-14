import sys
from typing import Callable
from PyQt5 import QtGui
import PyQt5.QtWidgets as qtw
from mainwindow.constants import APP_IMAGE
from mainwindow.settings import set_configuration
from mainwindow.actions import update_list, reset_alarm_values
sys.path.append('.')
from event.event import Event


class TldrWindow(qtw.QTabWidget):
    def __init__(self, event: Event, pop_up: Callable, pop_up_lbl, list_widget, *entries) -> None:
        super().__init__()
        self.setWindowTitle("Event")
        self.cur_event = event
        self.list_widget = list_widget
        self.pop_up = pop_up
        self.pop_up_lbl = pop_up_lbl
        self.entries = entries
        self.name_e, *_ = entries
        self.setWindowIcon(QtGui.QIcon(APP_IMAGE))

        # Set layout
        self.setLayout(qtw.QVBoxLayout())


        for key, value in self.cur_event.items():
            lbl = qtw.QLabel(f"{key}: {value}")
            self.layout().addWidget(lbl)

        self.do_now_show_again = qtw.QCheckBox("Do now show again", self)
        self.layout().addWidget(self.do_now_show_again)
        ok_btn = qtw.QPushButton("Ok")
        ok_btn.clicked.connect(lambda: self.save_and_close())
        self.layout().addWidget(ok_btn)

    def save_and_close(self):
        if self.do_now_show_again.isChecked():
            set_configuration('tldr_window', False)

        self.cur_event.save()
        update_list(self.list_widget)
        self.pop_up(self.pop_up_lbl, f"Event `{self.name_e.text()}` has been saved!")
        reset_alarm_values(*self.entries)
        self.close()
