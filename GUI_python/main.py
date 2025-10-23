from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from PySide6.QtCore import *
import sys
from const import *
from collections import defaultdict

DEFAULT_FONT = QFont("Arial", 14)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowIcon(QIcon("./GUI_python/icon.png"))
        self.result = []
        self.count = 0

        #! mode selector
        self.mode = SINGLE_MODE
        self.mode_label = QLabel("Select a mode", self)
        self.select_mode = QComboBox()
        self.select_mode.setFont(DEFAULT_FONT)
        self.select_mode.setStyleSheet("padding:4px;")
        self.select_mode.addItems(MODE_NAME)
        self.select_mode.currentIndexChanged.connect(self.mode_changed)

        #! drawing UI
        self.draw_UI()

    def mode_changed(self):

        self.mode = MODE_VALUE[self.select_mode.currentText()]
        #!redrawing UI
        self.draw_UI()

    def draw_UI(self):

        #! central widget and layout
        centre = QWidget()
        self.setCentralWidget(centre)

        #! title
        label = QLabel("Sorting Algorithm Benchmark", self)
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("padding:10px;")

        #! setting parameters (min, max , size)
        parameter_info = self.get_label(
            "Set Parameters", font=QFont("Arial", 10), align=Qt.AlignLeft)

        #!Min
        l_min = self.get_label("minimum", font=QFont("Arial", 10))
        self.min = self.get_range_input(MIN_LIMIT, 0, 0)
        min_box = self.get_box(l_min, self.min)
        #!Max
        l_max = self.get_label("maximum", font=QFont("Arial", 10))
        self.max = self.get_range_input(0, MAX_LIMIT, 100)
        max_box = self.get_box(l_max, self.max)
        #!Size
        l_size = self.get_label("size", font=QFont("Arial", 10))

        #! if mode is SINGLE
        if (self.mode == SINGLE_MODE):
            self._size = self.get_range_input(1, SIZE_LIMIT, 10000)

        #! if mode is MULTIPLE
        if (self.mode == MULTIPLE_MODE):
            self._size = QTextEdit()
            self._size.setFont(DEFAULT_FONT)
            self._size.setMaximumHeight(30)
            self._size.setText(DEFAULT_SIZES)
        self_box = self.get_box(l_size, self._size)

        #! select algorithm
        l2 = self.get_label("Select Algorithm")

        #! algo selector
        self.select = QListWidget()
        self.select.setFont(DEFAULT_FONT)
        self.select.setMinimumHeight(150)

        #! adding algorithms
        for algo in ALGORITHMS:
            item = QListWidgetItem(algo)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            self.select.addItem(item)

        #! run
        self.button = QPushButton("Run", self)
        self.button.setFont(DEFAULT_FONT)
        self.button.clicked.connect(self.run)

        #! Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumWidth(300)
        self.terminal.setFont(QFont("Arial", 12))
        self.terminal.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; padding: 5px; color:white;"
        )
        #!Charts
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chartView = QChartView(self.chart)
        self.chartView.setMinimumHeight(300)
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
        vbox.setSpacing(6)
        vbox.addWidget(label)
        vbox.addWidget(self.mode_label)
        vbox.addWidget(self.select_mode)

        paramenter_box = QHBoxLayout()
        paramenter_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        paramenter_box.setContentsMargins(0, 0, 0, 20)
        paramenter_box.setSpacing(50)
        paramenter_box.addLayout(min_box)
        paramenter_box.addLayout(max_box)
        paramenter_box.addLayout(self_box)

        vbox.addWidget(parameter_info)
        vbox.addLayout(paramenter_box)

        vbox.addWidget(l2)
        vbox.addWidget(self.select)
        vbox.addWidget(self.button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.terminal)
        hbox2.addWidget(self.chartView)
        vbox.addLayout(hbox2)
        centre.setLayout(vbox)

    #! drawing helper functions
    def get_range_input(self, min=10, max=100, value=0, font=DEFAULT_FONT):
        r = QSpinBox()
        r.setFont(font)
        r.setMinimum(min)
        r.setMaximum(max)
        r.setValue(value)
        return r

    def get_label(self, text, font=DEFAULT_FONT, align=Qt.AlignCenter):
        l = QLabel(text, self)
        l.setFont(font)
        l.setAlignment(align)
        return l

    def get_box(self, *x):
        box = QHBoxLayout()
        box.setDirection(QBoxLayout.RightToLeft)
        box.setAlignment(Qt.AlignmentFlag.AlignRight)
        box.setSpacing(6)
        for i in x:
            box.addWidget(i)
        return box


#! helper functions

    def get_selected(self):
        selected = []
        for i in range(self.select.count()):
            item = self.select.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        return selected


##! process functions


    def run(self):
        print("running")
        self.button.setDisabled(True)

        # if SINGLE_MODE then simply run engine once and show the result
        if (self.mode == SINGLE_MODE):
            self.run_engine(self.min.value(), self.max.value(),
                            self._size.value(), self.get_selected())

        # if MULTIPLE_MODE then run engine for each size
        if (self.mode == MULTIPLE_MODE):
            self.sizes = [int(s.strip())
                          for s in self._size.toPlainText().split(",") if s != ""]
            self.progress.setValue(0)
            self.progress.show()
            i = 0
            for size in self.sizes:
                i += 1
                self.run_engine_Mutiple(self.min.value(), self.max.value(),
                                        size, self.get_selected())

    def run_engine_Mutiple(self, min, max, size, algo_list):
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
        if (output.strip().startswith("PROGRESS") and self.mode == SINGLE_MODE):
            self.progress.setValue(
                int((output.strip().split(" : ")[1]).split("\n")[0]))
            print(output.strip("PROGRESS : 100\n"))
        self.terminal.setText(output.strip("PROGRESS : 100\n"))

    def process_finished(self, size=0):
        if (self.mode == SINGLE_MODE):
            self.button.setDisabled(False)
            result = self.parse_results(self.terminal.toPlainText())
            sorted_result = dict(sorted(result.items(), key=lambda x: x[1]))
            self.terminal.setText("")
            for r in sorted_result:
                self.terminal.setText(self.terminal.toPlainText(
                ) + r + " : " + str(sorted_result[r]) + "ms\n")
            self.set_chart_single(sorted_result)
            self.progress.hide()

        if (self.mode == MULTIPLE_MODE):
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
                self.set_chart_mutiple(self.result)
                self.result = []
                self.count = 0

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

    def set_chart_mutiple(self, results):
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

    def set_chart_single(self, results):
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
        axisX.append(["Algorithms"])
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
