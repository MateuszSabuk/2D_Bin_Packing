import tkinter as tk

from helpers import *
from algorithms import Algorithms

class BinPackingApp:
    def gen_boxes(self):
        self.bss.generate_boxes(
            self.min_box_dim,
            self.max_box_dim,
            self.num_of_boxes)
        self.boxes_text.delete('1.0', tk.END)
        self.boxes_text.insert(1.0, self.bss.get_boxes_text())
        
    def run_solver(self):
        self.num = 0
        self.canvas.delete("all")
        # Try solving the problem
        try:
            self.bss.update_boxes_from_txt(self.boxes_text.get("1.0", tk.END))

            bins1 = self.bss.solve(Algorithms.HFF)
            bins2 = self.bss.solve(Algorithms.HNF)

            # Draw the data
            self.draw_bins(bins1, bin_size = self.bss.bin_size)
            self.draw_bins(bins2, bin_size = self.bss.bin_size)
        except ValidationError as err:
            print(f"Exception: {err}")

    def __init__(self):
        self.bss = BoxStackingSolver() # Create the main solver
        self.min_box_dim = 1
        self.max_box_dim = 10
        self.num_of_boxes = 20
        self.bss.bin_size = (20, 15) # Set the size for the containers

        self.master = tk.Tk()
        self.gen_boxes_button = tk.Button(self.master,
                text="Generate Boxes",
                command= self.gen_boxes)
        self.gen_boxes_button.grid(row = 0, column = 0, padx = 2)
        
        self.boxes_text: tk.Text = tk.Text(self.master, width=20)
        self.boxes_text.grid(row = 1, column = 0, padx = 2)

        self.run_solver_button = tk.Button(self.master,
                text="Run Solver",
                command= self.run_solver)
        self.run_solver_button.grid(row = 3, column = 0, padx = 2)

        self.canvas = tk.Canvas(self.master, width=1000, height=1000, bg='white')
        self.canvas.grid(row = 0, column = 1, sticky = tk.W, padx = 2, rowspan=3)
        self.num = 0

    def run(self):
        self.master.mainloop()

    def draw_bins(self, bins, bin_size):
        scale = 10
        bin_offset = scale * 1.1 * bin_size[0]
        bin_y_offset = scale * 1.1 * bin_size[1]
        for bin_idx, bin in enumerate(bins):
            for box_idx, box in enumerate(bin):
                x0 = box.x * scale + bin_offset * bin_idx
                y0 = box.y * scale + bin_y_offset * self.num
                x1 = x0 + box.w * scale
                y1 = y0 + box.h * scale
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='red')
                # # Indexes on each for diagnostics
                # self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f'Box {bin_idx}-{box_idx}')
            
            # Draw a rectangle for each bin
            self.canvas.create_rectangle(
                bin_idx * bin_offset,
                self.num * bin_y_offset,
                bin_idx * bin_offset + bin_size[0] * scale,
                self.num * bin_y_offset + bin_size[1] * scale,
                outline='black')
        self.num += 1

def main():
    app = BinPackingApp()
    app.run()


if __name__ == "__main__":
    main()