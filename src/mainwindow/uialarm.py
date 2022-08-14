import time
import webbrowser
from datetime import datetime as dt
from event.event import Event
from .actions import (
    delete_selected_event,
    _get_selected_event,
    reset_alarm_values,
    check_event_exists,
    delete_all_events,
    update_list,
    form_event,
    pop_up,
)
from .settings import (
    get_config_attribute,
    change_alarm_sound,
    change_background,
    set_configuration,
    set_background,
    get_header,
    get_color,
)
from .constants import (
    APP_IMAGE,
    MAINUI,
    REPO,
)
from PyQt5.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QListWidget,
    QTabWidget,
    QComboBox,
    QLineEdit,
    QAction,
    QLabel,
)
from PyQt5 import uic, QtGui
from summary_window.summary import TldrWindow


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi(MAINUI, self)
        self.current_editing = None
        self.wwidht, self.wheight = self.size().width(), self.size().height()
        self.bg_fixed_size = get_config_attribute('bg_scale_size')
        self.setWindowIcon(QtGui.QIcon(APP_IMAGE))

        self.tab_widget = self.findChild(QTabWidget, 'tabWidget')
        self.tab_widget.setCurrentIndex(0)
        # 1st tab widgets
        self._load_labels()
        self._load_line_edits()
        self._load_buttons()
        self._load_comboboxes()

        # Button commands
        self.ok_btn.clicked.connect(lambda: self.ok())
        self.delete_all_btn.clicked.connect(lambda: delete_all_events(self.list_widget, self._pop_up2_lbl, self.yesno_messagebox))
        self.delete_btn.clicked.connect(lambda: delete_selected_event(self.list_widget, self._pop_up2_lbl))
        self.edit_btn.clicked.connect(lambda: self.edit_event(self.list_widget))

        # MENU BAR #
        # Preferences
        self.actionBackground.triggered.connect(lambda: change_background(self, self.messagebox, pop_up, self._pop_up_lbl))
        self.actionText_color.triggered.connect(lambda: self.change_text_color('Text color', 'Enter a hex (#FFFFFF) value, or and RGB (255,0,0) value):'))
        self.actionAlarm_sound.triggered.connect(lambda: change_alarm_sound(self, pop_up, self._pop_up_lbl))
        # Setings
        self.actionHeader.triggered.connect(lambda: self.change_header_text('Header text', 'Your new header:'))
        self.actionSummary_window_on.triggered.connect(lambda: set_configuration('tldr_window', True))
        # Help
        self.actionSource_code.triggered.connect(lambda: self.source_code_prompt())

        # Apearence
        set_background(self.tab1_bg_lbl, (self.wwidht, self.wheight), self.bg_fixed_size)
        update_list(self.list_widget)
        self._set_date_today()

        self.show()

    def _load_labels(self):
        self.tab1_bg_lbl = self.findChild(QLabel, 'tab1_bg')
        self.header_lbl = self.findChild(QLabel, 'header_lbl')
        self.name_lbl = self.findChild(QLabel, 'name_lbl')
        self.time_lbl = self.findChild(QLabel, 'time_lbl')
        self.hour_lbl = self.findChild(QLabel, 'hour_lbl')
        self.min_lbl = self.findChild(QLabel, 'min_lbl')
        self.date_lbl = self.findChild(QLabel, 'date_lbl')
        self.type_lbl = self.findChild(QLabel, 'type_lbl')
        self.day_lbl = self.findChild(QLabel, 'day_lbl')
        self.month_lbl = self.findChild(QLabel, 'month_lbl')
        self.year_lbl = self.findChild(QLabel, 'year_lbl')
        self._pop_up_lbl = self.findChild(QLabel, '_pop_up_lbl')
        self._pop_up2_lbl = self.findChild(QLabel, 'tab2_pop_up')

        r, g, b = get_config_attribute('text_tab1_color')
        header = get_config_attribute('tab1_header')

        self.header_lbl.setText(header)
        self.tab1_bg_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.header_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.name_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.time_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.hour_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.min_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.date_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.type_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.day_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.month_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self.year_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")
        self._pop_up_lbl.setStyleSheet(f"color: rgb({r}, {g}, {b})")

    def _load_line_edits(self):
        self.name_entry = self.findChild(QLineEdit, 'name_entry')
        self.type_entry = self.findChild(QLineEdit, 'type_entry')

    def _load_buttons(self):
        self.ok_btn = self.findChild(QPushButton, 'ok_btn')
        self.cancel_btn = self.findChild(QPushButton, 'cancel_btn')
        self.edit_btn = self.findChild(QPushButton, 'edit_btn')
        self.delete_btn = self.findChild(QPushButton, 'delete_btn')
        self.delete_all_btn = self.findChild(QPushButton, 'delete_all_btn')

    def _load_comboboxes(self):
        self.hour_box = self.findChild(QComboBox, 'hour_box')
        self.min_box = self.findChild(QComboBox, 'min_box')
        self.day_box = self.findChild(QComboBox, 'day_box')
        self.month_box = self.findChild(QComboBox, 'month_box')
        self.year_box = self.findChild(QComboBox, 'year_box')

    def _load_list_widget(self):
        self.list_widget = self.findChild(QListWidget, 'list_widget')

    def _set_date_today(self):
        prev = dt.now()
        date = prev.strftime('%d-%m-%Y')
        day, month, year = date.split('-')
        self.day_box.setCurrentText(day)
        self.month_box.setCurrentText(month)
        self.year_box.setCurrentText(year)

    def ok(self):
        if self.current_editing is None:
            event = form_event(
            self.name_entry.text(),
            f'{self.hour_box.currentText()}:{self.min_box.currentText()}',
            f'{self.day_box.currentText()}-{self.month_box.currentText()}-{self.year_box.currentText()}',
            self.type_entry.text(),
            self._pop_up_lbl,
            )
            if event:
                if check_event_exists(event.name):
                    pop_up(self._pop_up_lbl, f"Event `{event.name}` already exists.")
                else:
                    try:
                        if get_config_attribute("tldr_window"):
                            self.second_window = QMainWindow()
                            self.tldr = TldrWindow(event, pop_up, self._pop_up_lbl, self.list_widget,\
                                self.name_entry, self.hour_box, self.min_box,\
                                    self.day_box, self.month_box, self.year_box, self.type_entry)
                            self.tldr.show()
                        elif not get_config_attribute("tldr_window"):
                            event.save()
                            update_list(self.list_widget)
                            pop_up(self._pop_up_lbl, f"Event `{self.name_entry.text()}` has been saved!")
                            reset_alarm_values(
                                self.name_entry,
                                self.day_box,
                                self.month_box,
                                self.year_box,
                                self.hour_box,
                                self.min_box,
                                self.type_entry,
                                )
                    except AttributeError as e:
                        print(e)

                    else:
                        update_list(self.list_widget)

        elif self.current_editing:
            to_edit = Event.load(self.current_editing)
            time = f"{self.hour_box.currentText()}:{self.min_box.currentText()}"
            date = f"{self.day_box.currentText()}-{self.month_box.currentText()}-{self.year_box.currentText()}"
            to_edit.edit(self.name_entry.text(), time, date, self.type_entry.text())
            update_list(self.list_widget)
            pop_up(self._pop_up_lbl, f"Event `{to_edit.name}` is edited!")
            reset_alarm_values(
                self.name_entry,
                self.day_box,
                self.month_box,
                self.year_box,
                self.hour_box,
                self.min_box,
                self.type_entry,
                )
            self.current_editing = None

    def edit_event(self, list_widget):
        self.current_editing = _get_selected_event(list_widget)
        e = Event.load(self.current_editing)
        self.name_entry.setText(e.name)
        self.hour_box.setCurrentText(e.hour)
        self.min_box.setCurrentText(e.min)
        self.day_box.setCurrentText(e.day)
        self.month_box.setCurrentText(e.month)
        self.year_box.setCurrentText(e.year)
        self.type_entry.setText(e.category)
        self.tab_widget.setCurrentIndex(0)
        pop_up(self._pop_up_lbl, f"Be carefull, you're in `edit` mode. Anything you save will overwrite `{e.name}`")

    def yesno_messagebox(self, title, text):
        answer = {16384: True, 65536: False}
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        x = msg.exec_()
        return answer.get(x, False)

    def messagebox(self, title, text, details=None):
        answer = {16384: True, 65536: False}
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        if details is not None:
            msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        x = msg.exec_()
        if answer.get(x, False):
            set_configuration('bg_scale_size', True)
        elif not answer.get(x, False):
            set_configuration('bg_scale_size', False)

    def change_text_color(self, title: str, text: str):
        color, _ = QInputDialog.getText(self, title, text)
        get_color(color, pop_up, self._pop_up_lbl)

    def change_header_text(self, title, text):
        text, _ = QInputDialog.getText(self, title, text)
        get_header(text, pop_up, self._pop_up_lbl)

    def source_code_prompt(self):
        pop_up(self._pop_up_lbl, 'Consider leaving a star!', seconds=60)
        webbrowser.open(REPO)
