import json
import pwd
import os
import pathlib
import re
from suntime import Sun, SunTimeException

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config"
version = "1.5"

def exists():
    """returns True or False wether Config exists or not"""
    return os.path.isfile(path+"/yin_yang/yin_yang.json")


def get_desktop():
    """Return the current desktop's name or 'unkown' if can't determine it"""
    # just to get all possible implementations of dekstop variables
    env = str(os.getenv("GDMSESSION")).lower()
    second_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()
    third_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()

    # these are the envs I will look for
    # feel free to add your Desktop and see if it works
    gnome_re = re.compile(r'gnome')
    budgie_re = re.compile(r'budgie')
    kde_re = re.compile(r'kde')
    plasma_re = re.compile(r'plasma')
    plasma5_re = re.compile(r'plasma5')

    if gnome_re.search(env) or gnome_re.search(second_env) or gnome_re.search(third_env):
        return "gtk"
    if budgie_re.search(env) or budgie_re.search(second_env) or budgie_re.search(third_env):
        return "gtk"
    if kde_re.search(env) or kde_re.search(second_env) or kde_re.search(third_env):
        return "kde"
    if plasma_re.search(env) or plasma_re.search(second_env) or plasma_re.search(third_env):
        return "kde"
    if plasma5_re.search(env) or plasma5_re.search(second_env) or plasma5_re.search(third_env):
        return "kde"
    return "unknown"


def set_sun_time():
    latitude: float = float(get("latitude"))
    longitude: float = float(get("latitude"))
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        print('Today the sun raised at {} and get down at {}'.
              format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

        # Get today's sunrise and sunset in UTC
        update("switchToLight", today_sr.strftime('%H:%M'))
        update("switchToDark", today_ss.strftime('%H:%M'))

    except SunTimeException as e:
        print("Error: {0}.".format(e))


# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path+"/yin_yang").mkdir(parents=True, exist_ok=True)

# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path+"/yin_yang/userscripts").mkdir(parents=True, exist_ok=True)

# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path+"/yin_yang/userscripts/dark").mkdir(parents=True, exist_ok=True)

# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path+"/yin_yang/userscripts/light").mkdir(parents=True, exist_ok=True)

# if there is no config generate a generic one
defaultConfig = {}
defaultConfig["version"] = version
defaultConfig["desktop"] = get_desktop()
defaultConfig["followSun"] = False
defaultConfig["latitude"] = ""
defaultConfig["longitude"] = ""
defaultConfig["schedule"] = False
defaultConfig["switchToDark"] = "20:00"
defaultConfig["switchToLight"] = "07:00"
defaultConfig["running"] = False
defaultConfig["theme"] = ""
defaultConfig["codeLightTheme"] = "Default Light+"
defaultConfig["codeDarkTheme"] = "Default Dark+"
defaultConfig["codeEnabled"] = False
defaultConfig["kdeLightTheme"] = "org.kde.breeze.desktop"
defaultConfig["kdeDarkTheme"] = "org.kde.breezedark.desktop"
defaultConfig["kdeEnabled"] = True
defaultConfig["gtkLightTheme"] = ""
defaultConfig["gtkDarkTheme"] = ""
defaultConfig["atomLightTheme"] = ""
defaultConfig["atomDarkTheme"] = ""
defaultConfig["atomEnabled"] = False
defaultConfig["gtkEnabled"] = False
defaultConfig["wallpaperLightTheme"] = ""
defaultConfig["wallpaperDarkTheme"] = ""
defaultConfig["wallpaperEnabled"] = False
defaultConfig["firefoxEnabled"] = False
defaultConfig["firefoxDarkTheme"] = "firefox-compact-dark@mozilla.org"
defaultConfig["firefoxLightTheme"] = "firefox-compact-light@mozilla.org"
defaultConfig["firefoxActiveTheme"] = "firefox-compact-light@mozilla.org"
defaultConfig["gnomeEnabled"] = False
defaultConfig["gnomeLightTheme"] = ""
defaultConfig["gnomeDarkTheme"] = ""
defaultConfig["kvantumEnabled"] = False
defaultConfig["kvantumLightTheme"] = ""
defaultConfig["kvantumDarkTheme"] = ""
defaultConfig["userscriptsEnabled"] = False
defaultConfig["userscripts"] = path+"/yin_yang/userscripts/"
defaultConfig["desktop"] = get_desktop()

def write_config(config=defaultConfig):
    """Write configuration"""
    with open(path+"/yin_yang/yin_yang.json", 'w') as conf:
        json.dump(config, conf, indent=4)

def update(key, value):
    """Update the value of a key in configuration"""
    config[key] = value
    write_config(config)

def delete_old():
    os.remove(path+"/yin_yang/yin_yang.json")
    print("remove stuff")
    write_config()

if exists():
    # making config global for this module
    with open(path+"/yin_yang/yin_yang.json", "r") as conf:
        config = json.load(conf)
    if version > config["version"]:
        delete_old()
else:
    config = defaultConfig


def get_config():
    """returns the config"""
    return config


def gtk_exists():
    return os.path.isfile(path+"/gtk-3.0/settings.ini")


def get(key):
    """Return the given key from the config"""
    return config[key]


def is_scheduled():
    return config["schedule"]



