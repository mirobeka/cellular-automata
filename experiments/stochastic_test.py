import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.rules.stochastic import StochasticRule
from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import vonNeumannNeighbourhood
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from Tkinter import *
import tkColorChooser

class SquareLatticeWidget(LatticeWidget):
  def mapStateToRGB(self, state):
    rgb = 0
    if state[0] == 1:
      rgb = 255
    return "#{rgb:02X}{rgb:02X}{rgb:02X}".format(rgb=rgb)

  def setCellState(self, event):
    itemId = self.find_closest(event.x, event.y)[0]
    cell = self.lattice.canvasItemIds[itemId]
    rgb,colorHex = tkColorChooser.askcolor("white", title="choose cells state")
    if rgb is None:
      return

    self.itemconfig(itemId, fill=colorHex)
    cell.state = [rgb[0]/255]

class GUIStochasticTest(Frame):
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
    dimensions = (160, 160)
    rule = StochasticRule()
    self.lattice = SquareLattice.createInitialized(
        dimensions=dimensions,
        neighbourhoodMethod=vonNeumannNeighbourhood,
        resolution=16,
        rule=rule)
  
  def initializeLatticeWidget(self):
    self.latticeWidget = SquareLatticeWidget.createInitialized(self, self.lattice)
  
  def load(self):
    pass

  def save(self):
    data = self.lattice.toYAML()
    with open("data/two_band_configuration.ltc", 'w') as f:
      f.write(data)
    print("data saved")


  def simulationStep(self):
    self.lattice.nextStep()
    self.latticeWidget.redrawLattice()
    self.update()

  def simulationLoop(self):
    self.simulationStep()
    if self.running:
      self.after(100, self.simulationLoop)

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
  test = GUIStochasticTest(root)
  test.mainloop()

