import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighbourhoods import vonNeumannNeighbourhood
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.rules.base import DummyRule
from Tkinter import *

class VariableSquareLatticeWidget(LatticeWidget):
  def mapStateToRGB(self, state):
    return "#{:02X}{:02X}{:02X}".format(state[0], state[1], state[2])

class GUIVariableSquareLatticeTest(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.initializeLattice()
    self.pack()
    self.initializeLatticeWidget()
    self.createControls()

  def createControls(self):
    self.step = self.createButton("next step", self.simulationStep, "left")
    self.run = self.createRunButton()
    self.save = self.createButton("save", self.save, "right")
    self.load = self.createButton("load", self.load, "right")
    
  def initializeLattice(self):
    dimensions = (512, 512)
    rule = DummyRule()
    self.lattice = VariableSquareLattice.createInitialized(
        dimensions=dimensions,
        neighbourhoodMethod=vonNeumannNeighbourhood,
        resolution=16,
        rule=rule)
  
  def initializeLatticeWidget(self):
    self.latticeWidget = VariableSquareLatticeWidget.createInitialized(self, self.lattice)
  
  def load(self):
    pass

  def save(self):
    pass

  def simulationStep(self):
    self.lattice.nextStep()
    self.latticeWidget.redrawLattice()
    self.update()

  def simulationLoop(self):
    self.simulationStep()
    if self.running:
      self.after(0, self.simulationLoop)

  def runSimulation(self):
    self.toogleRunPause()
    self.running = True
    self.simulationLoop()

  def pauseSimulation(self):
    self.toogleRunPause()
    self.running = False

  def toogleRunPause(self):
    if self.run == None:
      self.pause.destroy()
      self.pause = None
      self.run = self.createRunButton()
    else:
      self.run.destroy()
      self.run = None
      self.pause = self.createPauseButton()

  def createRunButton(self):
    return self.createButton("run", self.runSimulation, "left")

  def createPauseButton(self):
    return self.createButton("pause", self.pauseSimulation, "left")

  def createButton(self, text, callback, align):
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

