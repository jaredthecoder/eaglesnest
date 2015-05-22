Eagle's Nest
============

Author: Jared Smith<br>
Contact: smith@utk.edu

###Demo:
---
I will have a demo up soon! Be patient!

###Overview:
---
Eagle's Nest was my experiment to learn the in's and out's of JavaScript, AngularJS, HTML, CSS, and hone my web development skills.
I also used Leaflet.js for rendering maps, D3.js for adding pings to the maps, Python's Flask to host the web server, and TextBlob and 
the NLTK to do basic sentiment analysis in Python.

I set up two UI's for the interface, which are in the v1 and v2 directories.

###Setup and Requirements:
---
It is only tested with Python 2.7.x, so if you want to use anything else then be aware there may be issues.

Steps to get up and running:
- `git clone https://github.com/jaredmichaelsmith/eaglesnest.git` -- Clone the source.
- `mkvirtualenv venv` -- Setup the virtualenv (if you're not using python virtualenv, you can do `pip install -U virtualenv`)
- `source venv/bin/activate` -- Activate the virtualenv.
- `pip install -r requirements.txt` -- Install the project dependencies.

When you are done, run `deactivate` to deactivate the virtualenv.

###Usage:
---
If you want to run version 1 of the UI, navigate to the v1 directory and run `python app.py N` to run without debug mode,
and `python app.py D` to run with debug mode. To run version 2 of the UI, navigate to the v2 directory and follow the 
same commands.
