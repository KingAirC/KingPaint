python setup.py sdist build
python setup.py bdist_wheel --universal
python setup.py sdist upload
python setup.py bdist_wheel upload
sudo rm -rf ./build/ ./dist/ ./src/KingPaint.egg-info/
