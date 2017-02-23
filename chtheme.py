#!/usr/bin/env python3
import os,sys,shutil

zshtheme = 'ZSH_THEME='

home = os.environ['HOME']
rcPath = os.path.join(home, ".zshrc")
bakPath = rcPath + ".bak"

def getTheme():
    theme = "Couldn't get current theme"
    with open(rcPath, 'r+') as rc:
        for l in rc.readlines():
            if l.startswith(zshtheme):
                theme = l
    return theme

def undo(): 
    try:
        shutil.copyfile(bakPath, rcPath)
        print(bakPath + " => " + rcPath)
        sys.exit(0)
    except FileNotFoundError:
        print("Can't undo because no backup found")

def changeTheme():
    with open(rcPath, 'r+') as rc:
        data = rc.read().replace(getTheme(), zshtheme + '"' + sys.argv[1] + '"')

    with open(rcPath, 'w+') as rc:
        rc.write(data)

if __name__ == "__main__":
                
    if len(sys.argv) < 2:
        print('Usage: chtheme.py [undo] <newtheme>\n')
        print(getTheme())
        sys.exit(1)
    if sys.argv[1] == "undo":
        undo()
    else:
        shutil.copyfile(rcPath, bakPath)
        changeTheme()