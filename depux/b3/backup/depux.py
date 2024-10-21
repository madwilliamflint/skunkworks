#!python

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QLineF

class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, text):
        super().__init__(-30, -30, 60, 60)
        self.setBrush(QBrush(Qt.yellow))
        self.setPos(x, y)
        self.text = text
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.edges = []
        self.temp_edge = None

    def boundingRect(self):
        return QRectF(-30, -30, 60, 60)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.yellow))
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() == Qt.ControlModifier:
                self.setFlag(QGraphicsItem.ItemIsMovable, True)
            else:
                if self.temp_edge is None:
                    self.temp_edge = QGraphicsLineItem(QLineF(self.pos(), event.scenePos()))
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
                        edge = Edge(self, item)
                        self.add_edge(edge)
                        item.add_edge(edge)
                        self.scene().addItem(edge)
                        break
                self.scene().removeItem(self.temp_edge)
                self.temp_edge = None
        super().mouseReleaseEvent(event)

class Edge(QGraphicsLineItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source = source_node
        self.dest = dest_node
        self.setPen(QPen(Qt.black, 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.adjust()

    def adjust(self):
        line = QLineF(self.source.scenePos(), self.dest.scenePos())
        self.setLine(line)

def main():
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    node1 = Node(0, 0, "Node 1")
    node2 = Node(200, 200, "Node 2")
    scene.addItem(node1)
    scene.addItem(node2)

    view = QGraphicsView(scene)
    view.show()

    def remove_selected_items():
        for item in scene.selectedItems():
            if isinstance(item, Edge):
                scene.removeItem(item)
                item.source.remove_edge(item)
                item.dest.remove_edge(item)
            elif isinstance(item, Node):
                for edge in item.edges[:]:
                    scene.removeItem(edge)
                    edge.source.remove_edge(edge)
                    edge.dest.remove_edge(edge)
                scene.removeItem(item)

    class CustomView(QGraphicsView):
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Delete:
                remove_selected_items()
            super().keyPressEvent(event)

    view = CustomView(scene)
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
