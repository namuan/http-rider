#!/bin/bash

for i in `ls resources/ui/*.ui`; do FNAME=`basename $i ".ui"`; ./venv/bin/pyuic5 $i > "httprider/generated/$FNAME.py"; done

./venv/bin/pyrcc5 -compress 9 -o httprider/resources_rc.py httprider/resources.qrc