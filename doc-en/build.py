import os

os.system("sphinx-build -a -b html ./source build")

os.system("cp -r build/* ../docs/")
os.system("rm -r build")
