from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from PySide6.QtCore import *
import sys
from const import *
from collections import defaultdict


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowIcon(QIcon("./GUI_python/icon.png"))
        self.result = []
        self.count = 0
        #! mode selector
        self.mode = "Comparison"
        self.mode_label = QLabel("Select a mode", self)
        self.select_mode = QComboBox()
        self.select_mode.addItems(MODE)
        self.select_mode.currentIndexChanged.connect(self.mode_changed)

        self.init_UI()

    def init_UI(self):

        centre = QWidget()
        self.setCentralWidget(centre)

        #! title
        label = QLabel("Sorting Algorithm Tester", self)
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("padding:20px;")

        #! setting parameters (min, max , size)
        l_min = QLabel("Min", self)
        l_min.setFont(QFont("Arial", 15))
        l_min.setAlignment(Qt.AlignCenter)

        l_max = QLabel("Max", self)
        l_max.setFont(QFont("Arial", 15))
        l_max.setAlignment(Qt.AlignCenter)

        l_size = QLabel("Size", self)
        l_size.setFont(QFont("Arial", 15))
        l_size.setAlignment(Qt.AlignCenter)

        self.min = QSpinBox()
        self.min.setFont(QFont("Arial", 15))
        self.min.setMinimum(0)
        self.min.setMaximum(100)

        self.max = QSpinBox()
        self.max.setFont(QFont("Arial", 15))
        self.max.setMinimum(0)
        self.max.setMaximum(1000)
        self.max.setValue(100)

        if (self.mode == "Time"):
            self._size = QTextEdit()
            self._size.setFont(QFont("Arial", 15))
            self._size.setMaximumSize(300, 30)
            self._size.setText(DEFAULT_SIZES)
        else:
            self._size = QSpinBox()
            self._size.setFont(QFont("Arial", 15))
            self._size.setMinimum(1000)
            self._size.setMaximum(50000)
            self._size.setValue(10000)
        #! select algorithm
        l2 = QLabel("Select a sorting algorithm", self)
        l2.setFont(QFont("Arial", 12))
        l2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.select = QListWidget()
        self.select.setFont(QFont("Arial", 15))
        self.select.setMaximumHeight(180)
        for algo in ALGORITHMS:
            item = QListWidgetItem(algo)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            self.select.addItem(item)

        #! run
        self.button = QPushButton("Run", self)
        self.button.setFont(QFont("Arial", 15))
        self.button.clicked.connect(self.run)

        #! Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumWidth(300)
        self.terminal.setFont(QFont("Arial", 12))
        self.terminal.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; padding: 5px;"
        )
        #!Charts
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chartView = ZoomPanChartView(self.chart)
        self.chartView.setMinimumHeight(400)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        #! progress bar
        self.progress = QProgressBar()
        self.progress.setMinimumHeight(40)
        self.progress.setRange(0, 0)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.hide()
        self.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #555;
                    border-radius: 8px;
                    text-align: center;
                    background: #2b2b2b;
                    color: white;
                    height: 18px;
                }
                QProgressBar::chunk {
                    background-color: #00bcd4;
                    width: 20px;
                    margin: 1px;
                }
                """)

        #! layout
        vbox = QVBoxLayout()
        vbox.setContentsMargins(50, 50, 50, 50)
        vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        vbox.setSpacing(10)
        vbox.addWidget(label)
        vbox.addWidget(self.mode_label)
        vbox.addWidget(self.select_mode)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 20)
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(l_min)
        hbox.addWidget(self.min)
        hbox.addWidget(l_max)
        hbox.addWidget(self.max)
        hbox.addWidget(l_size)
        hbox.addWidget(self._size)

        vbox.addLayout(hbox)
        vbox.addWidget(l2)
        vbox.addWidget(self.select)
        vbox.addWidget(self.button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.terminal)
        hbox2.addWidget(self.chartView)
        vbox.addLayout(hbox2)
        centre.setLayout(vbox)

    def mode_changed(self, i):
        self.mode = self.select_mode.currentText()
        self.init_UI()

    def get_selected(self):
        selected = []
        for i in range(self.select.count()):
            item = self.select.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        return selected

    def run(self):
        print("running")
        self.button.setDisabled(True)
        if (self.mode == "Time"):
            self.sizes = [int(s.strip())
                          for s in self._size.toPlainText().split(",") if s != ""]
            self.progress.setValue(0)
            self.progress.show()
            i = 0
            for size in self.sizes:
                i += 1
                self.run_engine_time(self.min.value(), self.max.value(),
                                     size, self.get_selected())
        else:

            self.run_engine(self.min.value(), self.max.value(),
                            self._size.value(), self.get_selected())

    def run_engine_time(self, min, max, size, algo_list):
        process = QProcess()
        process.readyReadStandardOutput.connect(
            lambda: self.process_output(process))
        process.finished.connect(lambda: self.process_finished(size))
        process.start(ENGINE_PATH, [str(min), str(max), str(size), *algo_list])

    def run_engine(self, min, max, size, algo_list):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(
            lambda: self.process_output(self.process))
        self.process.finished.connect(self.process_finished)
        self.process.start(ENGINE_PATH, [str(min), str(max), str(
            size), *algo_list])
        self.progress.setValue(0)
        self.progress.show()

    def process_output(self, process):
        output = process.readAllStandardOutput().data().decode("utf-8")
        if (output.strip().startswith("PROGRESS") and self.mode == "Comparison"):
            self.progress.setValue(
                int((output.strip().split(" : ")[1]).split("\n")[0]))
            print(output.strip("PROGRESS : 100\n"))
        self.terminal.setText(output.strip("PROGRESS : 100\n"))

    def process_finished(self, size=0):
        if (self.mode == "Time"):
            result = self.parse_results(self.terminal.toPlainText())
            for r in result:
                self.result.append(
                    {"name": r, "size": size, "time": result[r]})
            self.count += 1
            self.progress.setValue((self.count / len(self.sizes))*100)
            if (self.count == len(self.sizes)):
                self.terminal.setText("")
                total_time = {}
                for r in self.result:
                    if r["name"] not in total_time:
                        total_time[r["name"]] = 0
                    total_time[r["name"]] += r["time"]
                total_time = dict(sorted(total_time.items(),
                                         key=lambda x: x[1]))
                for t in total_time:
                    self.terminal.setText(self.terminal.toPlainText(
                    ) + t + " : " + str(total_time[t]) + "ms\n")

                self.progress.hide()
                self.button.setDisabled(False)
                self.set_chart_time(self.result)
                self.result = []
                self.count = 0
        else:
            self.button.setDisabled(False)
            self.set_chart_comparison(
                self.parse_results(self.terminal.toPlainText()))
            self.progress.hide()

    def parse_results(self, output):
        results = {}
        for line in output.split("\n"):
            if (":" not in line):
                continue
            algo, time = line.split(" : ")
            results[algo] = int(time.split("ms")[0])
        if ("PROGRESS" in results):
            results.pop("PROGRESS")
        return results

    def set_chart_time(self, results):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Group results by algorithm name
        grouped = defaultdict(list)
        for entry in results:
            grouped[entry["name"]].append(entry)

        # Add one QLineSeries per algorithm
        all_x, all_y = [], []
        for name, values in grouped.items():
            # sort by input size
            values = sorted(values, key=lambda x: x["size"])
            series = QLineSeries()
            series.setName(name)
            for v in values:
                series.append(v["size"], v["time"])
                all_x.append(v["size"])
                all_y.append(v["time"])
            self.chart.addSeries(series)

        self.chart.setTitle("Sorting Algorithm Runtimes (ms)")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # X Axis (Input Size)
        axisX = QValueAxis()
        axisX.setTitleText("Input Size")
        axisX.setLabelFormat("%d")
        axisX.setRange(min(all_x), max(all_x))
        self.chart.addAxis(axisX, Qt.AlignBottom)

        # Y Axis (Runtime)
        axisY = QValueAxis()
        axisY.setTitleText("Runtime (ms)")
        axisY.setLabelFormat("%d")
        axisY.setRange(0, max(all_y))
        self.chart.addAxis(axisY, Qt.AlignLeft)

        # Attach all series to both axes
        for series in self.chart.series():
            series.attachAxis(axisX)
            series.attachAxis(axisY)

    def set_chart_comparison(self, results):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QBarSeries()

        bars = []
        for algo, value in results.items():
            bar_set = QBarSet(algo)
            bar_set.append(value)
            bars.append(bar_set)
        series.append(bars)
        self.chart.addSeries(series)
        self.chart.setTitle("Sorting Algorithm Runtime (ms)")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # X Axis (categories = algorithm names)
        axisX = QBarCategoryAxis()
        axisX.append(["Test"])
        self.chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        # Y Axis
        axisY = QValueAxis()
        axisY.setTitleText("Runtime (ms)")
        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
