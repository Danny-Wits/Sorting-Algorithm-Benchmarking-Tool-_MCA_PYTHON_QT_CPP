from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import algo
import time


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sorting Benchmark")
        self.geometry("1400x800")
        self.sorting_algorithm = "All"
        self.sorting_info = {}  # store results for graph
        self.create_widgets()
        self.state("zoomed")
        self.style = ttk.Style()
        self.style.theme_use("xpnative")

    def create_widgets(self):
        self.algorithms = algo.ALGORITHMS
        self.algorithm_var = StringVar(self)
        self.algorithm_var.set(self.algorithms[0])
        self.algorithm_menu = ttk.Combobox(
            self, textvariable=self.algorithm_var, values=self.algorithms)
        self.algorithm_menu.pack(pady=10)
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.select_algorithm)

        self.size_var = StringVar(self)
        self.size_var.set("50")
        self.size_entry = ttk.Entry(self, textvariable=self.size_var)
        self.size_entry.pack(pady=10)

        buttons_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        buttons_frame.pack(padx=10, pady=10)

        self.generate_button = ttk.Button(
            buttons_frame, text="Generate", command=self.generate)
        self.generate_button.pack(side=LEFT, padx=10, pady=10)

        self.sort_button = ttk.Button(
            buttons_frame, text="Sort", command=self.sort)
        self.sort_button.pack(side=LEFT, padx=10, pady=10)

        self.graph_button = ttk.Button(
            buttons_frame, text="Graph", command=self.show_graph)
        self.graph_button.pack(side=LEFT, padx=10, pady=10)

        self.reset_button = ttk.Button(
            buttons_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=LEFT, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(
            self,
            orient=HORIZONTAL,
            length=600,
            mode="determinate")
        self.progress_bar.pack(padx=10, pady=10)

        self.canvas = Canvas(self, width=1400, height=600, bg="white")
        self.canvas.pack(pady=10)

    def draw(self, sorted=False):
        self.canvas.delete("all")
        if self.arr is None:
            return False
        if len(self.arr) > 300:
            self.canvas.create_text(
                self.canvas.winfo_width()/2,
                self.canvas.winfo_height() / 2,
                anchor="center",
                text=f"{len(self.arr)} elements are too many to visualize. But you can still sort them.",
                font=("Arial", 16))
            return False

        arr = self.arr
        canvas_height = 600
        canvas_width = 1400
        x_width = canvas_width / (len(arr) + 1)
        offset = 10
        spacing = 5
        normalized_arr = [i / max(arr) for i in arr]
        for i, height in enumerate(normalized_arr):
            x0 = i * x_width + offset + spacing
            y0 = canvas_height - height * 380
            x1 = (i + 1) * x_width + offset
            y1 = canvas_height
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="green" if sorted else "blue")
            if len(arr) <= 100:
                self.canvas.create_text(
                    x0 + x_width / 2,
                    y0 - 10,
                    text=str(arr[i]),
                    fill="black",
                    font=("Arial", 8),
                )
            self.update()
            time.sleep(0.01 if sorted else 0.001)
        return True

    def select_algorithm(self, event=None):
        selected_algorithm = self.algorithm_var.get()
        self.set_algo_from_name(selected_algorithm)

    def set_algo_from_name(self, selected_algorithm):
        if selected_algorithm == "All":
            self.sorting_algorithm = "All"
        elif selected_algorithm == "BubbleSort":
            self.sorting_algorithm = algo.BubbleSort()
        elif selected_algorithm == "SelectionSort":
            self.sorting_algorithm = algo.SelectionSort()
        elif selected_algorithm == "InsertionSort":
            self.sorting_algorithm = algo.InsertionSort()
        elif selected_algorithm == "MergeSort":
            self.sorting_algorithm = algo.MergeSort()
        elif selected_algorithm == "QuickSort":
            self.sorting_algorithm = algo.QuickSort()
        else:
            self.sorting_algorithm = None

    def generate(self):
        size = int(self.size_var.get())
        self.arr = algo.random_array(size)
        self.draw()

    def sort(self):
        if self.sorting_algorithm is None:
            messagebox.showinfo("Error", "Please select an algorithm.")
            return
        sorting_info = {}
        self.progress_bar["maximum"] = len(algo.ALGORITHMS)-1
        self.progress_bar["value"] = 0
        if self.sorting_algorithm == "All":
            for algorithm in algo.ALGORITHMS:
                if algorithm == "All":
                    continue
                self.set_algo_from_name(algorithm)
                algo_name, time_taken = self.get_sorting_info(
                    self.arr.copy() if algorithm != "QuickSort" else None)
                sorting_info[algo_name] = time_taken
                self.progress_bar["value"] += 1
                self.update()

            self.sorting_algorithm = "All"
        else:
            algo_name, time_taken = self.get_sorting_info()
            sorting_info[algo_name] = time_taken
            self.progress_bar["value"] = len(algo.ALGORITHMS)-1

        self.sorting_info = sorting_info  # store for graph
        self.draw(True)
        self.show_sorting_info(sorting_info)

    def get_sorting_info(self, arr=None):
        if arr is None:
            arr = self.arr
        start = time.perf_counter()
        self.sorting_algorithm.sort(arr)
        end = time.perf_counter()
        time_taken = (end - start) * 1000  # convert to ms
        return self.sorting_algorithm.name, round(time_taken, 2)

    def show_sorting_info(self, sorting_info):
        self.canvas.create_text(
            10,
            10,
            text=self.dict_to_string(self.sort_dict(sorting_info)),
            fill="black",
            anchor="nw",
            font=("Arial", 14),
        )
        self.update()

    def show_graph(self):
        """Draw a performance graph of the sorting results."""
        if not self.sorting_info:
            messagebox.showinfo("Info", "Please sort first to generate data.")
            return

        self.canvas.delete("all")

        data = self.sort_dict(self.sorting_info)
        algorithms = list(data.keys())
        times = list(data.values())

        # Graph settings
        canvas_width = 1400
        canvas_height = 600
        bar_width = (canvas_width - 200) / len(algorithms)
        max_time = max(times)
        scale = (canvas_height - 100) / max_time

        for i, algo_name in enumerate(algorithms):
            x0 = 100 + i * bar_width
            y0 = canvas_height - (times[i] * scale)
            x1 = x0 + bar_width * 0.7
            y1 = canvas_height - 50
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="skyblue", outline="black")
            self.canvas.create_text(
                (x0 + x1) / 2,
                y0 - 15,
                text=f"{times[i]} ms",
                font=("Arial", 10),
                fill="black",
            )
            self.canvas.create_text(
                (x0 + x1) / 2,
                canvas_height - 25,
                text=algo_name,
                font=("Arial", 10),
                fill="black",
                angle=45,
            )

        self.canvas.create_text(
            canvas_width / 2,
            30,
            text="Sorting Algorithm Performance",
            font=("Arial", 20, "bold"),
            fill="black",
        )

    def reset(self):
        self.canvas.delete("all")
        self.sorting_algorithm = None
        self.arr = None
        self.sorting_info = {}
        self.draw()

    def sort_dict(self, dictionary):
        return dict(sorted(dictionary.items(), key=lambda item: item[1]))

    def dict_to_string(self, dictionary):
        return "\n".join([f"{key:19}{value} ms" for key, value in dictionary.items()])


if __name__ == "__main__":
    app = App()
    app.mainloop()
