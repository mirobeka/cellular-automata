from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import abort
from flask import url_for
from flask import g
from flask_cake import Cake
import json
import logging
import os
import sys

#add cellular automata into path. Must be run from root directory
sys.path.insert(0, ".")

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
    return url_for("get_project", project_name=project_name, tab="settings")

@app.route("/projects/<project_name>/replays/", methods=["POST"])
def record_replay(project_name):
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)

    if "replay" in request.form:
        project.record_replay()
        return "recording replay"

    return "wrong input data"

@app.route("/projects/<project_name>/evolve/", methods=["POST"])
def evolve_weights(project_name):
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)

    if "evolve" in request.form:
        thread_handle = project.evolve_weights()
        add_thread(thread_handle)
        return "evolve thread started"

    return "wrong input data"

@app.route("/projects/<project_name>/replay/<replay_name>/", methods=["GET"])
def get_project_replay_data(project_name, replay_name):
    log = logging.getLogger("PROJECT")
    log.debug("project_name = {} replay_name = {}".format(project_name, replay_name))

    project = Project.load_project(project_name)
    if project is None:
        return abort(404)
    json_data = convert_to_json(project.replay(replay_name))
    return json_data

@app.route("/projects/<project_name>/<tab>/", methods=["GET"])
def get_project(project_name, tab):
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)
    if tab == "settings":
        return render_template("project_settings.jinja", project=project)
    elif tab == "replays":
        return render_template("project_replays.jinja", project=project)

@app.route("/projects/<project_name>/", methods=["PUT"])
@app.route("/projects/<project_name>/settings/", methods=["PUT"])
def update_project_config(project_name):
    log = logging.getLogger("WICA")
    log.debug("trying update project {}".format(project_name))
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)

    for option in request.form.keys():
        log.debug("form[{}] = {}".format(option, request.form[option]))
    project.update_config(request.form)
    project.save()
    return url_for("get_project", project_name=project_name, tab="settings")

@app.route("/projects/<project_name>/settings/", methods=["DELETE"])
def remove_project_field(project_name):
    log = logging.getLogger("WICA")
    log.debug("trying remove {} configuration field".format(project_name))
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)

    if "option" not in request.form.keys():
        log.debug("removing section {}".format(request.form["section"]))
        project.remove_section(request.form["section"])
    else:
        log.debug("removing option {}.{}".format(request.form["section"], request.form["option"]))
        project.remove_option(request.form["section"], request.form["option"])
    project.save()
    return "successfully removed"


@app.route("/projects/<project_name>/", methods=["DELETE"])
def delete_project(project_name):
    log = logging.getLogger("WICA")
    log.debug("deleting project {}".format(project_name))
    project = Project.load_project(project_name)
    if project is None:
        return abort(404)
    project.delete()
    return url_for("get_projects")

@app.route("/projects/", methods=["GET"])
def get_projects():
    projects = Project.load_projects()
    return render_template("projects.jinja", projects=projects)

@app.route("/about/")
def about():
    return render_template("about.jinja")

@app.route("/documentation/")
def documentation():
    return render_template("documentation.jinja")

def add_thread(thread_handle):
    ctx = app.app_context()
    threads = g.get("threads", [])
    threads.append(thread_handle)
    g.threads = threads
    ctx.push()

def set_logger(level="DEBUG", outfile=None):
    """Configure logger"""
    logging.basicConfig(
        format="%(asctime)s - [%(name)s.%(levelname)s] %(message)s",
        datefmt="%I:%M:%S %p",
        filename=outfile,
        filemode="w",
        level=level.upper())

def convert_to_json(data):
    return json.dumps(data)

if __name__ == "__main__":
    set_logger()
    app.run()
    # app.run(host="0.0.0.0")
