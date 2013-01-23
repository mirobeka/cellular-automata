def vonNeumannNeighborhood(cells, resolution, x, y):
  neighs = {}
  neighs["north"] = set(getCell(cells, (x,y-resolution)))
  neighs["east"] = set(getCell(cells, (x+resolution,y)))
  neighs["south"] = set(getCell(cells, (x,y+resolution)))
  neighs["west"] = set(getCell(cells, (x-resolution,y)))
  return neighs

def edieMooreNeighborhood(cells, resolution, x, y):
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

def getCell(cells, pos):
  if pos in cells:
    return [cells[pos]]
  else:
    return []
