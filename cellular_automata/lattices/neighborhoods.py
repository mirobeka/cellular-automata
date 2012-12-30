def vonNeumannNeighborhood(cells, x, y):
  neighs = {}
  neighs["north"] = getCell(cells, (x,y-1))
  neighs["east"] = getCell(cells, (x+1,y))
  neighs["south"] = getCell(cells, (x,y+1))
  neighs["west"] = getCell(cells, (x-1,y))
  return neighs

def edieMooreNeighborhood(cells, x, y):
  neighs = {}
  neighs["north"] = getCell(cells, (x,y-1))
  neighs["northeast"] = getCell(cells, (x+1,y-1))
  neighs["east"] = getCell(cells, (x+1,y))
  neighs["southeast"] = getCell(cells, (x+1,y+1))
  neighs["south"] = getCell(cells, (x,y+1))
  neighs["southwest"] = getCell(cells, (x-1,y+1))
  neighs["west"] = getCell(cells, (x-1,y))
  neighs["northwest"] = getCell(cells, (x-1,y-1))
  return neighs


def getCell(cells, (x,y)):
  if x < 0 or x >= len(cells[0]) or y < 0 or y >= len(cells):
    return None
  else:
    return cells[y][x]
