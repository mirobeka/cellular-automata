import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.rules.base import DummyRule
from cellular_automata.states.base import ColorTopologyState
from Tkinter import *

class VariableSquareLatticeWidget(LatticeWidget):
  def map_state_to_rgb(self, state):
    return "#{:02X}{:02X}{:02X}".format(state.rgb[0], state.rgb[1], state.rgb[2])

class GUIVariableSquareLatticeTest(Frame):
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
    dimensions = (512, 512)
    rule = DummyRule()
    self.lattice = VariableSquareLattice.create_initialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=16,
        state=ColorTopologyState,
        rule=rule)
  
  def initialize_lattice_widget(self):
    self.lattice_widget = VariableSquareLatticeWidget.create_initialized(self, self.lattice)
  
  def load(self):
    pass

  def save(self):
    pass

  def simulation_step(self):
    self.lattice.next_step()
    self.lattice_widget.redraw_lattice()
    self.update()

  def simulation_loop(self):
    self.simulation_step()
    if self.running:
      self.after(0, self.simulation_loop)

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
  test = GUIVariableSquareLatticeTest(root)
  test.mainloop()

