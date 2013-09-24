find . -iname '*.pyc' -delete;
find . -iname '*.pyo' -delete;
find . -iname '*.db' -delete;
find . -iname '*.orig' -delete;
rm -Rf Yatel.egg-info;
rm -Rf Sphinx_PyPI_upload*.egg;
rm -Rf dist;
