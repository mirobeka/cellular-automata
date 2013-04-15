import tkFileDialog
import tkColorChooser
from Tkinter import *


class LatticeWidget(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master)
        self.lattice = None

    @classmethod
    def create_initialized(cls, master, lattice):
        lattice_widget = cls(master)
        lattice_widget.lattice = lattice
        lattice_widget.config(highlightthickness=0, width=lattice.width,
                              height=lattice.height)
        lattice_widget.pack()
        lattice_widget.create_canvas_items()
        return lattice_widget

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

    @classmethod
    def map_state_to_rgb(cls, state):
        raise NotImplementedError("method map_state_to_rgb not implemented")

    @classmethod
    def map_rgb_to_state(cls, rgb, state):
        raise NotImplementedError(
            "method for setting cell state not implemented")

    def set_cell_state(self, event):
        item_id = self.find_closest(event.x, event.y)[0]
        cell = self.lattice.canvas_item_ids[item_id]
        rgb, color_hex = tkColorChooser.askcolor("white",
                                                 title="choose cells state")
        if rgb is None:
            return
        self.itemconfig(item_id, fill=color_hex)
        self.map_rgb_to_state(rgb, cell.state)

    def remove_unused_items(self):
        items = [item for item in self.find_all()]
        for cell in self.cells:
            if cell.canvas_item_id in items:
                items.remove(cell.canvas_item_id)

        for item in items:
            self.delete(item)
            del self.lattice.canvas_item_ids[item]


class ControlBox(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_controls()

    def create_controls(self):
        self.step = self.create_button("next step",
                                       self.master.simulation_step,
                                       "left")
        self.run = self.create_run_button()
        self.save = self.create_button("save", self.master.save, "right")
        self.load = self.create_button("load", self.master.load, "right")

    def create_run_button(self):
        return self.create_button("run", self.master.run_simulation, "left")

    def create_pause_button(self):
        return self.create_button("pause", self.master.pause_simulation,
                                  "left")

    def create_button(self, text, callback, align):
        btn = Button(self)
        btn["text"] = text
        btn["command"] = callback
        btn.pack(side=align)
        return btn


class Statistics(Frame):
    pass


class SimpleGUI(Frame):
    """ This is basic GUI for visualizing this cellular automaton.

    How it works?
        -> Initialize GUI, create instance of Frame.
        -> insert lattice widget into scene
        -> create Tk() root stuff and show that.

    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.lattice_box = Frame(self)
        self.lattice_box.pack()
        self.controls_box = ControlBox(self)
        self.controls_box.pack()
        # self.statistics_box = Statistics(self)

    def show_me_something(self):
        self.pack()

    def insert_lattice_widget(self, lattice_widget_class, lattice):
        self.lattice = lattice
        # destroy all previous lattices
        for child in self.lattice_box.winfo_children():
            child.destroy()
        self.lattice_widget = lattice_widget_class.create_initialized(self.lattice_box, self.lattice)
        self.lattice_widget.pack()

    def load(self):
        #get file_name to open
        file_dialog_options = dict()
        file_dialog_options['filetypes'] = [('lattice files', '.ltc')]
        file_dialog_options['initialdir'] = "./"
        file_name = tkFileDialog.askopenfilename(**file_dialog_options)

        if file_name is None:
            print("No more loading.")
            return

        # load lattice configuration
        self.lattice = self.lattice.load_configuration(file_name)
        print(self.lattice_widget.__class__)
        self.insert_lattice_widget(self.lattice_widget.__class__, self.lattice)
        self.pack()

    def save(self):
        file_dialog_options = dict()
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
            self.after(0, self.simulation_loop)

    def run_simulation(self):
        self.toogle_run_pause()
        self.running = True
        self.simulation_loop()

    def pause_simulation(self):
        self.toogle_run_pause()
        self.running = False

    def toogle_run_pause(self):
        if self.controls_box.run is None:
            self.controls_box.pause.destroy()
            self.controls_box.pause = None
            self.controls_box.run = self.controls_box.create_run_button()
        else:
            self.controls_box.run.destroy()
            self.controls_box.run = None
            self.controls_box.pause = self.controls_box.create_pause_button()

