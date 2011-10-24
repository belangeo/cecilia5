import os

build = True

os.system("python ..\pyinstaller\Configure.py")
os.system('python ..\pyinstaller\Makespec.py -F -c --icon=Resources\Cecilia.ico "Cecilia.py"')
if build:
    os.system('python ..\pyinstaller\Build.py "Cecilia.spec"')
    os.system("svn export . Cecilia_Win")
    os.system("copy dist\Cecilia.exe Cecilia_Win /Y")
    os.system("copy scripts\README.txt Cecilia_Win /Y")
    os.system("rmdir /Q /S Cecilia_Win\scripts")
    os.remove("Cecilia_Win/Cecilia.py")
    os.remove("Cecilia_Win/Resources/Cecilia.icns")
    os.remove("Cecilia_Win/Resources/CeciliaFileIcon.icns")
    os.remove("Cecilia.spec")
    #os.remove("warnCecilia.txt")
    #os.system("rmdir /Q /S buildCecilia")
    os.system("rmdir /Q /S build")
    os.system("rmdir /Q /S dist")

