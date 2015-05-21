##############################################################################
#
# File: server.py
# Description: Flask app server for the visualization webpage.
# Author: Jared M. Smith <jaredmichaelsmith.com>
#
##############################################################################

# Python Standard Libary assets
import re
import sys
import subprocess

# 3rd Party Assets
from flask import Flask
from flask import render_template


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/filter', methods=['GET'])
def filter():
    if request.method == 'GET':
        subprocess.Popen(['/usr/bin/python2.7', 'backend/run_harvester.py'] +
                         .data)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Error. Must provide 'D' or 'N' for debug or normal mode."
    elif sys.argv[1] == 'D':
        app.debug = True
    elif sys.argv[1] == 'N':
        app.debug = False

    app.run()
