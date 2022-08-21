import os
import sys
import unittest
sys.path.append('.')
import string
import random
from event.event import Event
from ringer import postpone_event

class TestEvent(unittest.TestCase):
    def test_delete_tests(self):  # Keep a limit for the testfiles (Not an actual test)
        MAX_FILES = 4
        files = os.listdir(Event.TESTFILE)
        while len(files) > MAX_FILES:
            file = random.choice(files)
            os.remove(os.path.join(Event.TESTFILE, file))
            files.remove(file)

    def test_valid_time(self):
        valid_times = []
        for i in range(24):
            for j in range(60):
                if len(str(i)) == 1:
                    h = f"0{i}"
                else:
                    h = str(i)
                    
                if len(str(j)) == 1:
                    m = f"0{j}"
                else:
                    m = str(j)
                valid_times.append(f"{h}:{m}")
        
        for t in valid_times:
            self.assertTrue(Event.is_valid_time(t), "A time that should be valid is fails")

    def test_invalid_time(self):
        invalid_times = []
        for i in range(24, 30):
            for j in range(65):
                if len(str(i)) == 1:
                    h = f"0{i}"
                else:
                    h = str(i)
                    
                if len(str(j)) == 1:
                    m = f"0{j}"
                else:
                    m = str(j)
                invalid_times.append(f"{h}:{m}")
                if int(m) > 23: # Reverse the order so we also have invalid hour test-cases
                    invalid_times.append(f"{m}:{h}")
        for t in invalid_times:
            self.assertFalse(Event.is_valid_time(t), "A time that should be invalid passes")

    def test_date(self):
        self.assertTrue(Event.is_valid_date("15-05-2022"), "A date that should be valid fails")
        self.assertTrue(Event.is_valid_date("31-12-2030"), "A date that should be valid fails")
        self.assertTrue(Event.is_valid_date("15-03-2022"), "A date that should be valid fails")
        self.assertFalse(Event.is_valid_date("32-12-2030"), "A date that should not be valid passes")
        self.assertFalse(Event.is_valid_date("15-13-2030"), "A date that should not be valid passes")

    def test_name(self):
        # Linux
        self.assertTrue(Event.is_valid_name('valid.pkl', 'linux'))
        self.assertFalse(Event.is_valid_name('not/valid.pkl', 'linux'))
        # Mac
        self.assertTrue(Event.is_valid_name('valid.pkl', 'darwin'))
        self.assertFalse(Event.is_valid_name('not:valid.pkl', 'darwin'))
        self.assertFalse(Event.is_valid_name('not/valid.pkl', 'darwin'))
        # Windows
        self.assertTrue(Event.is_valid_name('test.pkl', 'win32'))
        self.assertFalse(Event.is_valid_name('not*valid.pkl', 'win32'))
        self.assertFalse(Event.is_valid_name('not/valid.pkl', 'win32'))
        self.assertFalse(Event.is_valid_name('not<valid.pkl', 'win32'))
        self.assertFalse(Event.is_valid_name('not>valid.pkl', 'win32'))

    def test_save(self):
        initial = os.listdir(Event.TESTFILE)
        event = Event(
            name=''.join(random.choices(string.ascii_letters, k=5)),
            time="15:30",
            date="07-05-2022",
            category="Important",
        )
        event.save(Event.TESTFILE)
        after = os.listdir(Event.TESTFILE)
        self.assertEqual(len(initial)+1, len(after), "A file is not saved successfully")

    def test_load(self):
        file = random.choice(os.listdir(Event.TESTFILE))
        event = Event.load(f'{file}', Event.TESTFILE)
        self.assertTrue(isinstance(event, Event), "A loaded event is not loaded as a valid instance")
        self.assertRaises(FileNotFoundError, Event.load, "NotExists", Event.TESTFILE)

    def test_edit(self):
        new_name = "new_name"
        # Test case without editing name
        new_time = "18:20"
        new_date = "22-11-2023"
        new_category = "Not imporant"
        old = Event(
            name="to_edit",
            time="15:30",
            date="15-05-2022",
            category="Imporant"
        )
        old.save(Event.TESTFILE)
        load = Event.load(old.name + '.json', Event.TESTFILE)
        load.edit(old.name, new_time, new_date, new_category, Event.TESTFILE)
        new = Event.load(f"{load.name}.json", Event.TESTFILE)
        self.assertTrue(new.name == old.name, "Name is changed where is shouldn't")
        self.assertTrue(new.time == new_time, "Time is not edited successfully")
        self.assertTrue(new.date == new_date, "Date is not edited successfully")
        self.assertTrue(new.category == new_category, "Category is not edited successfully")
        os.remove(os.path.join(Event.TESTFILE, f"{new.name}{Event.EXTENSION}"))

        # Test case with editing name
        initial = os.listdir(Event.TESTFILE)
        old = Event(
            name="to_edit",
            time="15:30",
            date="15-05-2022",
            category="Imporant"
        )
        old.save(Event.TESTFILE)
        load = Event.load(f'{old.name}.json', Event.TESTFILE)
        load.edit(new_name, old.time, old.date, old.category, Event.TESTFILE)
        new_event = Event.load(f'{new_name}.json', Event.TESTFILE)
        self.assertTrue(new_event.name != old.name, "Name is not edited successfully")
        os.remove(os.path.join(Event.TESTFILE, f"{new_name}{Event.EXTENSION}"))
        after = os.listdir(Event.TESTFILE)
        
        self.assertTrue(len(initial) == len(after), "Old file is not being deleted successfully when editing name")

    # def test_postpone_event(self):
    #     self.assertEqual(postpone_event(22, 4), '22:09')
    #     self.assertEqual(postpone_event(20, 49), '20:54')
    #     self.assertEqual(postpone_event(20, 55), '21:00')
    #     self.assertEqual(postpone_event(20, 57), '21:02')
    #     self.assertEqual(postpone_event(23, 55), '00:00')
    #     self.assertEqual(postpone_event(23, 57), '00:02')

if __name__ == '__main__':
    unittest.main()
