find . -iname '*.pyc' -delete;
find . -iname '*.pyo' -delete;
find . -iname '*.db' -delete;
find . -iname '*.orig' -delete;
rm -Rf Yatel.egg-info;
rm -Rf dist;
