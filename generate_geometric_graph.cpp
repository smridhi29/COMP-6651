#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <fstream>

using namespace std;

// Structure to hold the coordinates of a vertex
struct Vertex {
    double x, y;
};

// Class to represent a geometric graph
class GeometricGraph {
public:
    vector<Vertex> vertices;           // List of all vertices
    vector<vector<int> > adjacencyList; // Adjacency list to store edges

    // Constructor to create a graph with n vertices
    GeometricGraph(int n) {
        srand(time(0)); // Seed random number generator
        // Initialize vertices with random coordinates
        for (int i = 0; i < n; i++) {
            Vertex v;
            v.x = static_cast<double>(rand()) / RAND_MAX;
            v.y = static_cast<double>(rand()) / RAND_MAX;
            vertices.push_back(v);
            adjacencyList.push_back(vector<int>()); // Initialize adjacency list for each vertex
        }
    }

    // Add edges between vertices that are within distance r
    void addEdges(double r) {
        int n = vertices.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (euclideanDistance(vertices[i], vertices[j]) <= r) {
                    adjacencyList[i].push_back(j);
                    adjacencyList[j].push_back(i);
                }
            }
        }
    }

    // Calculate the largest connected component of the graph using DFS
    int largestConnectedComponent() {
        int n = vertices.size();
        vector<bool> visited(n, false);
        int max_size = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                int size = 0;
                dfs(i, visited, size);
                max_size = max(max_size, size);
            }
        }
        return max_size;
    }
void saveGraphToFile(const string& filename) {
        ofstream outFile(filename);  // Open file to write
    if (!outFile) {
        cerr << "Error opening file for writing." << endl;
        return;
    }

    int n = vertices.size();
    for (int i = 0; i < n; i++) {
        for (int j : adjacencyList[i]) {
            if (i < j) {  // To avoid duplicate edges in an undirected graph
                // Print both nodes and their coordinates
                outFile << (i + 1) << " " << vertices[i].x << " " << vertices[i].y << " "
                        << (j + 1) << " " << vertices[j].x << " " << vertices[j].y << endl;
            }
        }
    }
    outFile.close();  // Close the file after writing
    }
private:
    // Recursive DFS function to explore the graph
    void dfs(int vertex, vector<bool>& visited, int& size) {
        visited[vertex] = true;
        size++; // Increment size for each vertex visited

        // Visit all adjacent vertices that have not been visited
        for (int neighbor : adjacencyList[vertex]) {
            if (!visited[neighbor]) {
                dfs(neighbor, visited, size);
            }
        }
    }

    // Calculate Euclidean distance between two vertices
    double euclideanDistance(const Vertex& u, const Vertex& v) {
        return sqrt(pow(u.x - v.x, 2) + pow(u.y - v.y, 2));
    }
};

// Function to find an appropriate value of r using binary search
double findOptimalR(int n, double minFraction, double maxFraction) {
//     int n: The total number of vertices in the graph.
// double minFraction: The minimum fraction of n that the LCC should at least contain.
// double maxFraction: The maximum fraction of n that the LCC should not exceed.
    double low = 0, high = sqrt(2), mid; // high set to root 2 as that is the max possible distance in a unit sqaure as all coordiantes of points are within [0,1]
    while (high - low > 0.001) {
        mid = (low + high) / 2;
        GeometricGraph graph(n);
        graph.addEdges(mid); // edges are added between vertices that within distance of mid, edges in the graph are re-created in each iteration w new r value
        int lccSize = graph.largestConnectedComponent(); //finding size of the lcc
        if (lccSize < minFraction * n) {
            low = mid;
        } else if (lccSize > maxFraction * n) {
            high = mid;
        } else {
            break; // Found an optimal r
        }
    }
    return mid;
}


int main() {
    // Graph with n = 300
    int n300 = 300;
    double optimalR300 = findOptimalR(n300, 0.9, 0.95);
    cout << "Optimal r for n = 300: " << optimalR300 << endl;
    GeometricGraph graph300(n300);
    graph300.addEdges(optimalR300);
    graph300.saveGraphToFile("graph_n300.edges");

    // Graph with n = 400
    int n400 = 400;
    double optimalR400 = findOptimalR(n400, 0.8, 0.9);
    cout << "Optimal r for n = 400: " << optimalR400 << endl;
    GeometricGraph graph400(n400);
    graph400.addEdges(optimalR400);
    graph400.saveGraphToFile("graph_n400.edges");

    // Graph with n = 500
    int n500 = 500;
    double optimalR500 = findOptimalR(n500, 0.7, 0.8);
    cout << "Optimal r for n = 500: " << optimalR500 << endl;
    GeometricGraph graph500(n500);
    graph500.addEdges(optimalR500);
    graph500.saveGraphToFile("graph_n500.edges");
   

    return 0;
}
