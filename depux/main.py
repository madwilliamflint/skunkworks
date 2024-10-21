import sys
import json
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QStatusBar, QMenuBar, QMenu, QAction, QFileDialog, QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QKeyEvent, QContextMenuEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF

from graphics import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.create_menu()

        node1 = Node(0, 0, "Node 1", "yellow")
        node2 = Node(200, 200, "Node 2", "yellow")
        self.scene.addItem(node1)
        self.scene.addItem(node2)

        self.view.show()
        self.scene.selectionChanged.connect(self.update_status)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_diagram)
        file_menu.addAction(save_action)
        
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_diagram)
        file_menu.addAction(load_action)

    def contextMenuEvent(self, event: QContextMenuEvent):
        context_menu = QMenu(self)

        add_ellipse_node_action = QAction('Add Ellipse Node', self)
        add_ellipse_node_action.triggered.connect(lambda: self.add_node(event.pos(), "ellipse"))
        context_menu.addAction(add_ellipse_node_action)
        
        add_rect_node_action = QAction('Add Rect Node', self)
        add_rect_node_action.triggered.connect(lambda: self.add_node(event.pos(), "rect"))
        context_menu.addAction(add_rect_node_action)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def add_node(self, position, node_type="ellipse"):
        scene_position = self.view.mapToScene(position)
        if node_type == "ellipse":
            node = Node(scene_position.x(), scene_position.y(), "New Ellipse Node", "yellow")
        else:
            node = RectNode(scene_position.x(), scene_position.y(), "New Rect Node", "lightblue")
        self.scene.addItem(node)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.remove_selected_items()
        super().keyPressEvent(event)

    def remove_selected_items(self):
        for item in self.scene.selectedItems():
            if isinstance(item, Edge):
                self.scene.removeItem(item)
                item.source.remove_edge(item)
                item.dest.remove_edge(item)
            elif isinstance(item, Node):
                for edge in item.edges[:]:
                    self.scene.removeItem(edge)
                    edge.source.remove_edge(edge)
                    edge.dest.remove_edge(edge)
                self.scene.removeItem(item)
        self.update_status()

    def update_status(self):
        selected_items = self.scene.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            if isinstance(selected_item, Node):
                self.statusBar.showMessage(f"Selected: {selected_item.text}")
            elif isinstance(selected_item, Edge):
                self.statusBar.showMessage(f"Selected: {selected_item.text}")
        else:
            self.statusBar.clearMessage()

    def save_diagram(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "JSON Files (*.json)")
        if filename:
            data = {"nodes": [], "edges": []}
            for item in self.scene.items():
                if isinstance(item, Node):
                    color = item.brush().color().name()
                    data["nodes"].append({"text": item.text, "x": item.x(), "y": item.y(), "color": color})
                elif isinstance(item, Edge):
                    color = item.pen().color().name()
                    data["edges"].append({"source": item.source.text, "dest": item.dest.text, "text": item.text, "color": color})
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)  # Pretty print JSON

    def load_diagram(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Diagram", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.scene.clear()
            nodes = {}
            for node_data in data["nodes"]:
                node = Node(node_data["x"], node_data["y"], node_data["text"], node_data["color"])
                self.scene.addItem(node)
                nodes[node.text] = node
            for edge_data in data["edges"]:
                source = nodes[edge_data["source"]]
                dest = nodes[edge_data["dest"]]
                edge = Edge(source, dest, edge_data["text"], edge_data["color"])
                source.add_edge(edge)
                dest.add_edge(edge)
                self.scene.addItem(edge)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
