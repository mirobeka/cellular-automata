#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from evosim.evolution import evolve_weights
import time
import os


def get_project_config(project_path):
    return os.path.join(project_path, "project.cfg")

def get_project_weights_file(project_path):
    file_name = time.ctime().replace(" ","_")+".wgh"
    return os.path.join(project_path, "weights", file_name)

def main():
    # define commandline arguments
    parser = ArgumentParser()

    parser.add_argument("-p", "--project", required=True, dest="project", help="Project path")

    # Parse commandline arguments
    options = parser.parse_args()

    cfg_path = get_project_config(options.project)

    # .new_evolution returns None
    weights = evolve_weights(cfg_path)

    file_name = get_project_weights_file(options.project)

    # save evolved weights into file
    with open(file_name, "w") as fp:
        for line in weights:
            fp.write(str(line)+"\n")

if __name__ == "__main__":
    main()
