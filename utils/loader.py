import ConfigParser

# dictionary to get path of different cellular automata modules
ca_dict = {
    "type": "cellular_automata.lattices.equiangular",
    "state": "cellular_automata.states.base",
    "neighbourhood": "cellular_automata.lattices.neighbourhoods",
    "rule": "cellular_automata.rules.neural_rule",
    "objective": "objectives.shapes",
    "strategy": "methods"
}


def load_module(path, class_name):
    """Imports class from python module and returns it

    :param path: module name
    :param class_name: class name that should be imported
    :return: class that we asked for
    """
    if path not in ca_dict:
        # small hack. This way, what's importable imports
        # and other string values are returned back
        return class_name
    absolute_path = ca_dict[path]
    module = __import__(absolute_path, fromlist=[class_name])
    return getattr(module, class_name)


def module_loader(file_name):
    # read configuration file
    conf = ConfigParser.ConfigParser()
    conf.read(file_name)

    conf_with_imports = import_importable(conf)
    return conf_with_imports


def import_importable(conf):
    # import and get all necessary components
    transformed_conf = dict()
    for section in conf.sections():
      transformed_conf[section] = dict([(path, load_module(path, cls)) for (path, cls) in conf.items(section)])
    return transformed_conf
