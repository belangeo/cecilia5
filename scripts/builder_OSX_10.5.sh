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
install_name_tool -id @executable_path/../Frameworks/libpng12.0.dylib libpng12.0.dylib

cd CsoundLib.framework/Versions/5.2/
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/lib_csnd.dylib lib_csnd.dylib
install_name_tool -change /Library/Frameworks/CsoundLib.framework/Versions/5.2/CsoundLib @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/CsoundLib lib_csnd.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib lib_csnd.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib lib_csnd.dylib
install_name_tool -change /usr/local/lib/libfltk.1.1.dylib @executable_path/../Frameworks/libfltk.1.1.dylib lib_csnd.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib lib_csnd.dylib

cd Resources
rm -rf Java/
rm -rf Manual/
rm -rf PD/
rm -rf TclTk/
rm -rf csladspa/
rm -rf samples/

# install_name_tool on all dylib inside Opcodes64
cd Opcodes/
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libambicode1.dylib libambicode1.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libambicode1.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libambicode1.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libambicode1.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libampmidid.dylib libampmidid.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libampmidid.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libampmidid.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libampmidid.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libbabo.dylib libbabo.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libbabo.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libbabo.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libbabo.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libbarmodel.dylib libbarmodel.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libbarmodel.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libbarmodel.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libbarmodel.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libchua.dylib libchua.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libchua.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libchua.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libchua.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcompress.dylib libcompress.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcompress.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcompress.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcompress.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcontrol.dylib libcontrol.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcontrol.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcontrol.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcontrol.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcrossfm.dylib libcrossfm.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcrossfm.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcrossfm.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcrossfm.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcs_date.dylib libcs_date.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_date.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcs_date.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_date.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcs_pan2.dylib libcs_pan2.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_pan2.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcs_pan2.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_pan2.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libcs_pvs_ops.dylib libcs_pvs_ops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libcs_pvs_ops.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libcs_pvs_ops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libcs_pvs_ops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libdoppler.dylib libdoppler.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libdoppler.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libdoppler.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libdoppler.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libeqfil.dylib libeqfil.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libeqfil.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libeqfil.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libeqfil.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libfluidOpcodes.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libfluidOpcodes.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libfluidOpcodes.dylib
install_name_tool -change /usr/local/lib/libfluidsynth.1.dylib @executable_path/../Frameworks/libfluidsynth.1.dylib libfluidOpcodes.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libftest.dylib libftest.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libftest.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libftest.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libftest.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libgabnew.dylib libgabnew.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libgabnew.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libgabnew.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libgabnew.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libgrain4.dylib libgrain4.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libgrain4.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libgrain4.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libgrain4.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libharmon.dylib libharmon.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libharmon.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libharmon.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libharmon.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libhrtferX.dylib libhrtferX.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libhrtferX.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libhrtferX.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libhrtferX.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libhrtfnew.dylib libhrtfnew.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libhrtfnew.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libhrtfnew.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libhrtfnew.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libimage.dylib libimage.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libimage.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libimage.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libimage.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libimage.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libjackTransport.dylib libjackTransport.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libjackTransport.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libjackTransport.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libjackTransport.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libloscilx.dylib libloscilx.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libloscilx.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libloscilx.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libloscilx.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libminmax.dylib libminmax.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libminmax.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libminmax.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libminmax.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libmixer.dylib libmixer.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmixer.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libmixer.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmixer.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libmodal4.dylib libmodal4.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmodal4.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libmodal4.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmodal4.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libmodmatrix.dylib libmodmatrix.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmodmatrix.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libmodmatrix.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmodmatrix.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libmp3in.dylib libmp3in.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmp3in.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libmp3in.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmp3in.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libmutexops.dylib libmutexops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libmutexops.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libmutexops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libmutexops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libosc.dylib libosc.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libosc.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libosc.dylib
install_name_tool -change /usr/local/lib/liblo.0.dylib @executable_path/../Frameworks/liblo.0.dylib libosc.dylib
install_name_tool -change /usr/local/lib/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib libosc.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpartikkel.dylib libpartikkel.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpartikkel.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpartikkel.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpartikkel.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libphisem.dylib libphisem.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libphisem.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libphisem.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libphisem.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libphysmod.dylib libphysmod.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libphysmod.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libphysmod.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libphysmod.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpitch.dylib libpitch.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpitch.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpitch.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpitch.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpmidi.dylib libpmidi.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpmidi.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpmidi.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpmidi.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libptrack.dylib libptrack.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libptrack.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libptrack.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libptrack.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpvlock.dylib libpvlock.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvlock.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpvlock.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvlock.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpvoc.dylib libpvoc.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvoc.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpvoc.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvoc.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpvsbuffer.dylib libpvsbuffer.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpvsbuffer.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpvsbuffer.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpvsbuffer.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libpy.dylib libpy.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libpy.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libpy.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libpy.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/librtcoreaudio.dylib librtcoreaudio.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtcoreaudio.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib librtcoreaudio.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtcoreaudio.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/librtjack.dylib librtjack.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtjack.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib librtjack.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtjack.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/librtpa.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib librtpa.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib librtpa.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib librtpa.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libscansyn.dylib libscansyn.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libscansyn.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libscansyn.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libscansyn.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libscoreline.dylib libscoreline.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libscoreline.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libscoreline.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libscoreline.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libsfont.dylib libsfont.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsfont.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libsfont.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsfont.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libshape.dylib libshape.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libshape.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libshape.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libshape.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libsignalflowgraph.dylib libsignalflowgraph.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsignalflowgraph.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libsignalflowgraph.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsignalflowgraph.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libstackops.dylib libstackops.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstackops.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libstackops.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstackops.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libstdopcod.dylib libstdopcod.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstdopcod.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libstdopcod.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstdopcod.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libstdutil.dylib libstdutil.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libstdutil.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libstdutil.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libstdutil.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libsystem_call.dylib libsystem_call.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libsystem_call.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libsystem_call.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libsystem_call.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libtabsum.dylib libtabsum.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libtabsum.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libtabsum.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libtabsum.dylib
install_name_tool -id @executable_path/../Frameworks/CsoundLib.framework/Versions/5.2/Resources/Opcodes/libudprecv.dylib libudprecv.dylib
install_name_tool -change /usr/local/lib/libsndfile.1.dylib @executable_path/../Frameworks/libsndfile.1.dylib libudprecv.dylib
install_name_tool -change /usr/local/lib/libportaudio.2.dylib @executable_path/../Frameworks/libportaudio.2.dylib libudprecv.dylib
install_name_tool -change libmpadec.dylib @executable_path/../Frameworks/libmpadec.dylib libudprecv.dylib

cd ../../../../../Python.framework/Versions/2.6/
chmod 775 Python
install_name_tool -id @executable_path/../Frameworks/Python.framework/Versions/2.6/Python Python

cd ../../../../../../

sudo chown -R root:admin Cecilia.app
sudo chmod 775 Cecilia.app/

#cd ..
#tar -cjvf Cecilia4_OSX-0.1.tar.bz2 Cecilia4_OSX
#rm -rf Cecilia4_OSX
