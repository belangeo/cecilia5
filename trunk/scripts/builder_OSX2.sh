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

echo "Remove Windows .ico files"
rm Cecilia.app/Contents/Resources/Cecilia.ico
rm Cecilia.app/Contents/Resources/CeciliaFileIcon.ico

echo "Repare dynamic library links"
cd Cecilia.app/Contents/MacOS
install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.6/Python @executable_path/../Frameworks/Python.framework/Versions/2.6/Python python

cd ../Frameworks
install_name_tool -id @executable_path/../Frameworks/libfluidsynth.1.dylib libfluidsynth.1.dylib
install_name_tool -id @executable_path/../Frameworks/libportaudio.2.dylib libportaudio.2.dylib
install_name_tool -id @executable_path/../Frameworks/libportmidi.dylib libportmidi.dylib

cd CsoundLib64.framework/Versions/5.2/
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/lib_csnd.dylib lib_csnd.dylib
install_name_tool -change /Library/Frameworks/CsoundLib64.framework/Versions/5.2/CsoundLib64 @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/CsoundLib64 lib_csnd.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib lib_csnd.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib lib_csnd.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib lib_csnd.dylib

cd Resources
rm -rf Java/
rm -rf Manual/
rm -rf PD/
rm -rf Python/
rm -rf TclTk/
rm -rf csladspa/
rm -rf samples/

