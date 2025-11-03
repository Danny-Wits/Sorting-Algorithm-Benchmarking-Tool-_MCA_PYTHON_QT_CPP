#include <iostream>
#include <sstream>
#include <map>
#include <string>
#include <chrono>
#include "file_manager.h"
#include "sorting_algorithm.h"
using namespace std;

class Engine
{
private:
    File f;
    SortingAlgorithm *algo;

public:
    static const char delimiter = '\n';
    Engine(File file, SortingAlgorithm *algo)
    {
        this->f = file;
        this->algo = algo;
    }

    int run()
    {
        string content = f.read();
        vector<int> arr = string_to_vector(content);
        auto start = chrono::high_resolution_clock::now();
        algo->sort(arr);
        auto end = chrono::high_resolution_clock::now();
        content = vector_to_string(arr);
        f.write(content);
        int execution_time = chrono::duration_cast<chrono::milliseconds>(end - start).count();
        return execution_time;
    }
    static string map_to_string(map<string, int> map)
    {
        string result = "";
        for (auto it = map.begin(); it != map.end(); it++)
        {
            result += it->first + " : " + to_string(it->second) + "ms" + "\n";
        }
        return result;
    }

    vector<int> &string_to_vector(string str)
    {
        static vector<int> result;
        result.clear();
        string token;
        istringstream tokenStream(str);
        while (getline(tokenStream, token, delimiter))
        {
            result.push_back(stoi(token));
        }
        return result;
    }
    static string vector_to_string(vector<int> arr)
    {
        string result = "";
        for (int i = 0; i < arr.size(); i++)
        {
            result += to_string(arr[i]) + delimiter;
        }
        return result;
    }
};
class RandomNumberGenerator
{
public:
    static int generate(int min, int max)
    {
        return rand() % (max - min + 1) + min;
    }
};
class FileFiller
{
public:
    static void fill_with_random(int min, int max, int size, vector<File> files)
    {
        string content;
        for (int i = 0; i < size; i++)
        {
            content += to_string(RandomNumberGenerator::generate(min, max)) + Engine::delimiter;
        }
        for (File file : files)
        {
            file.write(content);
        }
    }
};

class Tester
{
public:
    static map<string, int> &test(vector<SortingAlgorithm *> algorithms, int min = 0, int max = 10, int size = 1000)
    {
        vector<File> files;
        static map<string, int> results;
        results.clear();

        for (SortingAlgorithm *algo : algorithms)
        {
            File f("test_" + (*algo).name + ".txt");
            files.push_back(f);
        }
        FileFiller::fill_with_random(min, max, size, files);
        for (int i = 0; i < algorithms.size(); i++)
        {
            Engine engine(files[i], algorithms[i]);
            int execution_time = engine.run();
            cout << "PROGRESS : " + to_string((int)((i + 1.0) / algorithms.size() * 100)) << endl;
            results.insert({algorithms[i]->name, execution_time});
        }
        return results;
    }
};
int main(int argc, char *argv[])
{
    if (argc <= 1)
    {
        cout << "No Arguments provided : Need min max size ...algorithm_list" << endl;
        return 1;
    }
    int min, max, size;
    try
    {
        min = atoi(argv[1]);
        max = atoi(argv[2]);
        size = atoi(argv[3]);
    }
    catch (exception e)
    {
        cout << "Invalid Arguments : Need min max size ...algorithm_list" << endl;
        return 1;
    }

    vector<SortingAlgorithm *> algorithms;
    for (int i = 4; i < argc; i++)
    {
        SortingAlgorithm *temp = getAlgorithm(argv[i]);
        if (temp != nullptr)
        {
            algorithms.push_back(temp);
        }
    }
    if (algorithms.size() == 0)
    {
        algorithms.push_back(new MergeSort());
        algorithms.push_back(new InsertionSort());
        algorithms.push_back(new SelectionSort());
        algorithms.push_back(new BubbleSort());
        algorithms.push_back(new QuickSort());
        algorithms.push_back(new OptimizedBubbleSort());
    }
    auto result = Tester::test(algorithms, min, max, size);
    cout << Engine::map_to_string(result) << endl;
    auto resultFile = File("results.txt");

    resultFile.append("\n___________________________________\n");
    resultFile.append("\n" + to_string(min) + " " + to_string(max) + " " + to_string(size) + "\n");
    resultFile.append(Engine::map_to_string(result));
    resultFile.append("\n___________________________________\n");

    return 0;
}
