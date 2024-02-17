import os, glob, shutil
from datetime import datetime as dt
from subprocess import DEVNULL, STDOUT, check_call

## read the most recent version created
def get_version(ver):
    try:
        with open('versions.log', 'r') as log_file:
            latest = log_file.readlines()[-1]
            latest = latest.split("v")[1]
            latest = latest.split(".")

            ver = [
                str(latest[0]),
                str(latest[1]),
                str(latest[2]),
            ]

            ver[2] = "[" + ver[2] + "]"

            return ver

    except Exception as e:
        print(e)


## remove spaces and brackets
def unformat(formatted):
    return formatted.replace("]","").replace("[","").replace(" ","")


## clean up existing files
def cleanup(cwd, isInitial = False):
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


##
def install_dependencies():
    os.system('cls')
    for library in ['pyinstaller', 'python-dateutil', 'python-docx', 'docx2pdf', 'customtkinter', 'CTkTable', 'CTkMessagebox']:
        print("installing dependency: " + library)
        check_call(['pip', 'install', library], stdout=DEVNULL, stderr=STDOUT)
    print("done")


##
def build_exe(cwd, ver):
    cleanup(cwd, isInitial = True)

    ## build the exe from py files
    os.system("cls")
    print("building exe...")
    check_call(['python', '-m', 'PyInstaller', 'main.py', '--noconsole', '--onefile', '-w', '--icon=assets\\logo.ico', '--name=RetAG'], stdout=DEVNULL, stderr=STDOUT)
    print("done")

    ## after the exe is built, copy over the assets folder
    try: 
        shutil.copytree(cwd + "\\assets\\", cwd + "\\dist\\assets\\")
    except: 
        print("could not copy assets folder")

    ## zip the contents of the dist folder
    try: 
        shutil.make_archive("v" + (".").join(ver), 'zip', cwd + "\\dist")
    except Exception as e: 
        print("could not zip dist folder: ", e)

    ## move the created zip file into the releases folder
    try:
        for file in glob.glob(cwd + '\\v*.zip'):
            shutil.move(file, cwd + "\\releases")
    except Exception as e: print("could not move zip file: ", e)

    ## final cleanup of temporary files
    print("cleaning up...")
    cleanup(cwd, isInitial = False)
    print("done")

    ## write the newest build to the log
    with open('versions.log', 'a') as log_file:
        log_file.write("\n[" + dt.now().strftime("%d/%m/%Y, %H:%M:%I" + "]\t") + "v" + (".").join(ver))

    output_dir = (cwd + "\\releases")
    os.startfile(output_dir)