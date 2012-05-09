rm -rf build dist
py2applet --make-setup Cecilia5.py Resources/*
python setup.py py2app --plist=scripts/info.plist
rm -f setup.py
rm -rf build
mv dist Cecilia5_OSX

if cd Cecilia5_OSX;
then
    find . -name .svn -depth -exec rm -rf {} \
    find . -name *.pyc -depth -exec rm -f {} \
    find . -name .* -depth -exec rm -f {} \;
else
    echo "Something wrong. Cecilia5_OSX not created"
    exit;
fi

rm Cecilia5.app/Contents/Resources/Cecilia5.ico
rm Cecilia5.app/Contents/Resources/CeciliaFileIcon5.ico

ditto --rsrc --arch i386 Cecilia5.app Cecilia5-i386.app
rm -rf Cecilia5.app
mv Cecilia5-i386.app Cecilia5.app

cd ..
cp -R Cecilia5_OSX/Cecilia5.app .

# Fixed wrong path in Info.plist
cd Cecilia5.app/Contents
awk '{gsub("Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python", "@executable_path/../Frameworks/Python.framework/Versions/2.6/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist

cd ../..
tar -cjvf Cecilia5_OSX-5.0.4.tar.bz2 Cecilia5.app
rm -rf Cecilia5_OSX
rm -rf Cecilia5.app
