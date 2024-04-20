#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cmath>
#include <ctime>
#include <algorithm>

using namespace std;

// Graph class to handle graph operations
class Graph {
private:
    unordered_map<int, vector<int> > adjList; // Adjacency list for graph representation
    unordered_set<int> vertices; // Set to keep track of all vertices

    // Recursive DFS function to explore the graph and mark components
    void DFS(int v, unordered_set<int>& visited, vector<int>& component) {
        visited.insert(v); // Mark the vertex as visited
        component.push_back(v); // Add vertex to current component
        for (int neighbor : adjList[v]) { // Go through each neighbor of vertex
            if (visited.find(neighbor) == visited.end()) { // If neighbor is not visited
                DFS(neighbor, visited, component); // Recurse into neighbor
            }
        }
    }

public:
    // Function to add an undirected edge between u and v
    void addEdge(int u, int v) {
        adjList[u].push_back(v); // Add v to the adjacency list of u
        adjList[v].push_back(u); // Add u to the adjacency list of v since it's undirected
        vertices.insert(u); // Add u to the set of vertices
        vertices.insert(v); // Add v to the set of vertices
    }

    // Function to find the largest connected component (LCC) using DFS
    vector<int> findLCC() {
        unordered_set<int> visited; // Set to track visited vertices
        vector<int> largestComponent; // Vector to store the largest component found
        for (int v : vertices) { // Iterate over all vertices
            if (visited.find(v) == visited.end()) { // If vertex has not been visited
                vector<int> component; // Temp vector to store current component
                DFS(v, visited, component); // Perform DFS to populate component
                if (component.size() > largestComponent.size()) { // Check if current component is larger than the largest found
                    largestComponent = component; // Update largest component
                }
            }
        }
        return largestComponent; // Return the largest component found
    }

    // Heuristic to estimate the longest simple path within a component
    int heuristicLSP(const vector<int>& component) {
        int Lmax = 0; // Variable to store the longest path found
        srand(time(NULL)); // Seed random number generator
        int trials = sqrt(component.size()); // Determine number of trials based on component size
        for (int i = 0; i < trials; ++i) {
            int u = component[rand() % component.size()]; // Pick a random vertex
            int v = findDeepestNode(u); // Find deepest node from u
            int w = findDeepestNode(v); // Find deepest node from v
            Lmax = max(Lmax, w); // Update Lmax if current depth is greater
        }
        return Lmax; // Return the estimated longest path length
    }

    // Function to find the deepest node from a start node using DFS
    int findDeepestNode(int start) {
        unordered_map<int, int> depth; // Map to store depth of each node
        depth[start] = 0; // Initialize start node depth
        vector<int> stack(1, start); // Use a vector as a stack for DFS
        int maxDepth = 0; // Variable to store maximum depth found
        while (!stack.empty()) { // Process until stack is empty
            int v = stack.back(); // Get top vertex
            stack.pop_back(); // Remove top vertex
            for (int neighbor : adjList[v]) { // Iterate through neighbors
                if (depth.find(neighbor) == depth.end()) { // If neighbor has not been visited
                    depth[neighbor] = depth[v] + 1; // Set depth of neighbor
                    maxDepth = max(maxDepth, depth[neighbor]); // Update max depth if necessary
                    stack.push_back(neighbor); // Push neighbor onto stack
                }
            }
        }
        return maxDepth; // Return the maximum depth found
    }
};

// Function to read graph from file
void readGraphFromFile(const string& filename, Graph& g) {
    //for geometric graphs only
    // ifstream file(filename); // Open the file
    // string line; // String to store each line
    // while (getline(file, line)) { // Read lines until end of file
    //     stringstream ss(line); // Use stringstream to parse the line
    //     int u, v;
    //     float x1, y1, x2, y2;
    //     ss >> u >> x1 >> y1 >> v >> x2 >> y2; // Parse integers and floats
    //     g.addEdge(u, v); // Add an edge to the graph
    // }

    ifstream file(filename); // Open the file
    string line; // String to store each line
    while (getline(file, line)) { // Read lines until end of file
        stringstream ss(line); // Use stringstream to parse the line
        int u, v;
        ss >> u >> v; // Parse the two integers representing the edge
        g.addEdge(u, v); // Add an edge to the graph
    }
}
// }

// Main function
int main() {
    Graph g; // Create a Graph instance
    readGraphFromFile("DSJC500-5.mtx", g); // Read graph from the specified file
    vector<int> lcc = g.findLCC(); // Find the largest connected component
    int longestPathEstimate = g.heuristicLSP(lcc); // Estimate the longest simple path
    cout << "Estimated longest simple path length: " << longestPathEstimate << endl; // Output the result
    return 0; // Return from main
}
