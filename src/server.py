from flask import Flask, render_template
from data_process import *

app = Flask(__name__)

dp = DataProcess()

@app.route("/")
def front_end_resp():
    return render_template("index.html")

@app.route("/query")
def query():
    return "null"

app.run(debug=True)