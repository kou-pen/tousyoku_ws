from flask import Flask, render_template, Response, request, send_file, url_for, redirect, flash
from flask import session as sess

from modules.camera import *

app = Flask(__name__)

@app.route("/")
def index():
    print("hello world")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5555)