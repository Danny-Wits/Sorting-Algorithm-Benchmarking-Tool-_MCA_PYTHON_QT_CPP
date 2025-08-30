#ifndef SORTING_ALGORITHM
#define SORTING_ALGORITHM
#include <vector>
using namespace std;

class SortingAlgorithm
{

public:
    string name;
    virtual void sort(vector<int> &arr) = 0;
    virtual ~SortingAlgorithm() {}
};

class BubbleSort : public SortingAlgorithm
{
public:
    BubbleSort()
    {
        this->name = "BubbleSort";
    }
    void sort(vector<int> &arr) override
    {
        // cout << "BubbleSort" << endl;
        for (int i = 0; i < arr.size() - 1; i++)
        {
            for (int j = 0; j < arr.size() - i - 1; j++)
            {
                if (arr[j] > arr[j + 1])
                {
                    swap(arr[j], arr[j + 1]);
                }
            }
        }
    };
};
class OptimizedBubbleSort : public SortingAlgorithm
{
public:
    OptimizedBubbleSort()
    {
        this->name = "OptimizedBubbleSort";
    }
    void sort(vector<int> &arr) override
    {
        // cout << "OptimizedBubbleSort" << endl;
        bool swapped = true;

        for (int i = 0; i < arr.size() - 1 && swapped; i++)
        {
            swapped = false;
            for (int j = 0; j < arr.size() - i - 1; j++)
            {
                if (arr[j] > arr[j + 1])
                {
                    swap(arr[j], arr[j + 1]);
                    swapped = true;
                }
            }
        }
    };
};

class InsertionSort : public SortingAlgorithm
{
public:
    InsertionSort()
    {
        this->name = "InsertionSort";
    }
    void sort(vector<int> &arr) override
    {
        // cout << "InsertionSort" << endl;
        for (int i = 1; i < arr.size(); i++)
        {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key)
            {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    };
};

class SelectionSort : public SortingAlgorithm
{
public:
    SelectionSort()
    {
        this->name = "SelectionSort";
    }
    void sort(vector<int> &arr) override
    {
        // cout << "SelectionSort" << endl;
        for (int i = 0; i < arr.size() - 1; i++)
        {
            int min = i;
            for (int j = i + 1; j < arr.size(); j++)
            {
                if (arr[j] < arr[min])
                {
                    min = j;
                }
            }
            swap(arr[i], arr[min]);
        }
    }
};

class MergeSort : public SortingAlgorithm
{
public:
    MergeSort()
    {
        this->name = "MergeSort";
    }
    void sort(vector<int> &arr) override
    {
        static bool first = true;
        if (first)
        {
            // cout << "MergeSort" << endl;
            first = false;
        }
        if (arr.size() <= 1)
            return;
        int mid = arr.size() / 2;
        vector<int> left(arr.begin(), arr.begin() + mid);
        vector<int> right(arr.begin() + mid, arr.end());
        sort(left);
        sort(right);
        merge(arr, left, right);
    };
    void merge(vector<int> &arr, vector<int> &left, vector<int> &right)
    {
        int i = 0, j = 0, k = 0;
        while (i < left.size() && j < right.size())
        {
            if (left[i] < right[j])
            {
                arr[k++] = left[i++];
            }
            else
            {
                arr[k++] = right[j++];
            }
        }
        while (i < left.size())
        {
            arr[k++] = left[i++];
        }
        while (j < right.size())
        {
            arr[k++] = right[j++];
        }
    }
};

class QuickSort : public SortingAlgorithm
{
public:
    QuickSort()
    {
        this->name = "QuickSort";
    }
    void sort(vector<int> &arr) override
    {
        // cout << "QuickSort" << endl;
        quickSort(arr, 0, arr.size() - 1);
    };
    void quickSort(vector<int> &arr, int low, int high)
    {
        if (low < high)
        {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    int partition(vector<int> &arr, int low, int high)
    {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j <= high - 1; j++)
        {
            if (arr[j] < pivot)
            {
                i++;
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i + 1], arr[high]);
        return i + 1;
    }
};
SortingAlgorithm *getAlgorithm(string name)
{
    if (name == "MergeSort")
        return new MergeSort();
    if (name == "InsertionSort")
        return new InsertionSort();
    if (name == "SelectionSort")
        return new SelectionSort();
    if (name == "BubbleSort")
        return new BubbleSort();
    if (name == "QuickSort")
        return new QuickSort();
    if (name == "OptimizedBubbleSort")
        return new OptimizedBubbleSort();
    return nullptr;
}

#endif