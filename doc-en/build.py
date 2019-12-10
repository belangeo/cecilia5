import os

os.system("sphinx-build -a -b html ./source build")

rep = input("Do you want to upload to ajax server (y/n) ? ")
if rep == "y":
    os.system("scp -r build/* jeadum1@ajaxsoundstudio.com:/home/jeadum1/ajaxsoundstudio.com/cecilia5doc")
