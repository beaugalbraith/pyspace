#!/usr/bin/env python3
import os
import sys
import shutil
import psutil
import re
import subprocess

HOME = os.environ['HOME']

class Theme(object):
    theme = ""
    newTheme = ""
    bakPath = ""
    rcPath = ""

    def __init__(self, shell="zsh", destination="beau"):
        self.name = shell
        self.newTheme = destination
        self.get_theme()
        if destination == "undo":
            self.undo()

    def get_theme(self):
        if self.name == 'zsh':
            self.rcPath = os.path.join(HOME, ".zshrc")
            self.bakPath = self.rcPath + ".bak"
        elif self.name == 'bash':
            if os.path.exists(os.path.join(HOME, ".bashrc")):
                self.rcPath = os.path.join(HOME, ".bashrc")
                self.bakPath = self.rcPath + ".bak"

            else:
                self.rcPath = os.path.join(HOME, ".bash_profile")
                self.bakPath = self.rcPath + ".bak"

        with open(self.rcPath, 'r') as fd:
            for line in fd.readlines():
                match = re.search('THEME', line)
                if match != None:
                    self.theme = match.string

    def change_theme(self):
        with open(self.rcPath, 'r+') as rc:
            data = rc.read().replace(self.theme.split("=")[1], '"' + sys.argv[1] + '"' +'\n')
        with open(self.rcPath, 'w+') as rc:
            rc.write(data)
        path = subprocess.check_output(['which', self.name]).strip()
        new = os.path.split(path)
        os.execv(os.path.join(new[0], new[1]), ['-l'])

    def undo(self):
        try:
            shutil.copyfile(self.bakPath, self.rcPath)
            print(self.bakPath + " => " + self.rcPath)
            self.get_theme()
            print(self.theme)
            path = subprocess.check_output(['which', self.name]).strip()
            new = os.path.split(path)
            os.execv(os.path.join(new[0], new[1]), ['-l'])
        except FileNotFoundError:
            print("Can't undo because no backup found")


if __name__ == "__main__":
    current = Theme()
    if len(sys.argv) < 2:
        print('Usage: chtheme.py [undo] <newtheme>\n')
        print(current.theme)
        sys.exit(1)

    else:
        try:
            shell = psutil.Process(os.getppid()).name()
        except:
            shell = 'zsh'
        currentTheme = Theme(shell, sys.argv[1])
        #print(currentTheme.theme)
        #print(currentTheme.rcPath)
        shutil.copyfile(currentTheme.rcPath, currentTheme.bakPath)
        currentTheme.change_theme()
