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
    self.NEXT = Button(self)
    self.NEXT["text"] = "Next step"
    self.NEXT["command"] =  self.simulationStep
    self.NEXT.pack()
    
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
  
  def simulationStep(self):
    self.lattice.nextStep()
    self.latticeWidget.redrawLattice()

if __name__ == "__main__":
  root = Tk()
  root.wm_title("Cellular Automata")
  test = GUIVariableSquareLatticeTest(root)
  test.mainloop()

