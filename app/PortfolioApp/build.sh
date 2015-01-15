#!/bin/bash
#
# Script to clean and build application.
#
rm -r build dist # Removes build files and compiled application.
python setup.py py2app --no-strip # Compiles again.
killall WayFinding # Kills runnin application.
./dist/WayFinding.app/Contents/MacOS/WayFinding # Calls application binary from the command line.
