###################################################################################
#
# File: server.py
# Description: Flask app server for the visualization webpage.
# Author: Jared M. Smith <jaredmichaelsmith.com>
#
###################################################################################

# Python Standard Libary assets
import sys
import argparse
import subprocess

# 3rd Party Assets
from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)


@app.route('/')
def viz():
    return render_template('index.html')


if __name__ == '__main__':


    if not len(sys.argv) == 2:
        print "usage: python app.py <debug[d/n]>"
        sys.exit(1)
    elif sys.argv[1] == "D":
        app.debug = True
    elif sys.argv[1] == "N":
        app.debug = False
    else:
        print "usage: python app.py <debug[d/n]>"
        sys.exit(1)

    subprocess.Popen(['/usr/bin/python2.7', 'backend/run_harvester.py'])

    app.run()
