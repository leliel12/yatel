find . -iname '*.pyc' -delete;
find . -iname '*.pyo' -delete;
find . -iname '*.db' -delete;
rm -Rf Yatel.egg-info;
rm -Rf dist;
