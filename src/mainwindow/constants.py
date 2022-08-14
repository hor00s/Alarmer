import os
from event.event import Event

REPO = 'https://github.com/pant-s/Alarmer'

APP_IMAGE = os.path.join('..', 'alarm.png')
MAINUI = os.path.join('..', 'alarmer.ui')
RINGERUI = os.path.join('..', 'ringer.ui')
CONFIG_FILE = os.path.join('..', '.config.json')
TEST_CONFIG = os.path.join('..', '.testconfig.json')
BG = os.path.join('components', list(filter(lambda i: i.startswith('bg'), os.listdir('components')))[0])
SOUND = os.path.join('components', list(filter(lambda i: i.endswith('.mp3'), os.listdir('components')))[0])
DEFAULT_SOUNDS = os.path.join('..', 'default_sounds')
DEFAULT_BG = os.path.join('..', 'default_backgrounds')
