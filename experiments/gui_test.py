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
    def map_state_to_rgb(self, state):
        return "#{:02X}{:02X}{:02X}".format(state.rgb[0], state.rgb[1],
                                            state.rgb[2])


class GUITest(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.width = 600
        self.height = 480
        self.pack()
        self.configure(width=self.width, height=self.height)
        self.pack_propagate(False)
        # self.main_widget = self.create_slides(5)
        self.main_widget = self.create_main_slider()

    def create_main_slider(self):
        main_widget = Frame(self, width=self.width * 3, height=self.height)
        main_widget.configure(bg="#CCC")
        main_widget.pack_propagate(False)
        main_widget.place(anchor=NW)

        self.create_slide(main_widget)
        self.create_slide(main_widget)
        self.create_slide(main_widget)
        self.actual_slide = 1

        return main_widget

    def create_slide(self, main_widget):
        slide = Frame(main_widget)
        slide.configure(width=self.width, height=self.height)
        slide.configure(bg="#999", bd=2, relief=GROOVE, highlightcolor="#000")
        slide.pack(side="left")
        slide.pack_propagate(False)

        label = Label(slide, text="for next slide click right half")
        label.pack(fill=BOTH)
        label.configure(bg="#999")

        slide.bind("<Button-1>", self.move_slide)

    def next_slide(self):
        x = int(self.main_widget.place_info()["x"])
        while x > -self.width * self.actual_slide:
            self.main_widget.place_configure(x=x - 5)
            x -= 5
            self.update()
        self.actual_slide += 1

    def previous_slide(self):
        if self.actual_slide < 2:
            return
        x = int(self.main_widget.place_info()["x"])
        while x < -self.width * (self.actual_slide - 2):
            self.main_widget.place_configure(x=x + 5)
            x += 5
            self.update()
        self.actual_slide -= 1

    def move_slide(self, event):
        if event.x <= self.width / 2:
            self.previous_slide()
        else:
            self.next_slide()

    def create_slides(self, number_of_slides):
        main_widget = Frame(self, width=number_of_slides * self.width,
                            height=self.height)
        main_widget.pack()
        self.slides = [Frame(
            main_widget,
            width=self.width,
            height=self.height)] * number_of_slides

        for idx, slide in enumerate(self.slides):
            slide.pack()
            label = Label(slide, text="F{}".format(idx))
            label.pack()

            slide.configure(bg="#999", borderwidth=1)
            slide.place_configure(x=idx * self.width, y=0)
        main_widget.place_configure(x=0, y=0)
        self.configure(width=self.width, height=self.height)
        return main_widget

    def initialize_lattice_widget(self):
        self.lattice_widget = VariableSquareLatticeWidget.create_initialized(
            self, self.lattice)

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
    test = GUITest(root)
    test.mainloop()


