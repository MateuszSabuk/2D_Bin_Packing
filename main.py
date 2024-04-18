import tkinter as tk

from helpers import *
from algorithms import Algorithms

class BinPackingApp:
    def __init__(self):
        self.bss = BoxStackingSolver() # Create the main solver
        self.master = tk.Tk()
        self.num = 0

        self.inputs_frame = tk.Frame(self.master)
        self.inputs_frame.grid(row = 0, column = 0,sticky="n")

        # Generation parameters inputs
        self.box_gen_inputs_frame = tk.Frame(self.inputs_frame)
        self.box_gen_inputs_frame.pack()
        
        tk.Label(self.box_gen_inputs_frame, text="Box dimensions:").grid(row = 0, column = 0, columnspan=3)

        tk.Label(self.box_gen_inputs_frame, text="<= width <=").grid(row = 1, column = 1)
        self.min_box_width_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=8)
        self.min_box_width_entry.insert(0,"1")
        self.min_box_width_entry.grid(row = 1, column = 0, padx = 2)

        self.max_box_width_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=8)
        self.max_box_width_entry.insert(0,"10")
        self.max_box_width_entry.grid(row = 1, column = 2, padx = 2)

        tk.Label(self.box_gen_inputs_frame, text="<= height <=").grid(row = 2, column = 1)
        self.min_box_height_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=8)
        self.min_box_height_entry.insert(0,"2")
        self.min_box_height_entry.grid(row = 2, column = 0, padx = 2)

        self.max_box_height_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=8)
        self.max_box_height_entry.insert(0,"12")
        self.max_box_height_entry.grid(row = 2, column = 2, padx = 2)

        tk.Label(self.box_gen_inputs_frame, text="Num of boxes:").grid(row = 3, column = 0, columnspan=2)
        self.num_of_boxes_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=8)
        self.num_of_boxes_entry.insert(0,"20")
        self.num_of_boxes_entry.grid(row=3, column=2)

        tk.Label(self.box_gen_inputs_frame, text="Bin dimensions:").grid(row = 4, column = 0, columnspan=3)
        self.bin_size_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame, width=20)
        self.bin_size_entry.insert(0,"20x15")
        self.bin_size_entry.grid(row=5, column=0, columnspan=3)

        # Buttons and others
        self.gen_boxes_button = tk.Button(self.inputs_frame,
            text="Generate Boxes",
            command= self.gen_boxes)
        self.gen_boxes_button.pack(pady=5)

        self.boxes_text: tk.Text = tk.Text(self.inputs_frame, width=20)
        self.boxes_text.pack()

        self.run_solver_button = tk.Button(self.inputs_frame,
            text="Run Solver",
            command= self.run_solver)
        self.run_solver_button.pack(pady=5)

        tk.Label(self.inputs_frame, text="Output:").pack()
        self.output_label = tk.Label(self.inputs_frame, text="")
        self.output_label.pack()
        
        self.canvas = tk.Canvas(self.master, width=1000, height=1000, bg='white')
        self.canvas.grid(row = 0, column = 1, sticky = tk.W, padx = 2)

    def run(self):
        self.master.mainloop()
    
    def gen_boxes(self):
        try:
            self.bss.update_bin_size(self.bin_size_entry.get())

            self.bss.generate_boxes(
                int(self.min_box_width_entry.get()),
                int(self.max_box_width_entry.get()),
                int(self.min_box_height_entry.get()),
                int(self.max_box_height_entry.get()),
                int(self.num_of_boxes_entry.get()))
            self.boxes_text.delete('1.0', tk.END)
            self.boxes_text.insert(1.0, self.bss.get_boxes_text())
            self.output_label.config(text="Generated boxes", bg="green")
        except Exception as err:
            print(f"Exception: {err}")
            self.output_label.config(text=err, bg="red")
        
    def run_solver(self):
        self.num = 0
        self.canvas.delete("all")
        # Try solving the problem
        try:
            self.bss.update_bin_size(self.bin_size_entry.get())

            self.bss.update_boxes_from_txt(self.boxes_text.get("1.0", tk.END))

            bins1 = self.bss.solve(Algorithms.HFF)
            bins2 = self.bss.solve(Algorithms.HNF)

            # Draw the data
            self.draw_bins(bins1, bin_size = self.bss.bin_size)
            self.draw_bins(bins2, bin_size = self.bss.bin_size)
            self.output_label.config(text="Solved succesfully", bg="green")
        except ValidationError as err:
            print(f"Exception: {err}")
            self.output_label.config(text=err, bg="red")

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