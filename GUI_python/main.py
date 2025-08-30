from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from PySide6.QtCore import *
import sys
import subprocess
from const import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")
        self.setGeometry(100, 100, 800, 800)
        self.setWindowIcon(QIcon("./GUI_python/icon.png"))
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

        self.size = QSpinBox()
        self.size.setFont(QFont("Arial", 15))
        self.size.setMinimum(1000)
        self.size.setMaximum(50000)
        self.size.setValue(10000)

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

        #! Terminal Label
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumWidth(200)
        self.terminal.setFont(QFont("Arial", 12))
        self.terminal.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; padding: 5px;"
        )
        #!Charts
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        #! progress bar
        self.progress = QProgressBar()
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

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 30)
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(l_min)
        hbox.addWidget(self.min)
        hbox.addWidget(l_max)
        hbox.addWidget(self.max)
        hbox.addWidget(l_size)
        hbox.addWidget(self.size)
        vbox.addLayout(hbox)
        vbox.addWidget(l2)
        vbox.addWidget(self.select)
        vbox.addWidget(self.button)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.terminal)
        hbox2.addWidget(self.chartView)
        vbox.addLayout(hbox2)
        centre.setLayout(vbox)

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
        self.run_engine(self.min.value(), self.max.value(),
                        self.size.value(), self.get_selected())

    def run_engine(self, min, max, size, algo_list):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.process_output)
        self.process.finished.connect(self.process_finished)
        self.process.start(ENGINE_PATH, [str(min), str(max), str(
            size), *algo_list])
        self.progress.setValue(0)
        self.progress.show()

    def process_output(self):
        output = self.process.readAllStandardOutput().data().decode("utf-8")
        if (output.strip().startswith("PROGRESS")):
            self.progress.setValue(
                int((output.strip().split(" : ")[1]).split("\n")[0]))

        print(output.strip("PROGRESS : 100\n"))
        self.terminal.setText(output.strip("PROGRESS : 100\n"))

    def process_finished(self):
        self.button.setDisabled(False)
        self.set_chart(self.parse_results(self.terminal.toPlainText()))
        self.progress.hide()

    def parse_results(self, output):
        results = {}
        for line in output.split("\n"):
            if (":" not in line):
                continue
            algo, time = line.split(" : ")
            results[algo] = int(time.split("ms")[0])
        return results

    def set_chart(self, results: dict):

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
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
