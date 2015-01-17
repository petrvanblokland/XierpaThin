#!/bin/bash
#
# Script to clean and build application.
#
rm -r build dist # Removes build files and compiled application.
python setup.py py2app --no-strip # Compiles again.
killall XierpaThin # Kills runnin application.
./dist/XierpaThin.app/Contents/MacOS/XierpaThin # Calls application binary from the command line.
