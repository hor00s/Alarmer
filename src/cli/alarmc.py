#!/bin/env python3
import sys
from commands import commands, help_prompt
from colorama import Fore

if __name__ == '__main__':
    try:
        _, command, *arguments = sys.argv
        full_command = {key: arg for key, arg in zip(arguments[::2], arguments[1::2])}
        commands.get(command)(full_command)
    except Exception as e:
        print('\n' + Fore.RED, e)
        print(f"{Fore.GREEN}Try `alarmc.py help` to see the help prompt")
    