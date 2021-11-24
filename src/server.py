from flask import Flask, render_template, request, jsonify
from data_process import *

app = Flask(__name__)

dp = DataProcess()

@app.route("/")
def front_end_resp():
    return render_template("index.html")

@app.route("/query")
def query():
    if request.args.get("type") == "all_shops":
        return jsonify( dp.get_all_shops() )
    return "null"

app.run(debug=True)