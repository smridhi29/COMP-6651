#include <iostream>
#include <fstream>
#include <vector>
#include <limits>
#include <list>
#include <unordered_map>
#include <queue>
#include <functional>
#include <memory>
#include <string>
#include <sstream>

using namespace std;

struct Vertex {
    int id;
    double distance;  // Use double for potentially larger range of path weights
    Vertex* parent;

    Vertex(int id) : id(id), distance(-numeric_limits<double>::infinity()), parent(nullptr) {}
};

class Graph {
public:
    unordered_map<int, list<pair<int, double>>> adjacencyList;
    unordered_map<int, Vertex*> vertices;

    void addEdge(int u, int v, double weight) {
        adjacencyList[u].push_back({v, weight});
        adjacencyList[v].push_back({u, weight});
        if (vertices.find(u) == vertices.end()) vertices[u] = new Vertex(u);
        if (vertices.find(v) == vertices.end()) vertices[v] = new Vertex(v);
    }

    ~Graph() {
        for (auto& vertex : vertices) {
            delete vertex.second;
        }
    }
};

void relax(Vertex* u, int v, double weight, Graph& graph, priority_queue<pair<double, int>>& pq, unordered_map<int, bool>& inQueue) {
    Vertex* vertexV = graph.vertices[v];
    double newDist = u->distance + weight;
    if (vertexV->distance < newDist) {
        cout << "Updating distance for vertex " << v << " from " << vertexV->distance << " to " << newDist << endl;
        vertexV->distance = newDist;
        vertexV->parent = u;
        if (!inQueue[v]) {
            pq.push(make_pair(newDist, v));
            inQueue[v] = true;
        }
    }
}

void dijkstra(Graph& graph, int source) {
    unordered_map<int, bool> visited;
    unordered_map<int, bool> inQueue;
    priority_queue<pair<double, int>> pq;

    graph.vertices[source]->distance = 0;
    pq.push(make_pair(0, source));
    inQueue[source] = true;

    while (!pq.empty()) {
        auto top = pq.top(); pq.pop();
        int u = top.second;

        if (visited[u]) continue;
        visited[u] = true;
        cout << "Visiting vertex " << u << " with current longest distance " << graph.vertices[u]->distance << endl;

        for (const auto& neighbor : graph.adjacencyList[u]) {
            int v = neighbor.first;
            double weight = neighbor.second;
            if (!visited[v]) {
                relax(graph.vertices[u], v, weight, graph, pq, inQueue);
            }
        }
    }
}

void readGraphFromFile(Graph& graph, const string& filename) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        int u, v;
        double weight;
        ss >> u >> v >> weight;
        graph.addEdge(u, v, weight);
    }
}

int main() {
    Graph graph;
    string filename = "graph_n500.edges";
    readGraphFromFile(graph, filename);

    int sourceNode = 1;
    dijkstra(graph, sourceNode);

    double Lmax = -numeric_limits<double>::infinity();
    for (auto& vertexPair : graph.vertices) {
        Vertex* vertex = vertexPair.second;
        if (vertex->distance > Lmax) {
            Lmax = vertex->distance;
        }
    }

    cout << "Longest simple path length (Lmax) is " << Lmax << endl;
    return 0;
}
