rm -rf build dist

export DMG_DIR="Cecilia5 5.2.0"
export DMG_NAME="Cecilia5_5.2.0.dmg"

if [ -f setup.py ]; then
    mv setup.py setup_back.py;
fi

py2applet --make-setup --argv-emulation=0 Cecilia5.py Resources/*
python setup.py py2app --plist=scripts/info.plist
rm -f setup.py
rm -rf build
mv dist Cecilia5_OSX

if cd Cecilia5_OSX;
then
    find . -name .git -depth -exec rm -rf {} \
    find . -name *.pyc -depth -exec rm -f {} \
    find . -name .* -depth -exec rm -f {} \;
else
    echo "Something wrong. Cecilia5_OSX not created"
    exit;
fi

rm Cecilia5.app/Contents/Resources/Cecilia5.ico
rm Cecilia5.app/Contents/Resources/CeciliaFileIcon5.ico

# keep only 64-bit arch
ditto --rsrc --arch x86_64 QLive.app QLive-x86_64.app
rm -rf QLive.app
mv QLive-x86_64.app QLive.app

ditto --rsrc --arch x86_64 Cecilia5.app Cecilia5-x86_64.app
rm -rf Cecilia5.app
mv Cecilia5-x86_64.app Cecilia5.app

cd ..
cp -R Cecilia5_OSX/Cecilia5.app .

echo "assembling DMG..."
mkdir "$DMG_DIR"
cd "$DMG_DIR"
cp -R ../Cecilia5.app .
ln -s /Applications .
cd ..

hdiutil create "$DMG_NAME" -srcfolder "$DMG_DIR"

rm -rf "$DMG_DIR"
rm -rf Cecilia5_OSX
rm -rf Cecilia5.app

if [ -f setup_back.py ]; then
    mv setup_back.py setup.py;
fi

