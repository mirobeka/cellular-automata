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

def save_result(file_name, result):
    print("saving {}".format(file_name))
    with open(file_name, "w") as fp:
        fp.write(str(result["error"])+"\n")
        fp.write("["+ ",".join(map(str,result["weights"])) +"]\n")
        fp.write(str(result["pattern"])+"\n")
        # fp.write(str(result["generations"])+"\n")
        fp.write(str(result["lattice_age"])+"\n")
        fp.write(str(result["average_lattice_age"])+"\n")
        fp.write("\n")
        fp.write("progress:\n")
        for (error, weights) in result["progress"]:
            fp.write(str(error)+":")
            fp.write("["+ ",".join(map(str,result["weights"])) +"]\n")
        fp.flush()

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
    result = evolve_weights(cfg_path)

    file_name = get_project_weights_file(options.project)

    # save evolved weights into file
    try:
        save_result(file_name, result)
    except:
        print("exception during save_result")
        print(result)

if __name__ == "__main__":
    main()
