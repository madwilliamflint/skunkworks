import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TechTreeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tech Tree Diagram")
        self.geometry("800x600")

        graph = self.create_graph()
        self.draw_graph(graph)

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

    def draw_graph(self, graph):
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", ax=ax)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = TechTreeApp()
    app.mainloop()
