#####################################
# Cecilia5 OSX standalone application
# builder script.
#
# Olivier Belanger, 2019
#####################################

export DMG_DIR="Cecilia5 5.3.9"
export DMG_NAME="Cecilia5_5.3.9.dmg"

python3.7 setup.py py2app --plist=scripts/info.plist

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
awk '{gsub("@executable_path/../Frameworks/Python.framework/Versions/2.7/Python", "@executable_path/../Frameworks/Python.framework/Versions/3.7/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist
awk '{gsub("Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7", "@executable_path/../Frameworks/Python.framework/Versions/3.7/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist
awk '{gsub("/usr/local/bin/python3.7", "@executable_path/../Frameworks/Python.framework/Versions/3.7/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist

install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_core.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_core.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_core.so
install_name_tool -change @loader_path/libwx_osx_cocoau_adv-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_adv-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_adv.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_adv.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_adv.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_adv.so
install_name_tool -change @loader_path/libwx_osx_cocoau_html-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_html-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_html.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_html.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_html.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_html.so
install_name_tool -change @loader_path/libwx_osx_cocoau_html-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_html-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_osx_cocoau_richtext-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_richtext-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_osx_cocoau_adv-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_adv-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_richtext.so
install_name_tool -change @loader_path/libwx_osx_cocoau_stc-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_stc-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_stc.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_stc.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_stc.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_stc.so
install_name_tool -change @loader_path/libwx_baseu_xml-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_xml-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_xml.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_xml.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_xml.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/_xml.so
install_name_tool -change @loader_path/libwx_osx_cocoau_core-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/siplib.so
install_name_tool -change @loader_path/libwx_baseu_net-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu_net-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/siplib.so
install_name_tool -change @loader_path/libwx_baseu-3.0.0.4.0.dylib @loader_path/../../../../../Frameworks/libwx_baseu-3.0.0.4.0.dylib Resources/lib/python3.7/lib-dynload/wx/siplib.so

install_name_tool -change @loader_path/libportaudio.2.dylib @loader_path/../../../../../Frameworks/libportaudio.2.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo.so
install_name_tool -change @loader_path/libportmidi.dylib @loader_path/../../../../../Frameworks/libportmidi.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo.so
install_name_tool -change @loader_path/liblo.7.dylib @loader_path/../../../../../Frameworks/liblo.7.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo.so
install_name_tool -change @loader_path/libsndfile.1.dylib @loader_path/../../../../../Frameworks/libsndfile.1.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo.so
install_name_tool -change @loader_path/libportaudio.2.dylib @loader_path/../../../../../Frameworks/libportaudio.2.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo64.so
install_name_tool -change @loader_path/libportmidi.dylib @loader_path/../../../../../Frameworks/libportmidi.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo64.so
install_name_tool -change @loader_path/liblo.7.dylib @loader_path/../../../../../Frameworks/liblo.7.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo64.so
install_name_tool -change @loader_path/libsndfile.1.dylib @loader_path/../../../../../Frameworks/libsndfile.1.dylib Resources/lib/python3.7/lib-dynload/pyo/_pyo64.so

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
