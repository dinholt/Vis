from flask import Flask, render_template, request, jsonify
from flask.helpers import send_file
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
    if request.args.get("type") == "shop_detail":
        poiid = request.args.get("poiid")
        return jsonify( dp.get_shop_detail(poiid) )
    return "null"

@app.route("/wordcloud")
def wordcloud():
    if request.args.get("type") == "shop":
        pass
    if request.args.get("type") == "user":
        pass
    return send_file( wordcloudgen(), mimetype='image/png', as_attachment=False )

app.run(debug=True)