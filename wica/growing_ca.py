from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import abort
from flask import url_for
from flask_cake import Cake
from config_options import get_options
import os
import sys

#add cellular automata into path
sys.path.insert(0, "..")

from projects.project import Project

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
  project_name = request.form["projectName"]

  # TODO: check if project with this name already exists

  # creates project
  project = Project.create_project(project_name)
  return url_for("get_project", project_name=project_name)

@app.route("/projects/<project_name>/", methods=["GET"])
def get_project(project_name):
  project = Project.load_project(project_name)
  if project is None:
    return abort(404)
  return render_template("project.jinja", project=project)

@app.route("/projects/", methods=["GET"])
def get_projects():
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
