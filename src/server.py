from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def front_end_resp():
    return render_template("index.html")

app.run(debug=True)