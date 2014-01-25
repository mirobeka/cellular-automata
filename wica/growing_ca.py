from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_cake import Cake
from config_options import get_options

app = Flask(__name__)
app.debug = True
Cake(app)

@app.route("/")
def index():
  return redirect(url_for("dashboard"))

@app.route("/dashboard/")
def dashboard():
  return render_template("dashboard.jinja")

@app.route("/projects/", methods=["POST"])
def create_project():
  return request.form["projectName"]

@app.route("/projects/")
def projects():
  config_options = get_options()
  return render_template("projects.jinja", config_option=config_options)

@app.route("/replays/")
def replays():
  return render_template("replays.jinja")

@app.route("/about/")
def about():
  return render_template("about.jinja")

@app.route("/documentation/")
def documentation():
  return render_template("documentation.jinja")

if __name__ == "__main__":
  app.run()
