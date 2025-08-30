# Sorting Algorithm Benchmarking Tool

## 📌 Overview

This project is a **benchmarking tool** that measures and compares the execution time of different sorting algorithms.
It combines:

- **Engine (C++)** – Implements the sorting algorithms and executes benchmarks.
- **GUI (Python + PySide6)** – Provides a simple interface to trigger the engine and visualize results.

The GUI and engine communicate via **command-line arguments** and **stdout parsing**.

---

## 🎯 Features

- Sorting algorithms implemented in **C++**
- Execution time measurement in **milliseconds**
- GUI built with **PySide6**
- Bar chart comparison of runtimes using **QtCharts**
- Dark mode chart styling
- Progress bar during engine execution

---

## 📂 Project Structure

```
SortingBenchmark/
│
├── Engine_cpp/               # C++ Benchmarking Engine
│   ├── engine.cpp             # Main entry point
│   ├── sorting_algorithms.h   # Sorting algorithm implementations
│   ├── file_manager.h         # File helpers
│   └── engine.exe             # Compiled executable
│
├── GUI_python/               # Python GUI (PySide6)
│   ├── main.py                # Main GUI application
│   ├── const.py               # Constants/config
│
└── README.md                  # Documentation
```

---

## ⚙️ How It Works

1. The **GUI** triggers the engine (`engine.exe`) with specific arguments such as algorithm name and input size.
2. The **engine** runs the sorting algorithm(s) and prints execution times to **stdout**.
3. The **GUI** parses this output and plots results on a **bar chart**.

---

## 🚀 Running the Project

### 1. Build the C++ Engine

```bash
cd Engine_cpp
g++ engine.cpp -o engine.exe
```

### 2. Run the Python GUI

Install dependencies:

```bash
pip install PySide6
```

Run GUI:

```bash
cd GUI_python
python main.py
```

---

## 📊 Example Workflow

- User selects one or more algorithms.
- Engine executes them and outputs results like:

  ```
  BubbleSort 150
  QuickSort 40
  MergeSort 60
  ```

- GUI displays this data in a **bar chart** for comparison.

---

## 📖 Notes

- Created as part of an **MCA Assignment**.
- Focus is on **benchmarking**, not on step-wise visualization.
- Can be extended with additional algorithms or larger datasets.

---
