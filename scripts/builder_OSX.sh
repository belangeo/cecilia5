#####################################
# Cecilia5 OSX standalone application
# builder script.
#
# Olivier Belanger, 2017
#####################################

export DMG_DIR="Cecilia5 5.3.2"
export DMG_NAME="Cecilia5_5.3.2.dmg"

python3.6 setup.py py2app --plist=scripts/info.plist

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
ditto --rsrc --arch x86_64 Cecilia5.app Cecilia5-x86_64.app
rm -rf Cecilia5.app
mv Cecilia5-x86_64.app Cecilia5.app

# Fixed wrong path in Info.plist
cd Cecilia5.app/Contents
awk '{gsub("@executable_path/../Frameworks/Python.framework/Versions/2.7/Python", "@executable_path/../Frameworks/Python.framework/Versions/3.6/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist
awk '{gsub("Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6", "@executable_path/../Frameworks/Python.framework/Versions/3.6/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist

cd ../../..
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
