import os

build = True

os.system("python ..\pyinstaller\Configure.py")
os.system('python ..\pyinstaller\Makespec.py -F -c --icon=Resources\Cecilia5.ico "Cecilia5.py"')
if build:
    os.system('python ..\pyinstaller\Build.py "Cecilia5.spec"')
    os.system("svn export . Cecilia5_Win")
    os.system("copy dist\Cecilia5.exe Cecilia5_Win /Y")
    os.system("rmdir /Q /S Cecilia5_Win\scripts")
    os.remove("Cecilia5_Win/Cecilia5.py")
    os.remove("Cecilia5_Win/Resources/Cecilia5.icns")
    os.remove("Cecilia5_Win/Resources/CeciliaFileIcon5.icns")
    os.remove("Cecilia5.spec")
    os.system("rmdir /Q /S build")
    os.system("rmdir /Q /S dist")

