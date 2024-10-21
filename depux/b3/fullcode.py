

import sys
import json
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QStatusBar, QMenuBar, QAction, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF

import sys
import json
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QStatusBar, QMenu, QAction, QFileDialog, QGraphicsItem
from PyQt5.QtGui import QContextMenuEvent, QKeyEvent

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
import sys
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRectF

class EditDialog(QDialog):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Attributes")
        layout = QVBoxLayout()

        self.label_edit = QLineEdit(self)
        self.label_edit.setText(self.item.text)
        layout.addWidget(QLabel("Label:"))
        layout.addWidget(self.label_edit)

        self.color_button = QPushButton("Choose Color", self)
        self.color_button.clicked.connect(self.choose_color)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_button)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            if isinstance(self.item, Node):
                self.item.setBrush(QBrush(color))
            elif isinstance(self.item, Edge):
                self.item.setPen(QPen(color, 2))

    def save(self):
        self.item.text = self.label_edit.text()
        self.accept()

class Node(QGraphicsEllipseItem):
    node_counter = 0

    def __init__(self, x, y, text, color="yellow"):
        super().__init__(-30, -30, 60, 60)
        self.id = Node.node_counter
        Node.node_counter += 1
        self.setBrush(QBrush(QColor(color)))
        self.setPos(x, y)
        self.text = text
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.edges = []
        self.temp_edge = None

    def boundingRect(self):
        return QRectF(-30, -30, 60, 60)

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush())
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(self.boundingRect())
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.text)
        painter.setPen(QPen(Qt.red, 1))
        painter.drawLine(-15, 0, 15, 0)
        painter.drawLine(0, -15, 0, 15)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def mouseDoubleClickEvent(self, event):
        dialog = EditDialog(self)
        if dialog.exec_():
            self.color = self.brush().color().name()  # Update color attribute
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() == Qt.ControlModifier:
                self.setFlag(QGraphicsItem.ItemIsMovable, True)
            else:
                if self.temp_edge is None:
                    self.temp_edge = TempEdge(self)
                    self.temp_edge.setLine(QLineF(self.pos(), event.scenePos()))
                    self.scene().addItem(self.temp_edge)
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            super().mouseMoveEvent(event)
        else:
            if self.temp_edge:
                self.temp_edge.setLine(QLineF(self.pos(), event.scenePos()))
        for edge in self.edges:
            edge.adjust()

    def mouseReleaseEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            if self.temp_edge:
                items = self.scene().items(event.scenePos())
                for item in items:
                    if isinstance(item, Node) and item != self:
                        edge = Edge(self, item, "", "black")
                        self.add_edge(edge)
                        item.add_edge(edge)
                        self.scene().addItem(edge)
                        break
                self.scene().removeItem(self.temp_edge)
                self.temp_edge = None
        super().mouseReleaseEvent(event)

class TempEdge(QGraphicsLineItem):
    def __init__(self, source_node):
        super().__init__()
        self.source = source_node

class Edge(QGraphicsLineItem):
    edge_counter = 0

    def __init__(self, source_node, dest_node, text="", color="black"):
        super().__init__()
        self.id = Edge.edge_counter
        Edge.edge_counter += 1
        self.source = source_node
        self.dest = dest_node
        self.text = text
        self.color = color
        self.setPen(QPen(QColor(color), 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.adjust()

    def adjust(self):
        line = QLineF(self.source.scenePos(), self.dest.scenePos())
        self.setLine(line)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setPen(self.pen())
        painter.setBrush(self.pen().color())
        midpoint = self.line().pointAt(0.5)
        painter.drawText(midpoint, self.text)

    def mouseDoubleClickEvent(self, event):
        dialog = EditDialog(self)
        if dialog.exec_():
            self.color = self.pen().color().name()  # Update color attribute
            self.update()


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

        add_node_action = QAction('Add Node', self)
        add_node_action.triggered.connect(lambda: self.add_node(event.pos()))
        context_menu.addAction(add_node_action)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def add_node(self, position):
        scene_position = self.view.mapToScene(position)
        node = Node(scene_position.x(), scene_position.y(), "New Node", "yellow")
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
