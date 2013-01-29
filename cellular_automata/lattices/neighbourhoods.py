class Neighbourhood(object):
  @staticmethod
  def gather_neighbours(cells, resolution, x, y):
    raise NotImplementedError("method gather_neighbours not implemented")

class VonNeumann(Neighbourhood):
  @staticmethod
  def gather_neighbours(cells, resolution, x, y):
    neighs = {}
    neighs["north"] = set(getCell(cells, (x,y-resolution)))
    neighs["east"] = set(getCell(cells, (x+resolution,y)))
    neighs["south"] = set(getCell(cells, (x,y+resolution)))
    neighs["west"] = set(getCell(cells, (x-resolution,y)))
    return neighs

  @staticmethod
  def create_empty():
    neighs = {}
    neighs["north"] = set()
    neighs["east"] = set()
    neighs["south"] = set()
    neighs["west"] = set()
    return neighs

class EdieMoore(Neighbourhood):
  @staticmethod
  def gather_neighbours(cells, resolution, x, y):
    neighs = {}
    neighs["north"] = set(getCell(cells, (x,y-resolution)))
    neighs["northeast"] = set(getCell(cells, (x+resolution,y-resolution)))
    neighs["east"] = set(getCell(cells, (x+resolution,y)))
    neighs["southeast"] = set(getCell(cells, (x+resolution,y+resolution)))
    neighs["south"] = set(getCell(cells, (x,y+resolution)))
    neighs["southwest"] = set(getCell(cells, (x-resolution,y+resolution)))
    neighs["west"] = set(getCell(cells, (x-resolution,y)))
    neighs["northwest"] = set(getCell(cells, (x-resolution,y-resolution)))
    return neighs

  @staticmethod
  def create_empty():
    neighs = {}
    neighs["north"] = set()
    neighs["east"] = set()
    neighs["south"] = set()
    neighs["west"] = set()
    neighs["northeast"] = set()
    neighs["southeast"] = set()
    neighs["southwest"] = set()
    neighs["northwest"] = set()
    return neighs

def getCell(cells, pos):
  if pos in cells:
    return [cells[pos]]
  else:
    return []
