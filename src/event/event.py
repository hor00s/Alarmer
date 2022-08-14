import os
import sys
import json
import pickle

class EventSetupError(Exception): ...

class Event:
    EXTENSION = '.json'
    FILE = os.path.join('..', '.events')
    TESTFILE = os.path.join('..', '.testevents')
    MAX_YEAR = 2030
    def __init__(self, name: str, time: str, date: str, category: str) -> None:
        """
        Usecase:
        ```
            Event(
                name="Event_name",
                time="15:30",
                date="15-04-2022",
                category="Important",
            )
        """
        self._name = self._set_name(name)
        self._time = self._set_time(time)
        self._date = self._set_date(date)
        self._category = self._set_category(category)
        self._file_name = f"{self._name}{Event.EXTENSION}"
        # self._event = [('name', self._name), ('time', self._time), ('date', self._date), ('category', self._category)]
        self._event = {'name': self._name, 'time': self._time, 'date': self._date, 'category': self._category}
        self.hour, self.min = self.time.split(':')
        self.day, self.month, self.year = self.date.split('-')

    def __str__(self) -> str:
        return str(self._event)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('name', {self.name})"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __o: object) -> bool:
        return self.name == __o

    def __len__(self):
        return len(self._event)

    def __getitem__(self, i):
        return self._event[i]

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    @property
    def name(self):
        return self._name

    @property
    def time(self):
        return self._time

    @property
    def date(self):
        return self._date

    @property
    def category(self):
        return self._category

    @property
    def file_name(self):
        return self._file_name

    @staticmethod
    def load(name: str, file: str=FILE):
        """Find an event in the file and load it directly as an Event instance
        (Adds the .pkl automatically)
        ```
            event = Event.load(file_name)
            type(event)
            >>> __main__.Event
        ```
        :param str name: Name of the pkl file
        :param str file: Event or Testevent file, defaults to EVENT_FILE
        :return Event:
        """
        if not f"{name}{Event.EXTENSION}" in os.listdir(file):
            raise FileNotFoundError(f"There is not event `{name}`")
        with open(os.path.join(file, f"{name}{Event.EXTENSION}"), mode='r') as f:
            data = json.load(f)

        return Event(*[data[v] for v in data])

    @staticmethod
    def is_valid_name(name: str, platform: str=sys.platform) -> bool:
        """Validate name of an event
        ```
            Event.is_valid_name("some_name")
        ```
        :param str name:
        :param str platform: The User's OS, defaults to sys.platform
        :return bool:
        """        
        with open(os.path.join('event', 'dissallowedchars.json'), mode='r') as f:
            data = json.load(f)
        chars = data[platform]
        for char in list(name):
            if char in chars:
                return False
        return True

    @staticmethod
    def is_valid_time(time: str) -> bool:
        """Validate time of an event
        ```
            Event.is_valid_hour("15:30")
        ```
        :param str time:
        :return bool:
        """        
        hour, minute = time.split(':')
        return 0 <= int(hour) < 24\
        and 0 <= int(minute) < 60

    @staticmethod
    def is_valid_date(date: str) -> bool:
        """Validate date of an event
        ```
            Event.is_valid_date("15-05-2022")
        ```
        :param str date:
        :return bool:
        """        
        day, month, year = date.split('-')
        return 0 <= int(day) <= 31\
        and 1 <= int(month) <= 12\
        and 2022 <= int(year) <= Event.MAX_YEAR

    def _set_name(self, name: str, platform: str=sys.platform):
        if not Event.is_valid_name(name, platform) or not name:
            raise EventSetupError("Name either contains an illegal character or is empty")
        return name

    def _set_date(self, date: str):
        if not Event.is_valid_date(date):
            raise EventSetupError("Date is invalid")
        return date

    def _set_time(self, time: str):
        if not Event.is_valid_time(time):
            raise EventSetupError("Time is invalid")
        return time

    def _set_category(self, category):
        if not category:
            raise EventSetupError("Category either contains an illegal character or is empty")
        return category

    def save(self, file: str=FILE):
        """Save self._event of an initiated event into the file

        :param str file: Location for the file to be saved (.pkl is added automatically), defaults to EVENT_FILE
        """        
        with open(os.path.join(file, self._file_name), mode='w') as f:
            json.dump(self._event, f)

    def edit(self, new_name: str, new_time: str, new_date: str, new_category: str, file: str=FILE):
        """Load an event and edit its properties
        Example:
        ```
            event = Event.load(name, file)
            event.edit(name, time, date, category)
        ```
        :param str new_name: In this case we have to delete the file with the prev name
        :param str new_time:
        :param str new_date:
        :param str new_category:
        :param str file: Event or Testevent file, defaults to EVENT_FILE
        """        
        if new_name != self._name: # In case user edits the name we have to delete the file with the old name and create a new one
            os.remove(os.path.join(file, f"{self._name}{Event.EXTENSION}"))
        new_event = Event(
            name=self._set_name(new_name),
            time=self._set_time(new_time),
            date=self._set_date(new_date),
            category=new_category
        )
        new_event.save(file)

    def items(self):
        return self._event.items()
