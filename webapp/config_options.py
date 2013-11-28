def get_options():
  options = {
        "lattice" : ["SquareLattice", "DiffusionSquareLattice", "VariableSquareLattice"],
        "state" : ["BinaryState", "ColorState", "ColorTopologyState", "ChemicalState", "ChemicalInternalGrayscaleState"],
        "neighbourhood": ["VonNeumann", "Moore"],
        "rule": ["DummyRule", "GameOfLifeRule", "TestRule", "FullyInformed", "ANNColorRule"],
        "strategy": ["CMAES", "NES", "FullyInformed", "GA"],
        "objective": ["TwoBandObjective"]
      }

  # omitting "size", "resulution" and "initial weights" options
  return options
