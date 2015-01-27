#!/bin/bash
#
# Script to clean and build application.
#
python setup.py py2app -A # Compile with aliased dependencies
killall XierpaThin # Kills running application.
./dist/XierpaThin.app/Contents/MacOS/XierpaThin # Calls application binary from the command line.
