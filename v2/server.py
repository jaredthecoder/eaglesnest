###################################################################################
#
# File: server.py
# Description: Flask app server for the visualization webpage.
# Author: Jared M. Smith <jaredmichaelsmith.com>
#
###################################################################################

# Python Standard Libary assets
import argparse
import subprocess

# 3rd Party Assets
from flask import Flask
from flask import render_template

# Project specific assets
from utils import *

app = Flask(__name__)

@app.route('/')
def viz():
    return render_template('index.html')


if __name__ == '__main__':

    subprocess.Popen(['/usr/bin/python2.7', 'run_harvester.py'])

    app.debug = True
    app.run()
