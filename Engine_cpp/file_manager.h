#ifndef FILE_MANAGER
#define FILE_MANAGER
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;
class File
{
private:
    string path;

public:
    File() {};
    File(string path)
    {
        this->path = path;
        FILE *file = fopen(path.c_str(), "a");
        if (file == NULL)
        {
            cout << "Error opening file" << endl;
        }
        fclose(file);
    }

    string read()
    {
        ifstream file_stream(path);
        if (!file_stream)
        {
            cout << "Error reading file" << endl;
        }
        string content, line;

        while (getline(file_stream, line))
        {
            content += line + "\n";
        }
        file_stream.close();
        return content;
    };
    bool write(string content)
    {
        ofstream file_stream(path);
        if (!file_stream)
        {
            cout << "Error finding file" << endl;
            return false;
        }
        file_stream << content;
        file_stream.close();
        return true;
    };
    bool append(string content)
    {
        ofstream file_stream(path, ios::app);
        if (!file_stream)
        {
            cout << "Error finding file" << endl;
            return false;
        }
        file_stream << content;
        file_stream.close();
        return true;
    }
};

#endif