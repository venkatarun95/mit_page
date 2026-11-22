#!/bin/bash

git submodule update --remote --recursive
cd networks_lecture_notes
make
cd ..
cp -r networks_lecture_notes/build networks_notes
git add networks_notes
