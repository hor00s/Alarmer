<h1 align="center">Alarmer</h1>
<font size="3">
- Your classic TODO App that will produce a sound notification so you don't miss anything!
</font>

<hr style="border:px solid gray">

<h2>~ FEATURES ~</h2>

<font size="4">- Customizable sound notification</font>

You can select how the sound for you notifications through `Preference -> Alarm sound` (Accepts only .mp3 file format for now) 

<font size="4">- Customizable text colors</font>

Select the color theme through `Preferences -> Text color` (Acceps both Hex (#FF0000) and RGB (255, 0, 0) values) 

<font size="4">- Personalized background</font>

Choose the UI's background through `Preferences -> Background` (Accepts `.jpg` and `.png` and can be scaled down by user's preference although it is recommended for bigger images)

<font size="4">- Personalized header</font>

You set the APP's header, which by default is empty. Set one through `Settings -> Header` and see what it does! (Maxes at 20 characters)

<font size="4">- Flexible cli tool</font>

A flexible cli tools that let you do everything that is available in the app from the command line and more (Doesn't support the customizations **yet**)

<h2>~ HOW TO USE ~</h2>

For the gui, simply start the `Alarmer.py`, fill the fields, save, good to go. The app will then save the event in .events folder as a pickle file `(.pkl)` and check every 30 seconds. If it matches the date and time the `ringer.py` will be initiated by it self and notify you. The `Postpone` option will shut the sound notification and move your event 5 minutes later. The `Ok` button will shut the alarm and delete the event from the file. Shutting the window with the `X` button will also shut the notification but the file will not be deleted. If a mistake like this happens, it can also be deleted manually from th GUI by going to the `second tab -> select the event -> Delete`. The cli the tool can be found in `cli/alarmc.py`. Now run `alarmc.py help` for a detailed guide on how to use it!
<hr style="border:px solid gray">
<h2>~ WHAT IT SOLVES ~</h2>

- Nothing that it is not solved already with better tools

- Makes me happy!

<hr style="border:px solid gray">
<h2>~ KNOWN ISSUES ~</h2>

- Dates are simply passed as valid if the day is less than 31. The issue that this introduces, (let's take February for example) is that if a user adds an event at 30th day of the month it will still pass as valid

- The way the alarms are set up is not the most convinient yet

- Needs some more detailed error messages.

<hr style="border:px solid gray">
<h2>~ INSTALLATION ~</h2>

```git clone https://github.com/pant-s/Alarmer.git
cd Alarmer/src
pip install -r requirements.txt
python3 Alarmer.py # For the GUI
python3 cli/alarmc.py help # To see the usage of the cli
./linux-build.sh # To activate the timer
```
At this point the main application is located in `src/Alarmer.py` and cli is located in `src/cli/alarmc.py`. Do not manually start the `src/ringer.py` as this is the notification prompt and it's infinite loop will waste resources of your machine. The `linux-build.sh` does a better job by running it once every 30 seconds!

Note: It is also recommended that if you want to run this in a virtual environment to create it in `src/`
<br>
<br>
# *Support for windows is on the way when I figure some stuff out!*
