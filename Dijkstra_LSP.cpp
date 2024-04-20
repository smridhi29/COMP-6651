#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <limits>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <algorithm>

using namespace std;

class Graph {
private:
    unordered_map<int, vector<int>> adjList;

    void InitializeSingleSourceMax(const vector<vector<int>>& graph, int source, unordered_map<int, int>& distances) {
        for (int i = 0; i < graph.size(); i++) {
            distances[i] = numeric_limits<int>::min();
        }
        distances[source] = 0;
    }

    void RelaxEdgeMax(int u, int neighbor, int weight, unordered_map<int, int>& distances, priority_queue<pair<int, int>>& pq) {
        if (distances[neighbor] < distances[u] + weight) {
            distances[neighbor] = distances[u] + weight;
            pq.push(make_pair(-distances[neighbor], neighbor));  // Use negative to simulate max-heap
        }
    }

public:
    void addEdge(int u, int v) {
        adjList[u].push_back(v);
        adjList[v].push_back(u); // Assuming undirected graph
    }

    void DFS(int v, unordered_set<int>& visited, vector<int>& component) {
        visited.insert(v);
        component.push_back(v);
        for (int neighbor : adjList[v]) {
            if (visited.find(neighbor) == visited.end()) {
                DFS(neighbor, visited, component);
            }
        }
    }

    vector<int> findLCC() {
        unordered_set<int> visited;
        vector<int> largestComponent;
        for (auto& vertex : adjList) {
            if (visited.find(vertex.first) == visited.end()) {
                vector<int> component;
                DFS(vertex.first, visited, component);
                if (component.size() > largestComponent.size()) {
                    largestComponent = component;
                }
            }
        }
        return largestComponent;
    }

    int getLongestShortestPath(const vector<int>& lcc) {
        vector<vector<int>> graph(lcc.size());
        unordered_map<int, int> indexMap;
        for (int i = 0; i < lcc.size(); i++) {
            indexMap[lcc[i]] = i;
        }
        for (int vertex : lcc) {
            for (int neighbor : adjList[vertex]) {
                if (indexMap.find(neighbor) != indexMap.end()) {
                    graph[indexMap[vertex]].push_back(indexMap[neighbor]);
                }
            }
        }

        int n_samples = static_cast<int>(sqrt(lcc.size()));
        vector<int> sources(n_samples);
        for (int i = 0; i < n_samples; i++) {
            sources[i] = indexMap[lcc[rand() % lcc.size()]];
        }

        int max_distance = numeric_limits<int>::min();
        for (int source : sources) {
            unordered_map<int, int> distances;
            InitializeSingleSourceMax(graph, source, distances);
            priority_queue<pair<int, int>> pq;
            pq.push(make_pair(0, source));
            unordered_set<int> visited;

            while (!pq.empty()) {
                auto top = pq.top();
                pq.pop();
                int u = top.second;

                if (!visited.insert(u).second) continue;

                for (int neighbor : graph[u]) {
                    RelaxEdgeMax(u, neighbor, 1, distances, pq);  // Assuming weight is 1
                }
            }

            int current_distance = max_element(distances.begin(), distances.end(),
                                               [](const auto& a, const auto& b) { return a.second < b.second; })->second;
            max_distance = max(max_distance, current_distance);
        }
        return max_distance;
    }
};

void readGraphFromFile(const string& filename, Graph& g) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        int u, v;
        float x1, y1, x2, y2;
        ss >> u >> x1 >> y1 >> v >> x2 >> y2;
        g.addEdge(u, v);
    }
}

int main() {
    Graph g;
    readGraphFromFile("graph_n300.edges", g);
    vector<int> lcc = g.findLCC();
    int longestPathEstimate = g.getLongestShortestPath(lcc);
    cout << "Estimated longest simple path length: " << longestPathEstimate << endl;
    return 0;
}
