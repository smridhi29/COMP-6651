#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <cmath>
#include <algorithm>

using namespace std;

// Node structure to keep graph information
struct Node {
    int id;
    double distance; // Path length from source
    double heuristic; // Estimated distance to destination
    int predecessor; // Previous node in the path
    Node(int id) : id(id), distance(0), heuristic(0), predecessor(-1) {}
};

// Comparator for priority queue to make it a max-heap based on the score of Node
struct Comparison {
    bool operator()(const Node* a, const Node* b) {
        return (a->distance + a->heuristic) < (b->distance + b->heuristic);
    }
};

// Struct to return multiple results from the graph analysis
struct GraphAnalysis {
    int numNodesInLCC;
    int maxDegree;
    double averageDegree;
    int longestPathLength;
};

// Function to read the graph from a file
void readGraph(const string& filename, unordered_map<int, vector<int> >& graph) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Failed to open file." << endl;
        return;
    }
    cout << "Reading graph from file..." << endl;

    int u, v;
    double ux, uy, vx, vy;  // Position variables which we will read but not use

    while (file >> u >> ux >> uy >> v >> vx >> vy) {
        graph[u].push_back(v);
        graph[v].push_back(u); // Since the graph is undirected, add both directions
    }
    cout << "Graph loaded with " << graph.size() << " nodes." << endl;
}

// DFS function to find connected components
void dfs(int node, unordered_map<int, vector<int> >& graph, unordered_set<int>& visited, vector<int>& component) {
    visited.insert(node);
    component.push_back(node);
    for (int neighbor : graph[node]) {
        if (visited.find(neighbor) == visited.end()) {
            dfs(neighbor, graph, visited, component);
        }
    }
}

// Function to find the largest connected component
vector<int> findLargestConnectedComponent(unordered_map<int, vector<int> >& graph) {
    unordered_set<int> visited;
    vector<int> largestComponent;
    cout << "Searching for the largest connected component..." << endl;
    for (auto& pair : graph) {
        if (visited.find(pair.first) == visited.end()) {
            vector<int> component;
            dfs(pair.first, graph, visited, component);
            if (component.size() > largestComponent.size()) {
                largestComponent = component;
            }
        }
    }
    cout << "Largest component found with " << largestComponent.size() << " nodes." << endl;
    return largestComponent;
}

// Function to calculate the maximum degree of nodes in the LCC
int calculateMaxDegree(const vector<int>& lcc, const unordered_map<int, vector<int> >& graph) {
    int maxDegree = 0;
    for (int node : lcc) {
        maxDegree = max(maxDegree, static_cast<int>(graph.at(node).size()));
    }
    cout << "Maximum degree calculated: " << maxDegree << endl;
    return maxDegree;
}

// Function to calculate the average degree of nodes in the LCC
double calculateAverageDegree(const vector<int>& lcc, const unordered_map<int, vector<int> >& graph) {
    int totalEdges = 0;
    for (int node : lcc) {
        totalEdges += graph.at(node).size();
    }
    double average = static_cast<double>(totalEdges) / static_cast<double>(lcc.size());
    cout << "Average degree calculated: " << average << endl;
    return average;
}

// A* algorithm to find the longest path
// int aStar(unordered_map<int, vector<int> >& graph, vector<int>& lcc, int sourceId, int destinationId) {
//     unordered_map<int, Node*> nodes;
//     for (int id : lcc) {
//         nodes[id] = new Node(id);
//     }
//     cout << "Starting A* from node " << sourceId << " to node " << destinationId << endl;

//     nodes[sourceId]->distance = 0; // Start from the source node

//     priority_queue<Node*, vector<Node*>, Comparison> pq;
//     pq.push(nodes[sourceId]);

//     while (!pq.empty()) {
//         Node* current = pq.top();
//         pq.pop();

//         for (int neighborId : graph[current->id]) {
//             Node* neighbor = nodes[neighborId];
//             double newPathLength = current->distance + 1; // Increment path length by 1
//             if (newPathLength > neighbor->distance) {
//                 neighbor->distance = newPathLength;
//                 neighbor->predecessor = current->id;
//                 pq.push(neighbor);
//             }
//         }
//     }

//     int longestPathLength = static_cast<int>(nodes[destinationId]->distance);
//     cout << "Longest path length found: " << longestPathLength << endl;
//     return longestPathLength;
// }


// A* algorithm to find the longest path
int aStar(unordered_map<int, vector<int> >& graph, vector<int>& lcc, int sourceId, int destinationId) {
    unordered_map<int, Node*> nodes;
    for (int id : lcc) {
        nodes[id] = new Node(id);
    }
    cout << "Starting A* from node " << sourceId << " to node " << destinationId << endl;

    nodes[sourceId]->distance = 0; // Start from the source node

    priority_queue<Node*, vector<Node*>, Comparison> pq;
    pq.push(nodes[sourceId]);

    while (!pq.empty()) {
        Node* current = pq.top();
        pq.pop();

        //cout << "Processing node " << current->id << " with current distance " << current->distance << endl;

        for (int neighborId : graph[current->id]) {
            Node* neighbor = nodes[neighborId];
            double newPathLength = current->distance + 1; // Increment path length by 1
            if (newPathLength > neighbor->distance) {
                //cout << "Updating distance for node " << neighborId
                     //<< " from " << neighbor->distance << " to " << newPathLength << endl;

                neighbor->distance = newPathLength;
                neighbor->predecessor = current->id;
                pq.push(neighbor);

                //cout << "Pushing node " << neighborId << " to the priority queue with new distance " << newPathLength << endl;
            }
        }
    }

    int longestPathLength = static_cast<int>(nodes[destinationId]->distance);
    cout << "Longest path length found: " << longestPathLength << " to destination node " << destinationId << endl;
    return longestPathLength;
}

// Main function to drive the program
int main() {
    string filename = "graph_n300.txt";
    unordered_map<int, vector<int> > graph;
    readGraph(filename, graph);

    vector<int> lcc = findLargestConnectedComponent(graph);
    int sourceNode = lcc.front();
    int destinationNode = lcc.back();

    GraphAnalysis result;
    result.numNodesInLCC = lcc.size();
    result.maxDegree = calculateMaxDegree(lcc, graph);
    result.averageDegree = calculateAverageDegree(lcc, graph);
    result.longestPathLength = aStar(graph, lcc, sourceNode, destinationNode);

    cout << "Number of nodes in LCC: " << result.numNodesInLCC << endl;
    cout << "Maximum degree in LCC: " << result.maxDegree << endl;
    cout << "Average degree in LCC: " << result.averageDegree << endl;
    cout << "Longest path length found: " << result.longestPathLength << endl;

    return 0;
}
