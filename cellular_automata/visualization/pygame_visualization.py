import pygame, sys
from pygame.locals import *


class PygameVisualization:
    def __init__(self, lattice, fps=30):
        self.lattice = lattice
        self.fps = fps
        self.init_py_game()
        self.initialize_basic_colors()

    def initialize_basic_colors(self):
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)

    def init_py_game(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.init_window()

    def set_fps(self, fps):
        self.fps = fps

    def init_window(self):
        self.surface = pygame.display.set_mode(
            (self.lattice.width, self.lattice.height))
        pygame.display.set_caption("Cellular Automata")

    def start(self):
        self.running = True
        self.main_loop()

    def on_event(self, event):
        if event.type == QUIT:
            self.quit()
        elif event.type == KEYDOWN:
            self.key_event(event)
        elif event.type == MOUSEBUTTONUP:
            self.mouse_button_event(event)

    def key_event(self, event):
        if event.key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(QUIT))

    def mouse_button_event(self, event):
        pass

    def quit(self):
        self.running = False

    def on_loop(self):
        self.lattice.next_step()
        self.print_stats()

    def on_render(self):
        self.clear_surface()
        self.draw_lattice(self.lattice.cells)
        self.update()

    def update(self):
        pygame.display.update()
        self.fps_clock.tick(self.fps)

    def clear_surface(self):
        self.surface.fill(self.white)

    def draw_lattice(self, cells):
        for cell in cells.values():
            self.draw_cell(cell)

    def draw_cell(self, cell):
        tlx = cell.x - cell.radius
        tly = cell.y - cell.radius
        width = cell.radius * 2
        height = cell.radius * 2
        rgb = cell.state.rgb
        py_color = pygame.Color(rgb[0], rgb[1], rgb[2])
        self.draw_rect(py_color, (tlx, tly, width, height))

    def draw_rect(self, color, position):
        pygame.draw.rect(self.surface, color, position)

    def print_stats(self):
        count = len(self.lattice.cells)
        print("time {:05d}".format(pygame.time.get_ticks()))
        print("# Cells : {:03d}".format(count))

    def on_cleanup(self):
        print("Ending application loop")
        pygame.quit()
        sys.exit()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
