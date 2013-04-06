from Tkinter import *
from glob import glob
from cmaes.objectives import EnergyStopCriterion    # JUST TEMPORARY, REMOVE LATER
import tkFileDialog
import time


class LatticeWidget(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master)
        self.lattice = None

    @classmethod
    def create_initialized(cls, master, lattice):
        view = cls(master)
        view.lattice = lattice
        view.config(highlightthickness=0, width=lattice.width,
                    height=lattice.height)
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
        self.tag_bind(cell.canvas_item_id, '<ButtonPress-1>',
                      self.set_cell_state)
        self.lattice.canvas_item_ids[cell.canvas_item_id] = cell

    def redraw_lattice(self):
        map(lambda cell: self.redraw_cell(cell), self.cells)
        self.remove_unused_items()

    def redraw_cell(self, cell):
        # redraw position + color
        if not hasattr(cell,
                       "canvas_item_id"):   # must create new canvas item after merge or division
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
        raise NotImplementedError(
            "method for setting cell state not implemented")


class SimpleGUI(Frame):
    def __init__(self, master, lattice_widget_class):
        Frame.__init__(self, master)
        self.lattice_widget_class = lattice_widget_class
        self.initialize_lattice()
        self.initialize_lattice_widget()
        self.create_controls()
        self.pack()

    def create_controls(self):
        self.step = self.create_button("next step", self.simulation_step,
                                       "left")
        self.run = self.create_run_button()
        self.save = self.create_button("save", self.save, "right")
        self.load = self.create_button("load", self.load, "right")

    def initialize_lattice(self):
        raise NotImplementedError(
            "method for initializing lattice is not implemented")

    def initialize_lattice_widget(self):
        self.lattice_widget = self.lattice_widget_class.create_initialized(self,
                                                                           self.lattice)

    def load(self):
        #get file_name to open
        file_dialog_options = {}
        file_dialog_options['filetypes'] = [('lattice files', '.ltc')]
        file_dialog_options['initialdir'] = "./"
        file_name = tkFileDialog.askopenfilename(**file_dialog_options)

        if file_name is None:
            print("No more loading.")
            return

        # create new widget
        self.lattice_widget.destroy()

        # load lattice configuration
        self.lattice = self.lattice.load_configuration(file_name)
        self.initialize_lattice_widget()
        self.pack()

    def save(self):
        file_dialog_options = {}
        file_dialog_options['filetypes'] = [('lattice files', '.ltc')]
        file_dialog_options['initialdir'] = "./"
        file_name = tkFileDialog.asksaveasfilename(**file_dialog_options)
        if file_name is None:
            print("Forget about saving...")
            return

        self.lattice.save_configuration(file_name)
        print("Yep, it's saved.")

    def simulation_step(self):
        self.lattice.next_step()
        self.lattice_widget.redraw_lattice()
        self.update()

    def simulation_loop(self):
        self.simulation_step()
        if self.running:
            if self.stop_criterion.should_run(
                    self.lattice):    # JUST TEMPORARY, REMOVE LATER
                self.after(0, self.simulation_loop)
            else:
                if self.lattice.chaotic:
                    print("chaotic rule, stopping after 1024 steps")
                else:
                    print("lattice energy variance stabilized")
                self.pause_simulation()

    def run_simulation(self):
        self.stop_criterion = EnergyStopCriterion()
        self.toogle_run_pause()
        self.running = True
        self.simulation_loop()

    def pause_simulation(self):
        self.toogle_run_pause()
        self.running = False

    def toogle_run_pause(self):
        if self.run is None:
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