# install_name_tool on all dylib inside Opcodes64
cd Opcodes64/
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libambicode1.dylib libambicode1.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libambicode1.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libambicode1.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libambicode1.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libambicode1.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libampmidid.dylib libampmidid.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libampmidid.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libampmidid.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libampmidid.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libampmidid.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libbabo.dylib libbabo.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libbabo.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libbabo.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libbabo.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libbabo.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libbarmodel.dylib libbarmodel.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libbarmodel.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libbarmodel.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libbarmodel.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libbarmodel.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libchua.dylib libchua.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libchua.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libchua.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libchua.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libchua.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcompress.dylib libcompress.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcompress.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcompress.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcompress.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcompress.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcontrol.dylib libcontrol.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcontrol.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcontrol.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcontrol.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcontrol.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcrossfm.dylib libcrossfm.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcrossfm.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcrossfm.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcrossfm.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcrossfm.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcs_date.dylib libcs_date.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_date.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcs_date.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_date.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcs_date.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcs_pan2.dylib libcs_pan2.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_pan2.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcs_pan2.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_pan2.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcs_pan2.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libcs_pvs_ops.dylib libcs_pvs_ops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_pvs_ops.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libcs_pvs_ops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_pvs_ops.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libcs_pvs_ops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libdoppler.dylib libdoppler.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libdoppler.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libdoppler.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libdoppler.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libdoppler.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libeqfil.dylib libeqfil.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libeqfil.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libeqfil.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libeqfil.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libeqfil.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libfluidOpcodes.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libfluidOpcodes.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libfluidsynth.1.dylib @executable_path/../Frameworks/libfluidsynth.1.dylib libfluidOpcodes.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libftest.dylib libftest.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libftest.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libftest.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libftest.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libftest.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libgabnew.dylib libgabnew.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libgabnew.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libgabnew.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libgabnew.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libgabnew.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libgrain4.dylib libgrain4.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libgrain4.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libgrain4.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libgrain4.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libgrain4.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libharmon.dylib libharmon.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libharmon.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libharmon.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libharmon.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libharmon.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libhrtferX.dylib libhrtferX.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libhrtferX.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libhrtferX.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libhrtferX.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libhrtferX.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libhrtfnew.dylib libhrtfnew.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libhrtfnew.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libhrtfnew.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libhrtfnew.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libhrtfnew.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libimage.dylib libimage.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libimage.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libimage.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libimage.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libimage.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libjacko.dylib libjacko.dylib
install_name_tool -change /Library/Frameworks/Jackmp.framework/Versions/A/Jackmp @executable_path/../Frameworks/Jackmp.framework/Versions/A/Jackmp libjacko.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libjacko.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libjacko.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libjacko.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libjacko.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libjackTransport.dylib libjackTransport.dylib
install_name_tool -change /Library/Frameworks/Jackmp.framework/Versions/A/Jackmp @executable_path/../Frameworks/Jackmp.framework/Versions/A/Jackmp libjackTransport.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libjackTransport.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libjackTransport.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libjackTransport.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libjackTransport.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/liblinear_algebra.dylib liblinear_algebra.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib liblinear_algebra.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib liblinear_algebra.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib liblinear_algebra.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib liblinear_algebra.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libloscilx.dylib libloscilx.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libloscilx.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libloscilx.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libloscilx.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libloscilx.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libminmax.dylib libminmax.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libminmax.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libminmax.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libminmax.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libminmax.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libmixer.dylib libmixer.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmixer.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libmixer.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmixer.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libmixer.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libmodal4.dylib libmodal4.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmodal4.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libmodal4.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmodal4.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libmodal4.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libmodmatrix.dylib libmodmatrix.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmodmatrix.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libmodmatrix.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmodmatrix.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libmodmatrix.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libmp3in.dylib libmp3in.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmp3in.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libmp3in.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmp3in.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libmp3in.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libmutexops.dylib libmutexops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmutexops.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libmutexops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmutexops.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libmutexops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libosc.dylib libosc.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libosc.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libosc.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libosc.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libosc.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpartikkel.dylib libpartikkel.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpartikkel.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpartikkel.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpartikkel.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpartikkel.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libphisem.dylib libphisem.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libphisem.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libphisem.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libphisem.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libphisem.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libphysmod.dylib libphysmod.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libphysmod.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libphysmod.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libphysmod.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libphysmod.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpitch.dylib libpitch.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpitch.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpitch.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpitch.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpitch.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpmidi.dylib libpmidi.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpmidi.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpmidi.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpmidi.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpmidi.dylib
install_name_tool -change /Users/victor/src/portmidi/Release/libportmidi.dylib @executable_path/../Frameworks/libportmidi.dylib libpmidi.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libptrack.dylib libptrack.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libptrack.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libptrack.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libptrack.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libptrack.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpvlock.dylib libpvlock.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvlock.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpvlock.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvlock.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpvlock.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpvoc.dylib libpvoc.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvoc.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpvoc.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvoc.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpvoc.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpvsbuffer.dylib libpvsbuffer.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvsbuffer.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpvsbuffer.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvsbuffer.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpvsbuffer.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libpy.dylib libpy.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpy.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libpy.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpy.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libpy.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/librtcoreaudio.dylib librtcoreaudio.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtcoreaudio.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib librtcoreaudio.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtcoreaudio.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib librtcoreaudio.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/librtjack.dylib librtjack.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtjack.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib librtjack.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtjack.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib librtjack.dylib
install_name_tool -change /Library/Frameworks/Jackmp.framework/Versions/A/Jackmp @executable_path/../Frameworks/Jackmp.framework/Versions/A/Jackmp librtjack.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/librtpa.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib librtpa.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib librtpa.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libscansyn.dylib libscansyn.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libscansyn.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libscansyn.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libscansyn.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libscansyn.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libscoreline.dylib libscoreline.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libscoreline.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libscoreline.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libscoreline.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libscoreline.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libsfont.dylib libsfont.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsfont.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libsfont.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsfont.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libshape.dylib libshape.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libshape.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libshape.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libshape.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libshape.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libsignalflowgraph.dylib libsignalflowgraph.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsignalflowgraph.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libsignalflowgraph.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsignalflowgraph.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libsignalflowgraph.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libstackops.dylib libstackops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstackops.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libstackops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstackops.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libstackops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libstdopcod.dylib libstdopcod.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstdopcod.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libstdopcod.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstdopcod.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libstdopcod.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libstdutil.dylib libstdutil.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstdutil.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libstdutil.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstdutil.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libstdutil.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libsystem_call.dylib libsystem_call.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsystem_call.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libsystem_call.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsystem_call.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libsystem_call.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libtabsum.dylib libtabsum.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libtabsum.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libtabsum.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libtabsum.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libtabsum.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib64.framework/Versions/5.2/Resources/Opcodes64/libudprecv.dylib libudprecv.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libudprecv.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libudprecv.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libudprecv.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libudprecv.dylib

cd ../../../../../Jackmp.framework/
install_name_tool -id @executable_path/../Frameworks/Jackmp.framework/Versions/A/Jackmp Jackmp
cd Versions/A/
install_name_tool -id @executable_path/../Frameworks/Jackmp.framework/Versions/A/Jackmp Jackmp

cd ../../../Python.framework/Versions/2.6/
chmod 775 Python
install_name_tool -id @executable_path/../Frameworks/Python.framework/Versions/2.6/Python Python

cd ../../../../../../

sudo chown -R root:admin Cecilia.app
sudo chmod 775 Cecilia.app/

#cd ..
#tar -cjvf Cecilia4_OSX-0.1.tar.bz2 Cecilia4_OSX
#rm -rf Cecilia4_OSX
