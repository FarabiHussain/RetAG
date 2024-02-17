import shutil, os, glob, msvcrt
from datetime import datetime as dt
from subprocess import DEVNULL, STDOUT, check_call
from build_app_utils import *

cwd = os.getcwd()
ver = ['0', '0', '0']
kb = None
cur = 2


ver = get_version(ver)
latest_build = unformat(ver[0]) + "." + unformat(ver[1]) + "." + unformat(ver[2])

# increment the patch number for the current build
ver[2] = "[" + str(int(unformat(ver[2])) + 1) + "]"

# install dependencies needed to build the file
install_dependencies()

while True:
    os.system('cls')

    print(
        ("Use 'a' and 'd' keys to navigate, 'w' and 's' to change version, 'e' to confirm. 'q' to quit.\n") +
        ("Latest build found: v" + latest_build + "\n") +
        ("New build version: v" + ver[0] + "." + ver[1] + "." + ver[2])
    )

    kb = msvcrt.getch()

    for i in range(len(ver)):
        ver[i] = unformat(ver[i])

    try: kb = kb.decode(encoding='utf-8')
    except: pass

    if kb == "a":
        cur = (cur - 1) % 3
    elif kb == "d":
        cur = (cur + 1) % 3
    elif kb == "w":
        ver[cur] = str(int(ver[cur]) + 1)
    elif kb == "s" and int(ver[cur]) > 0:
        ver[cur] = str(int(ver[cur]) - 1)
    elif kb == "e":
        for i in range(len(ver)):
            ver[i] = unformat(ver[i])
        build_exe(cwd, ver)
        break
    elif kb == "q":
        break

    ver[cur] = "[" + ver[cur].replace(" ", "") + "]"


