rm -rf build dist
py2applet --make-setup Cecilia.py Resources/*
python setup.py py2app --plist=scripts/info.plist
rm -f setup.py
rm -rf build
mv dist Cecilia4_OSX

if cd Cecilia4_OSX;
then
    find . -name .svn -depth -exec rm -rf {} \
    find . -name *.pyc -depth -exec rm -f {} \
    find . -name .* -depth -exec rm -f {} \;
else
    echo "Something wrong. Cecilia_OSX not created"
    exit;
fi

rm Cecilia.app/Contents/Resources/Cecilia.ico
rm Cecilia.app/Contents/Resources/CeciliaFileIcon.ico
cd ..
#tar -cjvf Cecilia4_OSX-0.1.tar.bz2 Cecilia4_OSX
#rm -rf Cecilia4_OSX
