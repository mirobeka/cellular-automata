def vonNeumannNeighborhood(cells, x, y):
  neighs = {}
  neighs["north"] = set(getCell(cells, (x,y-1)))
  neighs["east"] = set(getCell(cells, (x+1,y)))
  neighs["south"] = set(getCell(cells, (x,y+1)))
  neighs["west"] = set(getCell(cells, (x-1,y)))
  return neighs

def edieMooreNeighborhood(cells, x, y):
  neighs = {}
  neighs["north"] = set(getCell(cells, (x,y-1)))
  neighs["northeast"] = set(getCell(cells, (x+1,y-1)))
  neighs["east"] = set(getCell(cells, (x+1,y)))
  neighs["southeast"] = set(getCell(cells, (x+1,y+1)))
  neighs["south"] = set(getCell(cells, (x,y+1)))
  neighs["southwest"] = set(getCell(cells, (x-1,y+1)))
  neighs["west"] = set(getCell(cells, (x-1,y)))
  neighs["northwest"] = set(getCell(cells, (x-1,y-1)))
  return neighs

def getCell(cells, (x,y)):
  if x < 0 or x >= len(cells[0]) or y < 0 or y >= len(cells):
    return []
  else:
    return [cells[y][x]]
