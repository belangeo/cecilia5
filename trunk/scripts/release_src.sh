#! /bin/sh

svn export . Cecilia5_5.0.4-src
tar -cjvf Cecilia5_5.0.4-src.tar.bz2 Cecilia5_5.0.4-src
rm -R Cecilia5_5.0.4-src
