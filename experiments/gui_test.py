import sys, os
ca_directory = os.getcwd()
if ca_directory not in sys.path:
  sys.path.insert(0, ca_directory)

from cellular_automata.lattices.equiangular import VariableSquareLattice
from cellular_automata.lattices.neighbourhoods import VonNeumann
from cellular_automata.visualization.tkinter_visualization import LatticeWidget
from cellular_automata.rules.base import DummyRule
from cellular_automata.states.base import ColorState
from Tkinter import *

class VariableSquareLatticeWidget(LatticeWidget):
  def mapStateToRGB(self, state):
    return "#{:02X}{:02X}{:02X}".format(state.rgb[0], state.rgb[1], state.rgb[2])

class GUITest(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.width = 600
    self.height = 480
    self.pack()
    self.configure(width=self.width, height=self.height)
    self.pack_propagate(False)
    # self.mainWidget = self.createSlides(5)
    self.mainWidget = self.createMainSlider()

  def createMainSlider(self):
    mainWidget = Frame(self, width=self.width*3, height=self.height)
    mainWidget.configure(bg="#CCC")
    mainWidget.pack_propagate(False)
    mainWidget.place(anchor=NW)

    
    self.createSlide(mainWidget)
    self.createSlide(mainWidget)
    self.createSlide(mainWidget)
    self.actualSlide = 1

    return mainWidget

  def createSlide(self, mainWidget):
    slide = Frame(mainWidget)
    slide.configure(width=self.width, height=self.height)
    slide.configure(bg="#999", bd=2, relief=GROOVE, highlightcolor="#000")
    slide.pack(side="left")
    slide.pack_propagate(False)

    label = Label(slide, text="for next slide click right half")
    label.pack(fill=BOTH)
    label.configure(bg="#999")

    slide.bind("<Button-1>", self.moveSlide)

  def nextSlide(self):
    x = int(self.mainWidget.place_info()["x"])
    while x > -self.width*self.actualSlide:
      self.mainWidget.place_configure(x=x-5)
      x -=5
      self.update()
    self.actualSlide += 1

  def previousSlide(self):
    if self.actualSlide < 2:
      return
    x = int(self.mainWidget.place_info()["x"])
    while x < -self.width*(self.actualSlide-2):
      self.mainWidget.place_configure(x=x+5)
      x +=5
      self.update()
    self.actualSlide -= 1

  def moveSlide(self, event):
    if event.x <= self.width/2:
      self.previousSlide()
    else:
      self.nextSlide()

  def createSlides(self, numberOfSlides):
    mainWidget = Frame(self, width=numberOfSlides*self.width, height=self.height)
    mainWidget.pack()
    self.slides = [Frame(
      mainWidget,
      width=self.width,
      height=self.height)]*numberOfSlides

    for idx,slide in enumerate(self.slides):
      slide.pack()
      label = Label(slide, text="F{}".format(idx))
      label.pack()

      slide.configure(bg="#999",borderwidth=1)
      slide.place_configure(x=idx*self.width, y=0)
    mainWidget.place_configure(x=0, y=0)
    self.configure(width=self.width, height=self.height)
    return mainWidget
    
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
  test = GUITest(root)
  test.mainloop()


