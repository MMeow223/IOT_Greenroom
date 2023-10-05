from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/greenroom-detail')
def page_greenroom_detail():
    return render_template('greenroom-detail.html')
