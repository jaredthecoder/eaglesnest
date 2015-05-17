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
from flask import render_template, redirect
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms.fields import Field, TextField
from wtforms.validators import Regexp, Required

app = Flask(__name__, static_path='/static')
CsrfProtect(app)


class BasicKeywordField(Field):
    widget = TextField()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class AdvancedKeywordField(BasicKeywordField):

    def __init__(self, label='', validators=None, remove_duplicates=True,
                 **kwargs):
        super(AdvancedKeywordField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(AdvancedKeywordField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class KeywordForm(Form):
    an_regexp = re.compile("^[a-zA-Z0-9]*$")
    keywords = AdvancedKeywordField('Keywords', validators=[Required(),
                                                            Regexp(an_regexp)])


@app.route('/')
def main_view():
    return render_template('index.html', form=ff)


@app.route('filter', methods=['POST'])
def filter():
    kw_form = KeywordForm()
    if request.method == 'POST' and kw_form.validate():
        subprocess.Popen(['/usr/bin/python2.7', 'backend/run_harvester.py'] +
                         kw_form.keywords.data)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Error. Must provide 'D' or 'N' for debug or normal mode."
    elif sys.argv[1] == 'D':
        app.debug = True
    elif sys.argv[1] == 'N':
        app.debug = False

    app.run()
