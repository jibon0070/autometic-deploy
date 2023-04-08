import datetime
import re
import subprocess
from sys import argv
from time import sleep

import pyautogui
import pynput


class AutomaticDeploy:
    one_min_alert = False
    send_notf_at = 60

    def __init__(self):
        arguments = self.get_arguments()
        self.is_dev = arguments['is_dev']
        self.branch = arguments['branch']
        if not arguments['working_directory'] or not arguments['working_branch']:
            self.print_help()
            return
        self.working_directory = arguments['working_directory']
        self.working_branch = arguments['working_branch']

        if arguments['help']:
            self.print_help()
            return

        if not arguments['profile_directory']:
            self.print_help()
            return

        date = self.date(arguments['date'])

        if (arguments['branch'] and arguments['working_directory'] and arguments['working_branch']) or (
                arguments['url'] and arguments['message']):
            self.one_min_alert = (date - datetime.datetime.now()).seconds <= self.send_notf_at
            while True:
                current_date = datetime.datetime.now()
                if current_date >= date:
                    subprocess.run(
                        f"notify-send -u critical 'Automatic Deploy' 'About to deploy {arguments['branch']} branch. "
                        f"Do not interrupt, do not touch keyboard or mouse.'", shell=True)
                    if arguments['branch'] and not self.is_dev:
                        self.deploy_branch()
                    else:
                        print("no branch found, not deploying")
                    if arguments['url'] and arguments['message']:
                        self.send_message(arguments['url'], arguments['message'], arguments['profile_directory'],
                                          self.is_dev)
                    else:
                        print("no messenger url or message found, not sending update message")
                    subprocess.run(
                        f"notify-send -u critical 'Automatic Deploy' 'Deployment finished, you may continue.'",
                        shell=True)
                    break
                remaining = date - current_date
                if remaining.seconds <= self.send_notf_at and not self.one_min_alert:
                    subprocess.run(f"notify-send -u critical "
                                   f"'Automatic Deploy' "
                                   f"'About to deploy in 1 minute. Premare to stay still.'", shell=True)
                    self.one_min_alert = True
                print(
                    f"{arguments['branch'] + ', ' if arguments['branch'] else ''}"
                    f"current time: {current_date.strftime('%Y-%m-%d %I:%M:%S %p')}, "
                    f"scheduled time: {date.strftime('%Y-%m-%d %I:%M %p')}, {remaining} left"
                )
                sleep(1)
        else:
            self.print_help()

        if self.is_dev:
            self.pressed_esc = False

            def on_press(key):
                if key == pynput.keyboard.Key.esc:
                    self.pressed_esc = True

            listener = pynput.keyboard.Listener(on_press=on_press)
            listener.start()

            run = True
            while run:
                print(pyautogui.position())
                if self.pressed_esc:
                    break
            # close browser
            pyautogui.hotkey("ctrl", "w")

    @staticmethod
    def print_help():
        print("""-d [yyyy-mm-dd hh:mm AM/PM]
-b [branch name]
-u [messenger url]
-m [message]
-p [profile directory]
-wd [working directory]
-wb [working branch]
-h [help]
--dev for development environment [optional]""")

    @staticmethod
    def get_arguments():
        date = False
        branch = False
        url = False
        message = False
        profile_directory = False
        _help = False
        is_dev = False
        working_directory = False
        working_branch = False

        try:
            argv.index("-h")
            _help = True
        except:
            _help = False

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

        try:
            index = argv.index("-p")
            profile_directory = argv[index + 1]
        except:
            profile_directory = False

        try:
            index = argv.index("-wd")
            working_directory = argv[index + 1]
        except:
            working_directory = False

        try:
            index = argv.index('-wb')
            working_branch = argv[index + 1]
        except:
            working_branch = False

        return {"date": date, "branch": branch, "url": url, "message": message, "profile_directory": profile_directory,
                "help": _help, "is_dev": is_dev, "working_directory": working_directory,
                "working_branch": working_branch}

    @staticmethod
    def send_message(url: str, message: str, profile_directory: str, is_dev: bool = True):
        # open browser
        sleep(.5)
        pyautogui.press("win")
        sleep(.5)
        pyautogui.write("edge")
        sleep(.5)
        pyautogui.press("enter")
        sleep(5)
        profile_directory = profile_directory.replace(' ', '\\ ')
        subprocess.run(
            f"/usr/bin/microsoft-edge-stable --flag-switches-begin --flag-switches-end "
            f"--profile-directory={profile_directory}",
            shell=True)
        sleep(.5)

        # goto messenger url
        pyautogui.write(url)
        pyautogui.press("enter")
        sleep(30)

        # # write message
        for m in message.split("<cl>"):
            pyautogui.write(m, interval=.25)
            pyautogui.press("space")
            sleep(.1)
            pyautogui.hotkey("win", "space")
            sleep(.1)
            pyautogui.press("backspace")
        sleep(.1)

        # send message
        if not is_dev:
            pyautogui.press("enter")
            sleep(5)

        # close browser
        if not is_dev:
            pyautogui.hotkey("ctrl", "w")

    def deploy_branch(self):
        if not self.is_dev:
            # check for uncommitted and untracked work
            git_status = subprocess.run(f"cd {self.working_directory} && "
                                        f"git status", shell=True, capture_output=True).stdout
            git_status = git_status.decode()
            has_uncommitted_file = re.search("Changes to be committed:", git_status)
            has_unstated_file = re.search("Changes not staged for commit:", git_status)
            temp_branch = "temp-test-test-temp"
            if has_uncommitted_file or has_unstated_file:
                # temporarily save files to temp branch
                subprocess.run(f"cd {self.working_directory} && "
                               f"git branch {temp_branch} && "
                               f"git checkout {temp_branch} && "
                               f"git add -A && "
                               f"git commit -m 'update' && "
                               f"git checkout {self.working_branch}", shell=True)
            subprocess.run(f"cd {self.working_directory} && "
                           f"git checkout {self.working_branch} && "
                           f"git merge {self.branch} -m 'merged {self.branch} with {self.working_branch}' && "
                           f"git push && "
                           f"git branch {self.branch} -D && "
                           f"./deploy.sh",
                           shell=True)
            if has_uncommitted_file or has_unstated_file:
                # restore to previous
                subprocess.run(f"cd {self.working_directory} && "
                               f"git checkout {temp_branch} && "
                               f"git reset HEAD~ && "
                               f"git checkout {self.working_branch} && "
                               f"git branch {temp_branch} -D", shell=True)

    @staticmethod
    def date(date: str) -> datetime.datetime:
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
        return date


AutomaticDeploy()
