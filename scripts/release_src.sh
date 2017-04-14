#! /bin/bash

#
# 1. change version number
# 2. Execute from cecilia5 folder : ./scripts/release_src.sh
#

version=5.3.0
replace=XXX

src_rep=Cecilia5_XXX-src
src_tar=Cecilia5_XXX-src.tar.bz2

git checkout-index -a -f --prefix=${src_rep/$replace/$version}/
tar -cjvf ${src_tar/$replace/$version} ${src_rep/$replace/$version}
rm -R ${src_rep/$replace/$version}

