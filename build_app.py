import shutil, os, glob, msvcrt
from datetime import datetime as dt
from subprocess import DEVNULL, STDOUT, check_call

cwd = os.getcwd() # current working dir
ver = ['[0]',' 0 ',' 0 ']

# --------------------------------------------------------

## clean up existing files
def cleanup(isInitial = False):
    if os.path.exists(cwd + "\\build"):
        shutil.rmtree(cwd + "\\build")

    if os.path.exists(cwd + "\\dist"):
        shutil.rmtree(cwd + "\\dist")

    if not os.path.exists(cwd + "\\releases"):
        os.makedirs(cwd + "\\releases")

    for f in glob.glob("*.spec"):
        os.remove(f)

    if isInitial:
        for f in glob.glob("v*.zip"):
            os.remove(f)

## read the most recent version created
def read_version():
    global ver

    try:
        with open('versions.log', 'r') as log_file:
            latest = log_file.readlines()[-1]
            latest = latest.split("v")[1]
            latest = latest.split(".")

            ver = [
                "[" + str(latest[0]) + "]",
                " " + str(latest[1]) + " ",
                " " + str(latest[2]) + " ",
            ]

    except Exception as e:
        print(e)

# --------------------------------------------------------

done = False
cursor = 0
kb = None

read_version()

while not done:
    os.system('cls')
    print("Use 'a' and 'd' keys to navigate, 'w' and 's' to change version, 'e' to confirm.\napp version: v" + ver[0] + "." + ver[1] + "." + ver[2])
    kb = msvcrt.getch()

    for i in range(len(ver)):
        ver[i] = ver[i].replace("]"," ").replace("["," ")

    try: kb = kb.decode(encoding='utf-8')
    except: pass

    if kb == "a":
        cursor = (cursor - 1) % 3
    elif kb == "d":
        cursor = (cursor + 1) % 3
    elif kb == "w":
        ver[cursor] = " " + str(int(ver[cursor]) + 1) + " "
    elif kb == "s" and int(ver[cursor]) > 0:
        ver[cursor] = " " + str(int(ver[cursor]) - 1) + " "
    elif kb == "e":
        for i in range(len(ver)):
            ver[i] = str(int(ver[i].replace("]","").replace("[","")))
        done = True

    if done == False:
        ver[cursor] = "[" + ver[cursor].replace(" ", "") + "]"

cleanup(isInitial = True)

## build the exe from py files
os.system("cls")
print("building exe...")
check_call(['python', '-m', 'PyInstaller', 'main.py', '--noconsole', '--onefile', '-w', '--icon=assets\\logo.ico', '--name=RetAG'], stdout=DEVNULL, stderr=STDOUT)
print("done")

## after the exe is built, copy over the assets folder
try: shutil.copytree(cwd + "\\assets\\", cwd + "\\dist\\assets\\")
except: print("could not copy assets folder")

## zip the contents of the dist folder
try: shutil.make_archive("v" + (".").join(ver), 'zip', cwd + "\\dist")
except Exception as e: print("could not zip dist folder: ", e)

## move the created zip file into the releases folder
try:
    for file in glob.glob(cwd + '\\v*.zip'):
        shutil.move(file, cwd + "\\releases")
except Exception as e: print("could not move zip file: ", e)

## final cleanup of temporary files
print("cleaning up...")
cleanup(isInitial = False)
print("done")

## write the newest build to the log
with open('versions.log', 'a') as log_file:
    log_file.write("\n[" + dt.now().strftime("%d/%m/%Y, %H:%M:%I" + "]\t") + "v" + (".").join(ver))

output_dir = (cwd + "\\releases")
os.startfile(output_dir)
