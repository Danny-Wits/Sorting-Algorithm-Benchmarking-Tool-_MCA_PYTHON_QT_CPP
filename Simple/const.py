from PySide6.QtCharts import *
from PySide6.QtGui import *

ENGINE_PATH = "./Engine_cpp/engine.exe"
ALGORITHMS = ["BubbleSort", "InsertionSort",
              "MergeSort", "QuickSort", "SelectionSort", "OptimizedBubbleSort"]
MODE_NAME = ["Comparison of Algorithms on same dataset ",
             "Comparison of Algorithms on different datasets"]
MODE_VALUE = {MODE_NAME[0]: "Comparison", MODE_NAME[1]: "Time"}
DEFAULT_SIZES = "10000, 20000, 30000, 40000, 50000"


# Custom Class for Zooming and Panning
class ZoomPanChartView(QChartView):

    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setDragMode(QChartView.ScrollHandDrag)
        self._last_pos = None

    # --- Panning ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._last_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._last_pos is not None and event.buttons() & Qt.LeftButton:
            delta = event.pos() - self._last_pos
            self.chart().scroll(-delta.x(), delta.y())
            self._last_pos = event.pos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._last_pos = None
        super().mouseReleaseEvent(event)

    # --- Zooming with scroll wheel ---
    def wheelEvent(self, event):
        zoom_in_factor = 1.2
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.chart().zoom(zoom_in_factor)   # zoom in
        else:
            self.chart().zoom(zoom_out_factor)  # zoom out
