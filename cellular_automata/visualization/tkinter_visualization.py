from Tkinter import *
import tkColorChooser

class LatticeWidget(Canvas):
  def __init__(self, master):
    Canvas.__init__(self, master)
    self.lattice = None

  @classmethod
  def createInitialized(cls,master, lattice):
    view = cls(master)
    view.lattice = lattice
    view.config(width=lattice.width, height=lattice.height)
    view.pack()
    view.createCanvasItems()
    return view

  # small property helper
  @property
  def cells(self):
    return self.lattice.cells.values()

  def createCanvasItems(self):
    self.lattice.canvasItemIds = {}
    map(lambda cell: self.createCellItem(cell), self.cells)

  def createCellItem(self, cell):
    rgb = self.mapStateToRGB(cell.state)
    box = (
        cell.x-cell.radius,
        cell.y-cell.radius,
        cell.x+cell.radius,
        cell.y+cell.radius
        )
    cell.canvasItemId = self.create_rectangle(
        box,
        fill=rgb)
    self.tag_bind(cell.canvasItemId, '<ButtonPress-1>', self.setCellState)
    self.lattice.canvasItemIds[cell.canvasItemId] = cell

  def redrawLattice(self):
    map(lambda cell: self.redrawCell(cell), self.cells)
    self.removeUnusedItems()

  def redrawCell(self, cell):
    # redraw position + color
    if not hasattr(cell, "canvasItemId"):   # must create new canvas item after merge or division
      self.createCellItem(cell)
    rgb = self.mapStateToRGB(cell.state)
    box = (
        cell.x-cell.radius,
        cell.y-cell.radius,
        cell.x+cell.radius,
        cell.y+cell.radius
        )
    self.coords(cell.canvasItemId, box)
    self.itemconfig(cell.canvasItemId, fill=rgb)

  def mapStateToRGB(self, state):
    raise NotImplementedError("method mapStateToRGB not implemented")

  def removeUnusedItems(self):
    items = [item for item in self.find_all()]
    for cell in self.cells:
      if cell.canvasItemId in items:
        items.remove(cell.canvasItemId)

    for item in items:
      self.delete(item)
      del self.lattice.canvasItemIds[item]

  def setCellState(self, event):
    itemId = self.find_closest(event.x, event.y)[0]
    cell = self.lattice.canvasItemIds[itemId]
    rgb,colorHex = tkColorChooser.askcolor("red", title="choose cells state")
    self.itemconfig(itemId, fill=colorHex)
    cell.state = [x for x in rgb] + [0,0]

