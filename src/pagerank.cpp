#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <omp.h>

using namespace std;

struct Graph {
    int n;
    long long m;
    vector<vector<int>> incoming;
    vector<int> outdegree;
};

int get_index(unordered_map<int, int>& mp, int id) {
    auto it = mp.find(id);
    if (it != mp.end()) return it->second;

    int idx = mp.size();
    mp[id] = idx;
    return idx;
}

Graph load_graph(const string& filename) {
    ifstream file(filename);

    if (!file) {
        cerr << "Could not open file\n";
        exit(1);
    }

    string line;
    vector<pair<int, int>> edges;
    unordered_map<int, int> id_to_idx;

    while (getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;

        istringstream iss(line);
        int from_id, to_id;

        if (iss >> from_id >> to_id) {
            int from = get_index(id_to_idx, from_id);
            int to = get_index(id_to_idx, to_id);
            edges.push_back({from, to});
        }
    }

    Graph g;
    g.n = id_to_idx.size();
    g.m = edges.size();
    g.incoming.assign(g.n, vector<int>());
    g.outdegree.assign(g.n, 0);

    for (auto& e : edges) {
        int from = e.first;
        int to = e.second;
        g.incoming[to].push_back(from);
        g.outdegree[from]++;
    }

    return g;
}

vector<double> pagerank(const Graph& g, int max_iter, double damping, double tol, int threads, double& elapsed, int& used_iter, double& last_diff) {
    omp_set_num_threads(threads);

    int n = g.n;
    vector<double> rank(n, 1.0 / n);
    vector<double> next_rank(n, 0.0);

    double start = omp_get_wtime();

    for (int iter = 1; iter <= max_iter; iter++) {
        double dangling_sum = 0.0;

        #pragma omp parallel for reduction(+:dangling_sum)
        for (int i = 0; i < n; i++) {
            if (g.outdegree[i] == 0) {
                dangling_sum += rank[i];
            }
        }

        double base = (1.0 - damping) / n + damping * dangling_sum / n;
        double diff = 0.0;

        #pragma omp parallel for reduction(+:diff)
        for (int i = 0; i < n; i++) {
            double sum = 0.0;

            for (int src : g.incoming[i]) {
                sum += rank[src] / g.outdegree[src];
            }

            next_rank[i] = base + damping * sum;
            diff += fabs(next_rank[i] - rank[i]);
        }

        rank.swap(next_rank);
        last_diff = diff;
        used_iter = iter;

        if (diff < tol) break;
    }

    double end = omp_get_wtime();
    elapsed = end - start;

    return rank;
}

int main(int argc, char* argv[]) {
    if (argc < 5) {
        cerr << "Usage: ./pagerank input.txt iterations damping threads\n";
        return 1;
    }

    string filename = argv[1];
    int iterations = stoi(argv[2]);
    double damping = stod(argv[3]);
    int threads = stoi(argv[4]);
    double tol = 1e-8;

    Graph g = load_graph(filename);

    double elapsed = 0.0;
    int used_iter = 0;
    double last_diff = 0.0;

    vector<double> rank = pagerank(g, iterations, damping, tol, threads, elapsed, used_iter, last_diff);

    cout << fixed << setprecision(6);
    cout << "Nodes: " << g.n << "\n";
    cout << "Edges: " << g.m << "\n";
    cout << "Threads: " << threads << "\n";
    cout << "Iterations: " << used_iter << "\n";
    cout << "Damping: " << damping << "\n";
    cout << "Time: " << elapsed << " seconds\n";
    cout << scientific << setprecision(6);
    cout << "Last diff: " << last_diff << "\n";

    vector<pair<double, int>> top;
    for (int i = 0; i < g.n; i++) {
        top.push_back({rank[i], i});
    }

    sort(top.rbegin(), top.rend());

    cout << fixed << setprecision(10);
    cout << "Top 10 PageRank values:\n";

    for (int i = 0; i < 10 && i < g.n; i++) {
        cout << i + 1 << " " << top[i].second << " " << top[i].first << "\n";
    }

    return 0;
}
