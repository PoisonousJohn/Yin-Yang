import subprocess
from src import config
from os import listdir

userscripts = config.get("userscripts")

def switch_to_light():
    light_userscripts = listdir(userscripts+"light")
    for script in light_userscripts:
        subprocess.run(["sh", userscripts+"light/"+script])


def switch_to_dark():
    dark_userscripts = listdir(userscripts+"dark")
    for script in dark_userscripts:
        subprocess.run(["sh", userscripts+"dark/"+script])
