#! /bin/bash

#
# 1. change version number
# 2. Execute from cecilia5 folder : ./scripts/release_src.sh
#

version=5.3.8
replace=XXX

doc_rep=Cecilia5_XXX-doc
doc_tar=Cecilia5_XXX-doc.tar.bz2

src_rep=Cecilia5_XXX-src
src_tar=Cecilia5_XXX-src.tar.bz2

cp -R ./doc-en/build ./doc-en/${doc_rep/$replace/$version}
cd doc-en
tar -cjvf ${doc_tar/$replace/$version} ${doc_rep/$replace/$version}
rm -R ${doc_rep/$replace/$version}
cd ..

git checkout-index -a -f --prefix=${src_rep/$replace/$version}/
tar -cjvf ${src_tar/$replace/$version} ${src_rep/$replace/$version}
rm -R ${src_rep/$replace/$version}

