import tkinter as tk
from tkinter import messagebox
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("900x600")

        # Array and Speed
        self.data = []
        self.speed = 0.1

        # UI Elements
        self.ui_frame = tk.Frame(self.root, width=900, height=200, bg='black')
        self.ui_frame.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self.root, width=900, height=400, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.ui_frame, text="Enter Array Elements (comma-separated):", bg='lightgray').grid(row=0, column=0, padx=10, pady=10)
        self.array_entry = tk.Entry(self.ui_frame, width=50)
        self.array_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.ui_frame, text="Generate Array", command=self.generate_array).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.ui_frame, text="Choose Sorting Algorithm:", bg='lightgray').grid(row=1, column=0, padx=10, pady=10)

        self.algorithm_menu = tk.StringVar()
        self.algorithm_menu.set("Bubble Sort")
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
        self.algorithm_dropdown = tk.OptionMenu(self.ui_frame, self.algorithm_menu, *algorithms)
        self.algorithm_dropdown.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.ui_frame, text="Speed (1-10):", bg='lightgray').grid(row=2, column=0, padx=10, pady=10)
        self.speed_scale = tk.Scale(self.ui_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_scale.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.ui_frame, text="Start Sorting", command=self.start_sorting).grid(row=2, column=2, padx=10, pady=10)

    def generate_array(self):
        array_input = self.array_entry.get()
        try:
            self.data = [int(x) for x in array_input.split(",")]
            self.draw_array(self.data, ['blue' for _ in range(len(self.data))])
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid array of integers separated by commas.")

    def draw_array(self, data, color_array):
        self.canvas.delete("all")
        canvas_width = 900
        canvas_height = 400
        bar_width = canvas_width / (len(data) + 1)
        offset = 30
        spacing = 10
        normalized_data = [x / max(data) for x in data]

        for i, height in enumerate(normalized_data):
            x0 = i * bar_width + offset
            y0 = canvas_height - height * 350
            x1 = (i + 1) * bar_width + offset
            y1 = canvas_height

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(data[i]))

        self.root.update_idletasks()

    def start_sorting(self):
        self.speed = self.speed_scale.get() / 10
        algorithm = self.algorithm_menu.get()

        if algorithm == "Bubble Sort":
            self.bubble_sort(self.data)
        elif algorithm == "Selection Sort":
            self.selection_sort(self.data)
        elif algorithm == "Insertion Sort":
            self.insertion_sort(self.data)
        elif algorithm == "Merge Sort":
            self.merge_sort(self.data, 0, len(self.data) - 1)
        elif algorithm == "Quick Sort":
            self.quick_sort(self.data, 0, len(self.data) - 1)

    def bubble_sort(self, data):
        for i in range(len(data)):
            for j in range(len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.draw_array(data, ['green' if x == j or x == j + 1 else 'blue' for x in range(len(data))])
                    time.sleep(self.speed)
        self.draw_array(data, ['green' for _ in range(len(data))])

    def selection_sort(self, data):
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            self.draw_array(data, ['green' if x == i or x == min_idx else 'blue' for x in range(len(data))])
            time.sleep(self.speed)
        self.draw_array(data, ['green' for _ in range(len(data))])

    def insertion_sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
                self.draw_array(data, ['green' if x == j or x == j + 1 else 'blue' for x in range(len(data))])
                time.sleep(self.speed)
            data[j + 1] = key
        self.draw_array(data, ['green' for _ in range(len(data))])

    def merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(data, left, mid)
            self.merge_sort(data, mid + 1, right)
            self.merge(data, left, mid, right)

    def merge(self, data, left, mid, right):
        left_part = data[left:mid + 1]
        right_part = data[mid + 1:right + 1]

        left_idx = right_idx = 0
        sorted_idx = left

        while left_idx < len(left_part) and right_idx < len(right_part):
            if left_part[left_idx] <= right_part[right_idx]:
                data[sorted_idx] = left_part[left_idx]
                left_idx += 1
            else:
                data[sorted_idx] = right_part[right_idx]
                right_idx += 1
            sorted_idx += 1
            self.draw_array(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
            time.sleep(self.speed)

        while left_idx < len(left_part):
            data[sorted_idx] = left_part[left_idx]
            left_idx += 1
            sorted_idx += 1
            self.draw_array(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
            time.sleep(self.speed)

        while right_idx < len(right_part):
            data[sorted_idx] = right_part[right_idx]
            right_idx += 1
            sorted_idx += 1
            self.draw_array(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
            time.sleep(self.speed)

    def quick_sort(self, data, low, high):
        if low < high:
            pi = self.partition(data, low, high)
            self.quick_sort(data, low, pi - 1)
            self.quick_sort(data, pi + 1, high)

    def partition(self, data, low, high):
        pivot = data[high]
        i = low - 1

        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                self.draw_array(data, ['green' if x == i or x == j else 'blue' for x in range(len(data))])
                time.sleep(self.speed)

        data[i + 1], data[high] = data[high], data[i + 1]
        self.draw_array(data, ['green' if x == i + 1 or x == high else 'blue' for x in range(len(data))])
        time.sleep(self.speed)

        return i + 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
