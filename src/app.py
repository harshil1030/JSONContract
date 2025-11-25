from flask import Flask, render_template, request
from generator import convert

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    output = ""
    if request.method == "POST":
        data = request.form["jsonInput"]
        try:
            output = convert(data)
        except Exception as ex:
            output = f"/* ERROR: {str(ex)} */"
    return render_template("index.html", result=output)

app.run(host="0.0.0.0", port=5000)
