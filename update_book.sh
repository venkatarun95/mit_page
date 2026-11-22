#!/bin/bash

git submodule update --remote --recursive
cd networks_lecture_notes
make
