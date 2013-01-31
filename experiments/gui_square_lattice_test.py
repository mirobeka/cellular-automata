import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import SquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.rules.neural_rule import MLPColorRule
from cellular_automata.state.base import ColorState
from Tkinter import *
import yaml

class SquareLatticeWidget(LatticeWidget):
  def mapStateToRGB(self, state):
    return "#{:02X}{:02X}{:02X}".format(state.rgb[0], state.rgb[1], state.rgb[2])

class GUISquareLatticeTest(Frame):
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
    dimensions = (256, 256)
    rule = MLPColorRule()
    rule.set_weights(self.get_weights())
    self.lattice = SquareLattice.createInitialized(
        dimensions=dimensions,
        neighbourhood=VonNeumann,
        resolution=16,
        state=ColorState,
        rule=rule)
  
  def get_weights(self):
    pass
    # with open("data/result.yaml",'r') as f:
    #   result = yaml.load(f)

    # return result

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
  test = GUISquareLatticeTest(root)
  test.mainloop()


