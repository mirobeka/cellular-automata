from __future__ import print_function
from glob import glob
from shutil import rmtree
import os
import logging
import ConfigParser

PROJECTS = "data"

class Project:
  def __init__(self, project_name):
    log = logging.getLogger("PROJECT")
    self.name = project_name
    # get path to project config
    self.config_path = self.get_config_path(os.path.join(PROJECTS, project_name))
    log.debug("config_path is {}".format(self.config_path))


  def save(self):
    """Save configuration to cfg file """
    with open("config_path", "w") as fp:
      self.config.write(fp)

  def delete(self):
    """Delete all project files, logs, replays, ..."""
    rmtree(os.path.join(PROJECTS, self.name))

  def parse_config(self, path):
    self.config = ConfigParser.ConfigParser()
    self.config.read(path)

  @classmethod
  def create_project(cls, project_name):
    log = logging.getLogger("PROJECT")
    # TODO: creates project, directory structure, ...
    if not os.path.exists(os.path.join(PROJECTS,project_name)):
      os.makedirs(os.path.join(PROJECTS,project_name))
      open(os.path.join(PROJECTS,project_name,"project.cfg"),"w").close()

    log.debug("Created project with name \"{}\"".format(project_name))

    project = cls(project_name)
    return cls(project_name)
    
  @classmethod
  def load_projects(cls):
    # go to projects folder, load all projects
    project_names = [os.path.basename(prj) for prj in glob(os.path.join(PROJECTS, "*"))]

    # create projects instances
    projects = []
    for project_name in project_names:
      project = cls.load_project(project_name)
      projects.append(project)

    return projects

  @classmethod
  def load_project(cls, project_name):
    log = logging.getLogger("PROJECT")
    # check if project directory exists
    if os.path.exists(os.path.join(PROJECTS,project_name)):
      # create and return instance
      project = Project(project_name)
      project.parse_config(project.config_path)
      return project

    log.debug("project not found at {}".format(os.path.join(PROJECTS,project_name))) 
    return None

  @staticmethod
  def create_project_directory(path_to_project):
    os.makedirs(path_to_project)
    os.makedirs(path_to_project+"/replays")

  def get_config_path(self, directory):
    """Find config file in directory and return full path.
    
    :param directory: string, path to directory to search in
    :param: absolute path to config file found in directory or None
    """
    log = logging.getLogger("PROJECT")
    configs = glob(os.path.join(PROJECTS, self.name, "*.cfg"))
    log.debug("config files for project {}".format(self.name))
    log.debug("Found {} config files: {}".format(len(configs),configs))
    if len(configs) <= 0:
      return None
    return os.path.abspath(configs[0])

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    self._name = name

