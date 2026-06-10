#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_set>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: ./graph_info input.txt\n";
        return 1;
    }

    ifstream file(argv[1]);

    if (!file) {
        cerr << "Could not open file\n";
        return 1;
    }

    string line;
    long long edges = 0;
    unordered_set<int> nodes;

    while (getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;

        istringstream iss(line);
        int from, to;

        if (iss >> from >> to) {
            nodes.insert(from);
            nodes.insert(to);
            edges++;
        }
    }

    cout << "Nodes: " << nodes.size() << "\n";
    cout << "Edges: " << edges << "\n";

    return 0;
}
