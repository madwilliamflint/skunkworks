import sys
import json
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QStatusBar, QMenuBar, QMenu, QAction, QFileDialog, QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QKeyEvent, QContextMenuEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF

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
