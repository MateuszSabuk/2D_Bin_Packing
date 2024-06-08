import tkinter as tk
import time

from helpers import *
from algorithms import Algorithms

class BinPackingApp:
    def __init__(self):
        self.canvas = None
        self.bss = BoxStackingSolver() # Create the main solver
        self.master = tk.Tk()
        self.num = 0
        self.new_windows = []
        width = self.master.winfo_screenwidth()
        if width <= 1980:
            width = 2560
        height = self.master.winfo_screenheight()
        if height <= 1080:
            height = 1440
        self.master.geometry('%dx%d' % (width/6, height/2))

        self.inputs_frame = tk.Frame(self.master)
        self.inputs_frame.grid(row = 0, column = 0,sticky="n")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.box_gen_inputs_frame = tk.Frame(self.inputs_frame)
        self.box_gen_inputs_frame.pack()

        tk.Label(self.box_gen_inputs_frame, text="Box dimensions:").grid(row = 0, column = 0, columnspan=3)

        tk.Label(self.box_gen_inputs_frame, text="<= width <=").grid(row = 1, column = 1)
        self.min_box_width_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.min_box_width_entry.insert(0,"1")
        self.min_box_width_entry.grid(row = 1, column = 0, padx = 2)

        self.max_box_width_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.max_box_width_entry.insert(0,"10")
        self.max_box_width_entry.grid(row = 1, column = 2, padx = 2)

        tk.Label(self.box_gen_inputs_frame, text="<= height <=").grid(row = 2, column = 1)
        self.min_box_height_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.min_box_height_entry.insert(0,"2")
        self.min_box_height_entry.grid(row = 2, column = 0, padx = 2)

        self.max_box_height_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.max_box_height_entry.insert(0,"12")
        self.max_box_height_entry.grid(row = 2, column = 2, padx = 2)

        tk.Label(self.box_gen_inputs_frame, text="Num of boxes:").grid(row = 3, column = 0, columnspan=2)
        self.num_of_boxes_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.num_of_boxes_entry.insert(0,"200")

        self.num_of_boxes_entry.grid(row=3, column=2)

        tk.Label(self.box_gen_inputs_frame, text="Bin dimensions:").grid(row = 4, column = 0, columnspan=3)
        self.bin_size_entry: tk.Entry = tk.Entry(self.box_gen_inputs_frame)
        self.bin_size_entry.insert(0,"20x15")
        self.bin_size_entry.grid(row=5, column=0, columnspan=3)

        # Algorithm selection
        tk.Label(self.inputs_frame, text="Select Algorithms:").pack()
        self.selected_algorithms = []
        self.algorithm_vars = []
        for algorithm_name in Algorithms.get_implemented_names():
            var = tk.BooleanVar()
            var.set(False)
            self.algorithm_vars.append(var)
            checkbox = tk.Checkbutton(self.inputs_frame, text=algorithm_name, variable=var, onvalue=True, offvalue=False)
            checkbox.pack()

        # Buttons and others
        self.gen_boxes_button = tk.Button(self.inputs_frame,
            text="Generate Boxes",
            command= self.gen_boxes)
        self.gen_boxes_button.pack(pady=5)

        self.boxes_text: tk.Text = tk.Text(self.inputs_frame, width=10)
        self.boxes_text.pack()

        self.run_solver_button = tk.Button(self.inputs_frame,
            text="Run Solver",
            command= self.run_solver)
        self.run_solver_button.pack(pady=5)

        tk.Label(self.inputs_frame, text="Output:").pack()
        self.output_label = tk.Label(self.inputs_frame, text="")
        self.output_label.pack()

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

        for window in self.new_windows:
            window.destroy()
        self.new_windows.clear()

        try:
            self.bss.update_bin_size(self.bin_size_entry.get())
            self.bss.update_boxes_from_txt(self.boxes_text.get("1.0", tk.END))

            selected_algorithms = [name for name, var in zip(Algorithms.get_implemented_names(), self.algorithm_vars) if var.get()]

            for algorithm_name in selected_algorithms:
                algorithm_function = getattr(Algorithms, algorithm_name)
                start_time = time.time()
                bins = algorithm_function(self.bss.bin_size, self.bss.boxes)
                end_time = time.time()
                elapsed_time = end_time - start_time

                # New window for each algorithm
                new_window = tk.Toplevel(self.master)
                self.new_windows.append(new_window)

                width = self.master.winfo_screenwidth()
                height = self.master.winfo_screenheight()
                new_window.geometry('%dx%d' % (width, height))

                tk.Label(new_window, text=algorithm_name).pack()
                scrollbar_vertical = tk.Scrollbar(new_window, orient=tk.VERTICAL)
                scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
                scrollbar_horizontal = tk.Scrollbar(new_window, orient=tk.HORIZONTAL)
                scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
                canvas = tk.Canvas(new_window, width=width, height=height, bg='white',
                                   yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
                canvas.pack(fill=tk.BOTH, expand=True)
                scrollbar_vertical.config(command=canvas.yview)
                scrollbar_horizontal.config(command=canvas.xview)

                # Draw bins for the current algorithm
                self.draw_bins(canvas, bins, bin_size=self.bss.bin_size, algorithm_name=algorithm_name,
                               computing_time=elapsed_time)

                canvas.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))

            self.output_label.config(text="Solved successfully", bg="green")
        except ValidationError as err:
            print(f"Exception: {err}")
            self.output_label.config(text=err, bg="red")

    def draw_bins(self, canvas, bins, bin_size, algorithm_name, computing_time):
        canvas.create_text(0,0, text=".",font=('Arial', 1, 'bold')) # Text to stop the canvas from cutting the left margin
        canvas_width = self.master.winfo_screenwidth()
        scale = 10.2 * canvas_width/2560
        bin_offset = scale * 1.1 * bin_size[0]
        print(bin_offset)
        bin_y_offset = scale * 1.1 * bin_size[1]

        x_offset = (canvas_width - (11*bin_offset))/2
        print(x_offset)
        y_text_offset = 40

        num_rows = ((len(bins) - len(bins) % 11) / 11 + 1)
        total_bins_height = num_rows * (bin_y_offset + 50)

        canvas.config(scrollregion=(0, 0, canvas.winfo_width(), canvas.winfo_height()))
        # Adjust canvas height if the total bins height exceeds current canvas height
        if total_bins_height > canvas.winfo_height():
            canvas.config(scrollregion=(0, 0, canvas.winfo_width(), total_bins_height))

        canvas.create_text(canvas_width/2, 20,
                                text=f'{algorithm_name}: {computing_time:.4f}s, bins used: {len(bins)}',
                                font=('Arial', 16, 'bold'))

        bin_row_x_offset = x_offset
        for bin_idx, bin in enumerate(bins):
            if bin_row_x_offset + bin_offset > canvas_width:
                bin_row_x_offset = x_offset
                y_text_offset += bin_y_offset + 30

            for box_idx, box in enumerate(bin):
                x0 = box.x * scale + bin_row_x_offset
                y0 = box.y * scale + y_text_offset
                x1 = x0 + box.w * scale
                y1 = y0 + box.h * scale
                canvas.create_rectangle(x0, y0, x1, y1, outline='red')
                if box.w < 3:
                    canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                       text=f'{box.w}x{box.h}', font=('Arial', 8), angle=90)
                else:
                    canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f'{box.w}x{box.h}', font=('Arial', 8))

            # Draw a rectangle for each bin
            canvas.create_rectangle(
                bin_row_x_offset,
                y_text_offset,
                bin_row_x_offset + bin_size[0] * scale,
                bin_size[1] * scale + y_text_offset,
                outline='black')

            bin_row_x_offset += bin_offset


def main():
    app = BinPackingApp()
    app.run()


if __name__ == "__main__":
    main()