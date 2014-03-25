from __future__ import print_function
from glob import glob
from shutil import rmtree
from cPickle import Pickler, Unpickler
from threading import Thread
from cellular_automata.creator import create_automaton
from objectives.shapes import EnergyStopCriterion
from ConfigParser import ConfigParser
import logging
import os
import time

PROJECTS = "data"

DEFAULT_CONFIG = {
        "lattice": {
            "type": "",
            "width": "",
            "height": "",
            "resolution": ""
            },
        "borders": {
            "border_top": "",
            "border_left": "",
            "border_right": "",
            "border_bottom": "",
            },
        "cells" : {
            "state" : "",
            "neighbourhood" : "",
            "rule" : "",
            },
        "network" : {
            "initial_weights" : ""
            }
        }

class Project:
    def __init__(self, project_name):
        log = logging.getLogger("PROJECT")
        self.name = project_name
        # get path to project config
        self.config_path = self.get_config_path(os.path.join(PROJECTS, project_name))
        log.debug("config_path is {}".format(self.config_path))

    def remove_section(self, section):
        """Remove whole section with all options from project configuration.
        
        If section is missing nothing happens.

        :param section: string, name of section
        :returns: None
        """
        self.config.remove_section(section)

    def remove_option(self, section, option):
        """Remove option from project configuration.
        
        If option is missing nothing happens.

        :param section: string, name of section
        :param option: string, name of option
        :returns: None
        """
        self.config.remove_option(section, option)

    def update_config(self, config):
        """Change configuration of project and saves it to
        project configure file.

        :param config: dictionary with fields to update / add
        :return: None
        """
        log = logging.getLogger("PROJECT")
        for form_key in [key for key in config.keys() if "." in key]:
            section, option = form_key.split(".")
            log.debug("{}.{} => {}".format(section, option, config[form_key]))
            if section not in self.config.sections():
                self.config.add_section(section)
            self.config.set(section, option, config[form_key])

        self.save()


    def save(self):
        """Save configuration to cfg file.
        
        :return: None
        """
        with open(self.config_path, "w") as fp:
          self.config.write(fp)

    def delete(self):
        """Delete all project files, logs, replays, ..."""
        rmtree(os.path.join(PROJECTS, self.name))

    def parse_config(self, path):
        self.config = ConfigParser()
        self.config.read(path)

    @property
    def replays(self):
        return [os.path.basename(repl) for repl in glob(os.path.join(PROJECTS, self.name, "replays", "*.replay"))]

    def replay(self, name):
        replay_file_path = os.path.join(PROJECTS, self.name, "replays", name)
        replay = None
        with open(replay_file_path, "r") as fp:
            upkl = Unpickler(fp)
            replay = upkl.load()
        return replay

    def record_replay(self):

        def start_simulation(config_path):
            log = logging.getLogger("THREAD")
            replay_file_name = os.path.join(PROJECTS, self.name, "replays", time.strftime("%Y_%m_%d_%H_%M_%S.replay"))
            log.info("creating automaton")
            automaton = create_automaton(config_path)
            log.info("Starting automaton")
            automaton.run_with_record(EnergyStopCriterion(), replay_file_name)
            log.info("Runngin finished! Replay saved in {}".format(replay_file_name))

        # create thread
        thrd = Thread(target=start_simulation, args=[self.config_path])
        #start executing
        thrd.start()

        # success
        return True

    @classmethod
    def create_project(cls, project_name):
        log = logging.getLogger("PROJECT")
        project_path = os.path.join(PROJECTS,project_name)
        # TODO: creates project, directory structure, ...
        if not os.path.exists(project_path):
            cls.create_default_config_file(os.path.join(PROJECTS,project_name,"project.cfg"))
            cls.create_project_directory(project_path)

        log.debug("Created project with name \"{}\"".format(project_name))

        project = cls(project_name)
        return cls(project_name)

    @classmethod
    def create_default_config_file(cls, config_path):
        cp = ConfigParser()

        for section in DEFAULT_CONFIG.keys():
            cp.add_section(section)
            for option in DEFAULT_CONFIG[section].keys():
                cp.set(section, option, DEFAULT_CONFIG[section][option])
        with open(config_path, "w") as fp:
            cp.write(fp)

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
        os.makedirs(os.join(path_to_project,"replays"))

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

