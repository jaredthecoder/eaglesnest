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
    viz_css_url = url_for('static', filename='css/viz.css')
    viz_js_url = url_for('static', filename='js/viz.js')
    bootstrap_js_url = url_for('static', filename='js/vendor/bootstrap.min.js')
    bootstrap_css_url = url_for('static', filename='css/vendor/bootstrap.min.css')
    bootstrap_theme_css_url = url_for('static', filename='css/vendor/bootstrap-theme.css')
    jquery_js_url = url_for('static', filename='js/vendor/jquery.min.js')
    leaflet_css_url = url_for('static', filename='css/vendor/leaflet.css')
    d3_js_url = url_for('static', filename='js/vendor/d3.min.js')
    leaflet_js_url = url_for('static', filename='js/vendor/leaflet.js')
    leaflet_d3_url = url_for('static', filename='js/vendor/leaflet-d3.min.js')
    stomp_js_url = url_for('static', filename='js/vendor/stomp.min.js')
    sock_js_url = url_for('static', filename='js/vendor/sockjs-0.3.js')

    return render_template('viz.html', viz_css=viz_css_url, viz_js=viz_js_url,
                           leaflet_css=leaflet_css_url, d3_js=d3_js_url,
                           leaflet_d3_js=leaflet_d3_url, leaflet_js=leaflet_js_url,
                           stomp_js=stomp_js_url, sock_js=sock_js_url,
                           bootstrap_css=bootstrap_css_url,
                           boostrap_theme_css=bootstrap_theme_css_url,
                           bootstrap_js=bootstrap_js_url,
                           jquery_js=jquery_js_url)


if __name__ == '__main__':

    #parser = setup_argparser()
    #args = parser.parse_args()

    subprocess.Popen(['/usr/bin/python2.7', 'run_harvester.py'])

    app.debug = False
    app.run()
