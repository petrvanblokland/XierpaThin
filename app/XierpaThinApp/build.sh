#!/bin/bash
#
# Script to clean and build application.
#
rm -r build dist # Removes build files and compiled application.
python setup.py py2app --no-strip # Compiles again.
killall Portfolio # Kills runnin application.
./dist/Portfolio.app/Contents/MacOS/Portfolio # Calls application binary from the command line.
