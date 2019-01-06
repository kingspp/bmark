#!/usr/bin/env bash

sudo rm -rf ./dist/*
sudo python3 ./setup.py sdist
sudo python3 ./setup.py bdist_wheel
twine upload dist/*

