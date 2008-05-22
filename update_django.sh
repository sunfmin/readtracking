cd ../django
svn up
cd ../readtracking
rm -fr django
cp -r ../django/django ./
cd django
find . -name ".svn" -type d -exec rm -rf {} \;
cd ../
# rm -fr django/bin
# rm -fr django/contrib/admin
# rm -fr django/contrib/auth
# rm -fr django/contrib/databrowse
# rm -fr django/test

