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
cd ..
#tar -cjvf Cecilia4_OSX-0.1.tar.bz2 Cecilia4_OSX
#rm -rf Cecilia5_OSX
