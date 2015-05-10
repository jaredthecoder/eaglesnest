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
from flask import render_template, url_for

# Project specific assets
from utils import *

app = Flask(__name__)

@app.route('/')
def viz():
    viz_css_url = url_for('static', filename='viz.css')
    leaflet_css_url = url_for('static', filename='leaflet.css')
    d3_js_url = url_for('static', filename='d3.min.js')
    leaflet_js_url = url_for('static', filename='leaflet.js')
    leaflet_d3_url = url_for('static', filename='leaflet-d3.min.js')
    stomp_js_url = url_for('static', filename='stomp.min.js')
    sock_js_url = url_for('static', filename='sockjs-0.3.js')

    return render_template('viz.html', viz_css=viz_css_url,
                           leaflet_css=leaflet_css_url, d3_js=d3_js_url,
                           leaflet_d3=leaflet_d3_url, leaflet_js=leaflet_js_url,
                           stomp_js=stomp_js_url, sock_js=sock_js_url)


if __name__ == '__main__':

    #parser = setup_argparser()
    #args = parser.parse_args()

    subprocess.Popen(['/usr/bin/python2.7', 'run_harvester.py'])

    app.debug = False
    app.run()
