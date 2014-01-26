from __future__ import print_function
import os
import shutil

PROJECTS = "data/"

class Project:
  def __init__(self, name):
    self.name = name

  @classmethod
  def create_project_instance(cls, project_name):
    # TODO: load all info from project directory
    return cls(project_name)

  @classmethod
  def create_project(cls, project_name):
    # TODO: creates project, directory structure, ...
    if not os.path.exists(PROJECTS+project_name):
      os.makedirs(PROJECTS+project_name)
    print("Created project  named: {}".format(project_name))
    return cls(project_name)
    
  @classmethod
  def load_project(cls, project_name):
    # check if project exists
    if os.path.exists(PROJECTS+project_name):
      # create and return instance
      return Project.create_project_instance(project_name)
    return None

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    self._name = name

