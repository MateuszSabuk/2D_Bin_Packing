import tkinter as tk

from helpers import *
from algorithms import Algorithms

class BinPackingApp:
    def __init__(self):
        self.master = tk.Tk()
        self.canvas = tk.Canvas(self.master, width=1000, height=1000, bg='white')
        self.canvas.pack()
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
            self.canvas.create_rectangle(   bin_idx * bin_offset,
                                            self.num * bin_y_offset,
                                            bin_idx * bin_offset + bin_size[0] * scale,
                                            self.num * bin_y_offset + bin_size[1] * scale,
                                            outline='black')
        self.num += 1

def main():
    app = BinPackingApp()

    bss = BoxStackingSolver() # Create the main solver
    bss.bin_size = (20, 15) # Set the size for the containers
    bss.generate_boxes(1, 10, 20)  # Generate boxes (5 boxes with dimensions ranging from 1 to 10)
    
    # Try solving the problem
    try:
        bins1 = bss.solve(Algorithms.HFF)
        bins2 = bss.solve(Algorithms.HNF)

        # Draw the data
        app.draw_bins(bins1, bin_size = bss.bin_size)
        app.draw_bins(bins2, bin_size = bss.bin_size)
    except ValidationError as err:
        print(f"Exception: {err}")
    
    app.run()


if __name__ == "__main__":
    main()