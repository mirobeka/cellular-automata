#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from evosim.evolution import evolve_weights
import logging
import time
import os


def get_project_config(project_path):
    return os.path.join(project_path, "project.cfg")

def get_project_weights_file(project_path):
    file_name = time.ctime().replace(" ","_")+".wgh"
    return os.path.join(project_path, "weights", file_name)

def set_logger(level="DEBUG", outfile=None):
    """Configure logger"""
    logging.basicConfig(
        format="%(asctime)s - [%(name)s.%(levelname)s] %(message)s",
        datefmt="%I:%M:%S %p",
        filename=outfile,
        filemode="w",
        level=level.upper())

def main():
    set_logger()

    # define commandline arguments
    parser = ArgumentParser()
    parser.add_argument("-p", "--project", required=True, dest="project", help="Project path")

    # Parse commandline arguments
    options = parser.parse_args()

    cfg_path = get_project_config(options.project)

    # .new_evolution returns None
    save_to = get_project_weights_file(options.project)
    evolve_weights(cfg_path, save_to)

if __name__ == "__main__":
    main()
    exit(0)
