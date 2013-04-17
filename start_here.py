#!/usr/bin/env python
from __future__ import print_function
from optparse import OptionParser
from evosim.simulation import Simulation
from evosim.evolution import Evolution


def main():
    # define commandline arguments
    parser = OptionParser()
    parser.add_option("-e", "--evolution", dest="evolving",
                      help="try to evolve solution instead of simulation")
    parser.add_option("-c", "--configuration", dest="conf_file",
                      help="Specify path to configuration \
                      file defining lattice properties")
    parser.add_option("-o", "--open", dest="lattice_file",
                      help="Specify path to file previously \
                      saved with application")

    # Parse commandline arguments
    (options, arguments) = parser.parse_args()

    if options.evolving is not None and options.conf_file is not None:
        # evolve solution
        Evolution.new_evolution(options.conf_file)
    elif options.conf_file is not None:
        # if configuration file is defined
        Simulation.new_simulation(conf_file=options.conf_file)
    elif options.lattice_file is not None:
        # load previously saved lattice file
        Simulation.load_simulation(lattice_file=options.lattice_file)
    elif options.lattice_file is None:
        # nothing to do, exiting
        print("Nothing to do.")
        exit(0)

if __name__ == "__main__":
    main()
