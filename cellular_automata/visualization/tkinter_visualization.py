from Tkinter import *
import tkColorChooser

class LatticeWidget(Canvas):
  def __init__(self, master):
    Canvas.__init__(self, master)
    self.lattice = None

  @classmethod
  def create_initialized(cls,master, lattice):
    view = cls(master)
    view.lattice = lattice
    view.config(highlightthickness=0, width=lattice.width, height=lattice.height)
    view.pack()
    view.create_canvas_items()
    return view

  # small property helper
  @property
  def cells(self):
    return self.lattice.cells.values()

  def create_canvas_items(self):
    self.lattice.canvas_item_ids = {}
    map(lambda cell: self.create_cell_item(cell), self.cells)

  def create_cell_item(self, cell):
    rgb = self.map_state_to_rgb(cell.state)
    cell.canvas_item_id = self.create_rectangle(
        cell.bounding_box,
        fill=rgb)
    self.tag_bind(cell.canvas_item_id, '<ButtonPress-1>', self.set_cell_state)
    self.lattice.canvas_item_ids[cell.canvas_item_id] = cell

  def redraw_lattice(self):
    map(lambda cell: self.redraw_cell(cell), self.cells)
    self.remove_unused_items()

  def redraw_cell(self, cell):
    # redraw position + color
    if not hasattr(cell, "canvas_item_id"):   # must create new canvas item after merge or division
      self.create_cell_item(cell)
    rgb = self.map_state_to_rgb(cell.state)
    self.coords(cell.canvas_item_id, cell.bounding_box)
    self.itemconfig(cell.canvas_item_id, fill=rgb)

  def map_state_to_rgb(self, state):
    raise NotImplementedError("method map_state_to_rgb not implemented")

  def remove_unused_items(self):
    items = [item for item in self.find_all()]
    for cell in self.cells:
      if cell.canvas_item_id in items:
        items.remove(cell.canvas_item_id)

    for item in items:
      self.delete(item)
      del self.lattice.canvas_item_ids[item]

  def set_cell_state(self, event):
    item_id = self.find_closest(event.x, event.y)[0]
    cell = self.lattice.canvas_item_ids[item_id]
    rgb,color_hex = tkColorChooser.askcolor("white", title="choose cells state")
    if rgb is None:
      return
    self.itemconfig(item_id, fill=color_hex)
    cell.state.rgb = tuple(rgb)

