import datetime
import subprocess
from sys import argv
from time import sleep

import pyautogui
import pynput


def print_help():
    print("""-d [yyyy-mm-dd hh:mm AM/PM]
-b [branch name]
-u [messenger url]
-m [message]
-h [help]
--dev for development environment [optional]""")


def send_message(url, message, is_dev=True):
    pyautogui.press("pause")
    sleep(.5)
    # open browser
    pyautogui.press("win")
    sleep(0.5)
    pyautogui.write("edge")
    sleep(.5)
    pyautogui.press("enter")
    sleep(3)

    # open incognito mode
    pyautogui.hotkey("ctrl", "shift", "n")
    sleep(.5)

    # type url
    pyautogui.write("https://www.facebook.com")
    pyautogui.press("enter")
    sleep(3)

    # login
    # type email
    pyautogui.write("atikurrahaman386@gmail.com")
    sleep(.5)
    # select password
    pyautogui.press("tab")
    sleep(.5)
    # type password
    pyautogui.write("Labonno#007")
    sleep(.5)
    pyautogui.press("enter")
    sleep(5)

    # goto messenger url
    pyautogui.hotkey("alt", "d")
    pyautogui.write(url)
    pyautogui.press("enter")
    sleep(5)

    # select message box
    pyautogui.press("f6")
    sleep(.1)
    # 27 shift tab
    for i in range(27):
        pyautogui.hotkey("shift", "tab")
        # sleep(.1)
    # change to avro bangla
    pyautogui.hotkey("win", "space")
    # write message
    pyautogui.write(message)
    sleep(.1)

    # send message
    pyautogui.press("tab")
    if not is_dev:
        pyautogui.press("enter")
        sleep(5)

    # close browser
    if not is_dev:
        pyautogui.hotkey("ctrl", "w")


def deploy_branch():
    if not is_dev:
        subprocess.run(f"cd /home/jibon/website/mymoviebazar.net && "
                       f"git checkout development && "
                       f"git merge {branch} -m 'merged {branch} with development' && "
                       f"git push && "
                       f"git branch {branch} -D && "
                       f"./deploy.sh",
                       shell=True)


_help = False
date = False
branch = False
is_dev = False
url = False
message = False
year = False
month = False
day = False
hour = False
minute = False

try:
    argv.index("-h")
    _help = True
except ValueError:
    _help = False

if _help:
    print_help()
    exit()

try:
    index = argv.index("-d")
    date = argv[index + 1]
except:
    date = False

try:
    index = argv.index("-b")
    branch = argv[index + 1]
except:
    branch = False

try:
    argv.index("--dev")
    is_dev = True
except:
    is_dev = False

try:
    index = argv.index("-u")
    url = argv[index + 1]
except:
    url = False

try:
    index = argv.index("-m")
    message = argv[index + 1]
except:
    message = False
if date:
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M %p")
    except Exception as e:
        print(e)
        pass
    if type(date) is not datetime.datetime:
        date = datetime.datetime.now()
else:
    date = datetime.datetime.now()

if branch or (url and message):
    while True:
        current_date = datetime.datetime.now()
        if current_date >= date:
            # subprocess.run("notify-send -u critical 'a' 'a'", shell=True)
            if branch and not is_dev:
                deploy_branch()
            else:
                print("no branch found, not deploying")
            if url and message:
                send_message(url, message, is_dev)
            else:
                print("no messenger url or message found, not sending update message")
            break
        print(
            f"{branch + ', ' if branch else ''}"
            f"current time: {current_date.strftime('%Y-%m-%d %I:%M:%S %p')}, "
            f"scheduled time: {date.strftime('%Y-%m-%d %I:%M %p')}, {date - current_date} left"
        )
        sleep(1)
else:
    print_help()

if is_dev:
    pressed_esc = False


    def on_press(key):
        global pressed_esc
        if key == pynput.keyboard.Key.esc:
            pressed_esc = True


    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

    run = True
    while run:
        print(pyautogui.position())
        if pressed_esc:
            break
    # close browser
    pyautogui.hotkey("ctrl", "w")
