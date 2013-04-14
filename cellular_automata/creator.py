import ConfigParser

# dictionary to get path of different cellular automata modules
ca_dict = {
    "lattice": "cellular_automata.lattices.equiangular",
    "state": "cellular_automata.states.base",
    "neighbourhood": "cellular_automata.lattices.neighbourhoods",
    "rule": "cellular_automata.rules.neural_rule"
}


def get_conf(file_name):
    # read configuration file
    conf = ConfigParser.ConfigParser()
    conf.read(file_name)

    # import and get all necessary components
    return dict([(path, load_module(path, cls)) for (path, cls)
                 in conf.items("simulation")])


def load_module(path, class_name):
    if path not in ca_dict:
        return class_name
    absolute_path = ca_dict[path]
    module = __import__(absolute_path, fromlist=[class_name])
    return getattr(module, class_name)


def create_automaton(conf_file):
    conf = get_conf(conf_file)
    lattice_class = conf["lattice"]
    lattice = lattice_class.create_initialized(conf)
    return lattice


def load_automaton(lattice_file):
    pass