import random

ALGORITHMS = ["All", "BubbleSort", "InsertionSort",
              "MergeSort", "QuickSort", "SelectionSort"]


def random_array(size):
    return [random.randint(1, 100) for i in range(size)]


class BubbleSort:
    def __init__(self):
        self.name = "BubbleSort"

    def sort(self, arr):
        for i in range(len(arr) - 1):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]


class InsertionSort:
    def __init__(self):
        self.name = "InsertionSort"

    def sort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key


class SelectionSort:
    def __init__(self):
        self.name = "SelectionSort"

    def sort(self, arr):
        for i in range(len(arr) - 1):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]


class MergeSort:
    def __init__(self):
        self.name = "MergeSort"

    def sort(self, arr):
        if len(arr) <= 1:
            return
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        self.sort(left)
        self.sort(right)
        self.merge(arr, left, right)

    def merge(self, arr, left, right):
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


class QuickSort:
    def __init__(self):
        self.name = "QuickSort"

    def sort(self, arr):
        self.quick_sort(arr, 0, len(arr) - 1)

    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
