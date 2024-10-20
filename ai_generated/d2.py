import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

class TechTreeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tech Tree Diagram")
        self.geometry("800x600")

        self.graph = self.create_graph()
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.draw_graph()
        self.enable_drag()

    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_edges_from([
            ("Project", "Task 1"),
            ("Task 1", "Subtask 1.1"),
            ("Task 1", "Subtask 1.2"),
            ("Project", "Task 2"),
            ("Task 2", "Subtask 2.1"),
            ("Task 2", "Subtask 2.2")
        ])
        return graph

    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color="skyblue", ax=self.ax)
        self.canvas.draw()

    def enable_drag(self):
        cursor = mplcursors.cursor(self.ax.figure, hover=True)
        cursor.connect("add", self.on_click)

    def on_click(self, sel):
        node = sel.annotation.get_text()
        self.dragging_node = node
        self.canvas.mpl_connect("motion_notify_event", self.on_drag)
        self.canvas.mpl_connect("button_release_event", self.on_release)

    def on_drag(self, event):
        if event.inaxes != self.ax:
            return
        pos = nx.spring_layout(self.graph)
        pos[self.dragging_node] = (event.xdata, event.ydata)
        self.ax.clear()
        nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color="skyblue", ax=self.ax)
        self.canvas.draw()

    def on_release(self, event):
        self.canvas.mpl_disconnect(self.on_drag)
        self.canvas.mpl_disconnect(self.on_release)

if __name__ == "__main__":
    app = TechTreeApp()
    app.mainloop()
