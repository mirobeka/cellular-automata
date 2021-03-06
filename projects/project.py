from __future__ import print_function
from cellular_automata.creator import create_automaton
from objectives.shapes import EnergyCriterion
from objectives.shapes import AgeCriterion
from utils.loader import module_loader
from cPickle import Pickler, Unpickler
from ConfigParser import ConfigParser
from threading import Thread
from shutil import rmtree
from glob import glob
import logging
import os
import time

log = logging.getLogger("PROJECT")

PROJECTS = "data"

DEFAULT_CONFIG = {
        "lattice": {
            "type": "SquareLattice",
            "width": "400",
            "height": "400",
            "resolution": "20"
            },
        "borders": {
            "border_top": "[[-1]]*20",
            "border_left": "[[1]]*20",
            "border_right": "[[-1]]*20",
            "border_bottom": "[[1]]*20",
            "border_top_northwest":"[[-1]]*20",
            "border_top_northeast":"[[-1]]*20",
            "border_left_northwest":"[[1]]*20",
            "border_left_southwest":"[[1]]*20",
            "border_right_northeast":"[[-1]]*20",
            "border_right_southeast":"[[-1]]*20",
            "border_bottom_southwest":"[[1]]*20",
            "border_bottom_southeast":"[[1]]*20"
            },
        "cells" : {
            "state" : "GrayscaleState",
            "neighbourhood" : "VonNeumann",
            "rule" : "FeedForwardNetwork",
            },
        "replay" : {
            "weights" : "",
            "max_time" : "512"
            },
        "stopcriterion" : {
            "criterion" : "EnergyCriterion"
            },
        "evolution" :{
            "objective" : "PatternObjective",
            "strategy" : "cmaes",
            "pattern" : "",
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

    def get_error_from_wgh(self, file_name):
        with open(file_name, "r") as fp:
            error = float(fp.readline().strip())
        log.debug("loaded error: {} -> {}".format(file_name, error))
        return error

    @property
    def weights(self):
        weights = [(self.get_error_from_wgh(wght),os.path.basename(wght)) for wght in glob(os.path.join(PROJECTS, self.name, "weights", "*.wgh"))]
        log.debug(weights)
        return weights

    def weight(self, name):
        weight_file_path = os.path.join(PROJECTS, self.name, "weights", name)
        weight = {}
        with open(weight_file_path, "r") as fp:
            weight["error"] = float(fp.readline().strip())
            weight["weights"] = eval(fp.readline().strip())
            weight["pattern"] = fp.readline().strip()
            weight["generations"] = int(fp.readline().strip())
            weight["lattice_age"] = int(fp.readline().strip())
            weight["average_lattice_age"] = float(fp.readline().strip())
            weight["progress"] = []
            fp.readline() # empty line
            assert fp.readline() == "progress:\n"
            for line in fp.readlines():
                i, w = line.split(":")
                gen, err = i.split(" ")
                gen = int(gen)
                err = float(err)
                w = eval(w)
                weight["progress"].append([gen, err, w])


        modules = module_loader(self.config_path)
        rule_instance = modules["cells"]["rule"]()
        rule_instance.set_weights(weight["weights"])

        weight["layer1"] = rule_instance.theta1.tolist()
        weight["layer2"] = rule_instance.theta2.tolist()
        weight["neigh"] = self.config.get("cells", "neighbourhood").lower()
        return weight

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

        def start_simulation(config_path, max_age):
            log = logging.getLogger("THREAD")
            replay_file_name = os.path.join(PROJECTS, self.name, "replays", time.strftime("%Y_%m_%d_%H_%M_%S.replay"))
            automaton = create_automaton(config_path)
            log.debug("automaton created")
            automaton.run_with_record(AgeCriterion(max_age=max_age), replay_file_name)
            log.info("Runngin finished! Replay saved in {}".format(replay_file_name))

        max_age = 800
        if "max_time" in self.config.options("replay"):
            max_age = self.config.getint("replay", "max_time")

        # create thread
        thrd = Thread(target=start_simulation, args=[self.config_path, max_age])
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
            cls.create_project_directory(project_path)
            cls.create_default_config_file(os.path.join(PROJECTS,project_name,"project.cfg"))

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
        os.makedirs(os.path.join(path_to_project,"replays"))
        os.makedirs(os.path.join(path_to_project,"patterns"))
        os.makedirs(os.path.join(path_to_project,"weights"))

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

