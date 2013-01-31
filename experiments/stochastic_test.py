import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.rules.stochastic import StochasticRule
from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.states.base import BinaryState
from Tkinter import *
import tkColorChooser

class SquareLatticeWidget(LatticeWidget):
  def map_state_to_rgb(self, state):
    rgb = 0
    if state.alive:
      rgb = 255
    return "#{rgb:02X}{rgb:02X}{rgb:02X}".format(rgb=rgb)

  def set_cell_state(self, event):
    item_id = self.find_closest(event.x, event.y)[0]
    cell = self.lattice.canvas_item_ids[item_id]
    rgb,color_hex = tkColorChooser.askcolor("white", title="choose cells state")
    if rgb is None:
      return

    self.itemconfig(item_id, fill=color_hex)
    new_state = BinaryState.create_state()
    new_state.alive = rgb[0] == 255
    cell.state = new_state

class GUIStochasticTest(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.initialize_lattice()
    self.pack()
    self.initialize_lattice_widget()
    self.create_controls()

  def create_controls(self):
    self.step = self.create_button("next step", self.simulation_step, "left")
    self.run = self.create_run_button()
    self.save = self.create_button("save", self.save, "right")
    self.load = self.create_button("load", self.load, "right")
    
  def initialize_lattice(self):
    dimensions = (160, 160)  # dimensions are in pixels
    rule = StochasticRule()
    self.lattice = SquareLattice.create_initialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=16,  # diameter of drawn cell in pixels
        state=BinaryState,
        rule=rule)
  
  def initialize_lattice_widget(self):
    self.lattice_widget = SquareLatticeWidget.create_initialized(self, self.lattice)
  
  def load(self):
    pass

  def save(self):
    data = self.lattice.to_yaml()
    with open("data/two_band_configuration.ltc", 'w') as f:
      f.write(data)
    print("data saved")

  def simulation_step(self):
    self.lattice.next_step()
    self.lattice_widget.redraw_lattice()
    self.update()

  def simulation_loop(self):
    self.simulation_step()
    if self.running:
      self.after(100, self.simulation_loop)

  def run_simulation(self):
    self.toogle_run_pause()
    self.running = True
    self.simulation_loop()

  def pause_simulation(self):
    self.toogle_run_pause()
    self.running = False

  def toogle_run_pause(self):
    if self.run == None:
      self.pause.destroy()
      self.pause = None
      self.run = self.create_run_button()
    else:
      self.run.destroy()
      self.run = None
      self.pause = self.create_pause_button()

  def create_run_button(self):
    return self.create_button("run", self.run_simulation, "left")

  def create_pause_button(self):
    return self.create_button("pause", self.pause_simulation, "left")

  def create_button(self, text, callback, align):
    btn = Button(self)
    btn["text"] = text
    btn["command"] = callback
    btn.pack(side=align)
    return btn

if __name__ == "__main__":
  root = Tk()
  root.wm_title("Cellular Automata")
  test = GUIStochasticTest(root)
  test.mainloop()

