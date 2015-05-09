from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

@app.route('/')
def viz():
    viz_css_url = url_for('static', filename='viz.css')
    return render_template('viz.html', viz_css=viz_css_url)


if __name__ == '__main__':
    app.debug = True
    app.run()
