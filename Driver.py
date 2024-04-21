import random
import math
from collections import defaultdict
from AStarLSP import Astar
from DFSLSP import DFS
from generateGraph import GeometricGraph
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
    
    def findOptimalR(self, n, minFraction, maxFraction):
        low = 0
        high = math.sqrt(2)
        while high - low > 0.001:
            mid = (low + high) / 2
            graph = GeometricGraph(n)
            graph.addEdges(mid)
            lccSize = graph.largestConnectedComponent()
            if lccSize < minFraction * n:
                low = mid
            elif lccSize > maxFraction * n:
                high = mid
            else:
                break
        return mid
    
    def getlccdegrees(self, edges, lcc):

        mdegree = 0
        total_degree = 0
        node_count = 0

        # Perform BFS starting from the LCC node
        for node in lcc:
            visited = set()
            queue = [node]
            while queue:
                current_node = queue.pop(0)
                visited.add(current_node)
                mdegree = max(mdegree, len(self.adjList[current_node]))
                total_degree += len(self.adjList[current_node])
                node_count += 1
                for neighbor in self.adjList[current_node]:
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)

        adegree = total_degree / node_count if node_count != 0 else 0

        return mdegree, adegree    

def generate():
    g= Graph()
    
    n300 = 300
    optimalR300 = g.findOptimalR(n300, 0.9, 0.95)
    print("Optimal r for n = 300:", optimalR300)
    graph300 = GeometricGraph(n300)
    graph300.addEdges(optimalR300)
    graph300.saveGraphToFile("graph_n300.edges")
    graph300.saveGraphToMtxFile("graph_n300.mtx")

    # Graph with n = 400
    n400 = 400
    optimalR400 = g.findOptimalR(n400, 0.8, 0.9)
    print("Optimal r for n = 400:", optimalR400)
    graph400 = GeometricGraph(n400)
    graph400.addEdges(optimalR400)
    graph400.saveGraphToFile("graph_n400.edges")
    graph400.saveGraphToMtxFile("graph_n400.mtx")
    
    # Graph with n = 500
    n500 = 500
    optimalR500 = g.findOptimalR(n500, 0.7, 0.8)
    print("Optimal r for n = 500:", optimalR500)
    graph500 = GeometricGraph(n500)
    graph500.addEdges(optimalR500)
    graph500.saveGraphToFile("graph_n500.edges")
    graph500.saveGraphToMtxFile("graph_n500.mtx")

def dfslsp():
    g = Graph()
    d = DFS()
    a = Astar()
    g.readGraphFromFile("graph_n300.mtx")
    lcc = g.findLCC()
    longestPathEstimate = d.searchLSP(lcc,g)
    print("Estimated longest simple path length:", longestPathEstimate)
    
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
    
def our():
    print("You chose option 2")    
    
def main():
    
    options = {
    1: generate,
    2: dfslsp,
    3: dijkstra,
    4: astar,
    5: our
}
    print("Welcome to Longest Simple Path Search!!")
    print("1. Generate Graphs with n=300, 400 and 500")
    print("2. DFS Based LSP Search")
    print("3. Dijkstra Based LSP Search")
    print("4. A* Based LSP Search")
    print("5. Our Hueristic LSP Search")
    num = int(input("Enter your choice: "))
    selected_option = options.get(num)
    if selected_option:
        selected_option()
    else:
        print("Invalid choice")
        
if __name__ == "__main__":
    main()
