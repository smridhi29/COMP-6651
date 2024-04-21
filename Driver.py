import random
from collections import defaultdict
from AStarLSP import Astar
from DFSLSP import DFS
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.adjList = defaultdict(list)
        self.vertices = set()

    def addEdge(self, u, v):
        self.adjList[u].append(v)
        self.adjList[v].append(u)
        self.vertices.update([u, v])

    def DFS(self, v, visited, component):
        visited.add(v)
        component.append(v)
        for neighbor in self.adjList[v]:
            if neighbor not in visited:
                self.DFS(neighbor, visited, component)

    def findLCC(self):
        visited = set()
        largestComponent = []
        for v in self.vertices:
            if v not in visited:
                component = []
                self.DFS(v, visited, component)
                if len(component) > len(largestComponent):
                    largestComponent = component
        return largestComponent
    
    def readGraphFromFile(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                u, v = map(int, line.strip().split())
                self.addEdge(u, v)
    
    def readGraphFromFilePos(self, filename):
        edges=[]
        with open(filename, 'r') as file:
            for line in file:
                components = line.strip().split()
                u = int(components[0])
                x1, y1 = map(float, components[1:3])
                v = int(components[3])
                x2, y2 = map(float, components[4:])
                # print("u=",u)
                self.addEdge(u, v)
                edges.append((int(u), x1, y1, int(v), x2, y2))
        return edges
    
    def visualize(self):
        
        plt.figure(figsize=(8, 6)) 

       
        nodes = list(self.vertices)  
        x_coords = [v[0] for v in nodes] 
        y_coords = [v[1] for v in nodes]  

        # Draw edges
        for vertex, neighbors in self.adjList.items():
            x1, y1 = vertex[0], vertex[1]  
            for neighbor in neighbors:
                x2, y2 = neighbor[0], neighbor[1] 
                plt.plot([x1, x2], [y1, y2], 'b-o', alpha=0.7) 

        
        plt.scatter(x_coords, y_coords, color='red', s=50, alpha=0.7) 

        plt.title("Graph Visualization")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.axis('off')  
        plt.show()

    
def dfslsp():
    g = Graph()
    d = DFS()
    a = Astar()
    g.readGraphFromFile("graph_n300.mtx")
    lcc = g.findLCC()
    longestPathEstimate = d.searchLSP(lcc,g)
    print("Estimated longest simple path length:", longestPathEstimate)

def dijkstra():
    print("You chose option 2")

def astar():
    g = Graph()
    a = Astar()
    edges = g.readGraphFromFilePos("graph_n300.edges")
    lcc = g.findLCC()
    longestPathEstimate = a.Get_Longest_Simple_Path(lcc,edges,g)
    print("Estimated longest simple path length:", longestPathEstimate)
    
def main():
    
    options = {
    1: dfslsp,
    2: dijkstra,
    3: astar
}
    print("Welcome to Longest Simple Path Search!!")
    print("1. DFS Based LSP Search")
    print("2. Dijkstra Based LSP Search")
    print("3. A* Based LSP Search")
    print("4. Our Hueristic LSP Search")
    num = int(input("Enter your choice: "))
    selected_option = options.get(num)
    if selected_option:
        selected_option()
    else:
        print("Invalid choice")
        
if __name__ == "__main__":
    main()
