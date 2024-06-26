import random
import math
from collections import defaultdict
# Import pathfinding algorithms
from AStarLSP import Astar
from DFSLSP import DFS
from DijkstraLSP import Dijkstra
from generateGraph import GeometricGraph
from OwnHeuristicLSP import OwnHeuristic
import matplotlib.pyplot as plt

class Vertex:
    # Initialize a graph vertex with coordinates and a node identifier
    def __init__(self, x, y, node):
        self.x = x
        self.y = y
        self.node = node
        self.distance = float('-inf')  # Used for distance calculations in pathfinding
        self.parent = None  # Pointer to parent vertex in a path

class Graph:
    # Initialize an empty graph with adjacency list and set of vertices
    def __init__(self):
        self.adjList = defaultdict(list)
        self.verticeSet = set()
        self.vertices = []
        self.verticeMap = {}

    # Add an edge between two vertices u and v in the graph
    def addEdge(self, u, v):
        self.adjList[u].append(v)
        self.adjList[v].append(u)
        
    # Add vertex with optional coordinates to the graph
    def addVertex(self, u, v, x1=0, y1=0, x2=0, y2=0):
        ver1 = Vertex(x1, y1, u)
        ver2 = Vertex(x2, y2, v)
        if u not in self.verticeSet:
            self.vertices.append(ver1)
            self.verticeMap[u] = ver1
        
        if v not in self.verticeSet:
            self.vertices.append(ver2)
            self.verticeMap[v] = ver2
        
        self.verticeSet.update([u, v])

    # Recursive DFS to find components in the graph
    def DFS(self, v, visited, component, d):
        visited.add(v)
        
        if d == 1:
            component.append(self.verticeMap[v])
        else:
            component.append(v)    
        for neighbor in self.adjList[v]:
            if neighbor not in visited:
                self.DFS(neighbor, visited, component, d)

    # Find the largest connected component in the graph
    def findLCC(self, d=0):
        visited = set()
        largestComponent = []
        for v in self.verticeSet:
            if v not in visited:
                component = []
                self.DFS(v, visited, component, d)
                if len(component) > len(largestComponent):
                    largestComponent = component    
        return largestComponent
    
    # Read graph from file to create edges and vertices
    def readGraphFromFile(self, filename):
        edges = []
        with open("graphs/"+filename, 'r') as file:
            for line in file:
                components = line.strip().split()
                if len(components) == 2:
                    u, v = map(int, components)
                    self.addEdge(u, v)
                    self.addVertex(u, v)
                else:
                    u = int(components[0])
                    x1, y1 = map(float, components[1:3])
                    v = int(components[3])
                    x2, y2 = map(float, components[4:])
                    self.addEdge(u, v)
                    self.addVertex(u, v, x1, y1, x2, y2)
                    edges.append((int(u), x1, y1, int(v), x2, y2))
        return edges    
    
    # Visualize the graph using matplotlib
    def visualize(self):
        
        plt.figure(figsize=(8, 6)) 
        
        nodes = list(self.vertices)  
        x_coords = [v.x for v in nodes] 
        y_coords = [v.y for v in nodes]  
        for vertex, neighbors in self.adjList.items():
            x1 = self.verticeMap[vertex].x
            y1 = self.verticeMap[vertex].y
            for neighbor in neighbors:
                x2 = self.verticeMap[neighbor].x
                y2 = self.verticeMap[neighbor].y
                plt.plot([x1, x2], [y1, y2], 'b-o', alpha=0.7) 

        
        plt.scatter(x_coords, y_coords, color='red', s=50, alpha=0.7) 
        for vertex in nodes:
            plt.annotate(vertex.node, (vertex.x,vertex.y), textcoords="offset points", xytext=(0, 10), ha='center')
        
        plt.title("Graph Visualization")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.axis('off')  
        plt.show()
    
    # Find optimal radius for connectivity using binary search
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
    
    # Calculate maximum and average degrees of vertices in the largest connected component
    def getlccdegrees(self, lcc):
        mdegree = 0
        total_degree = 0
        node_count = 0

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
    
    with open("graphs/n_rValues", 'w') as outFile:   
        outFile.write(f"{n300} {optimalR300}\n"
                      f"{n400} {optimalR400}\n"
                      f"{n500} {optimalR500}\n")

    
def dfslsp():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges', 'DSJC500-5.mtx', 'inf-euroroad.edges', 'inf-power.mtx']
    extracted_values = {}
    with open("graphs/n_rValues", 'r') as file:
            for line in file:
                components = line.strip().split()
                extracted_values[int(components[0])] = float(components[1])
                    
    for i, graph in enumerate(graphs):
        g = Graph()
        d = DFS()
        print("For the graph: "+graph+" , below are the results for DFS Algorithm")   
        if(i>=3):
            print("\033[3mAs the graph is large, results are generating, please wait....\033[0m")  
        edges = g.readGraphFromFile(graph)
        lcc = g.findLCC()
        
        mD, aD = g.getlccdegrees(lcc)
        
        if(i<3):
            r="{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3]))))
        else:
            r="-"    
        
        dfslsp = d.searchLSP(lcc,g)
        
        headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
        data = [
    ["DFS", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), dfslsp]
    ]        
        formatted_table = format_table(headers, data)
    
        
        print()
        # Print the formatted table
        print(formatted_table)
        print()

def dijkstra():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges', 'DSJC500-5.mtx', 'inf-euroroad.edges', 'inf-power.mtx']
    extracted_values = {}
    with open("graphs/n_rValues", 'r') as file:
            for line in file:
                components = line.strip().split()
                extracted_values[int(components[0])] = float(components[1])
                    
    for i, graph in enumerate(graphs):
        g = Graph()
        di = Dijkstra()
        print("For the graph: "+graph+" , below are the results for Dijkstra Algorithm")    
        if(i>=3):
            print("\033[3mAs the graph is large, results are generating, please wait....\033[0m")  
        edges = g.readGraphFromFile(graph)
        lcc = g.findLCC()
        dilcc = g.findLCC(1)
        mD, aD = g.getlccdegrees(lcc)
        
        if(i<3):
            r="{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3]))))
        else:
            r="-"    
            
        dilsp = di.searchLSP(g, random.choice(dilcc), dilcc)
        
        headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
        data = [
    ["Dijkstra", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), len(dilsp)]
    ]        
        formatted_table = format_table(headers, data)
    
        print()
        # Print the formatted table
        print(formatted_table)
        print()

def astar():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges']
    extracted_values = {}
    with open("graphs/n_rValues", 'r') as file:
            for line in file:
                components = line.strip().split()
                extracted_values[int(components[0])] = float(components[1])
                    
    for i, graph in enumerate(graphs):
        if(i<3):
            g = Graph()
            a = Astar()
            
            edges = g.readGraphFromFile(graph)
            
            lcc = g.findLCC()
            
            mD, aD = g.getlccdegrees(lcc)
            
            if(i<3):
                r="{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3]))))
            else:
                r="-"    
                
            if(i<3):
                alsp = a.searchLSP(lcc,edges,g)
            else:
                alsp = "N/A"
            
            headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
            data = [
        ["A*", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), alsp]
        ]        
            formatted_table = format_table(headers, data)
        
            print("For the graph: "+graph+" , below are the results for each Algorithm")
            print()
            # Print the formatted table
            print(formatted_table)
            print()
    
def own():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges', 'DSJC500-5.mtx', 'inf-euroroad.edges', 'inf-power.mtx']
    extracted_values = {}
    with open("graphs/n_rValues", 'r') as file:
            for line in file:
                components = line.strip().split()
                extracted_values[int(components[0])] = float(components[1])
                    
    for i, graph in enumerate(graphs):
        g = Graph()
        o= OwnHeuristic()
        print("For the graph: "+graph+" , below are the results for our Own Algorithm")    
        if(i>=3):
            print("\033[3mAs the graph is large, results are generating, please wait....\033[0m")    
        edges = g.readGraphFromFile(graph)
        lcc = g.findLCC()
        olcc=g.findLCC(1)     
        
        mD, aD = g.getlccdegrees(lcc)
        
        if(i<3):
            r="{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3]))))
        else:
            r="-"
                    
        ownlsp = o.searchLSP(olcc,g)
        
        headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
        data = [
    ["Own Heuristic", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), ownlsp]
    ]        
        formatted_table = format_table(headers, data)
    
        print()
        # Print the formatted table
        print(formatted_table)
        print()
    

def format_table(headers, data):
        
    column_widths = [max(len(str(row[i])) for row in data) for i in range(len(headers))]
    for i, header in enumerate(headers):
        column_widths[i] = max(column_widths[i], len(header))
    
    header_format_string = " | ".join("{:^" + str(width) + "}" for width in column_widths)
    row_format_string = " | ".join("{:<" + str(width) + "}" for width in column_widths)
    
    formatted_header = ("+ " + " + ".join("-" * width for width in column_widths) + " +\n"
                        "| " + header_format_string.format(*headers) + " |\n"
                        "+ " + " + ".join("=" * width for width in column_widths) + " +")
    
    formatted_rows = [row_format_string.format(*row) for row in data]
    
    formatted_rows = "\n".join("| " + row + " |" for row in formatted_rows)
    
    formatted_table = (formatted_header + "\n" + formatted_rows +
                       "\n+ " + " + ".join("-" * width for width in column_widths) + " +")
    
    return formatted_table


def all():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges', 'DSJC500-5.mtx', 'inf-euroroad.edges', 'inf-power.mtx']
    extracted_values = {}
    with open("graphs/n_rValues", 'r') as file:
            for line in file:
                components = line.strip().split()
                extracted_values[int(components[0])] = float(components[1])
                    
    for i, graph in enumerate(graphs):
        g = Graph()
        d = DFS()
        di = Dijkstra()
        a = Astar()
        o= OwnHeuristic()
        print("For the graph: "+graph+" , below are the results for each Algorithm")
        if(i>=3):
            print("\033[3mAs the graph is large, results are generating, please wait....\033[0m")  
        edges = g.readGraphFromFile(graph)
        
        lcc = g.findLCC()
        dilcc = g.findLCC(1)
        olcc=g.findLCC(1)     
        
        mD, aD = g.getlccdegrees(lcc)
        
        if(i<3):
            r="{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3]))))
        else:
            r="-"    
            
        dfslsp = d.searchLSP(lcc,g)
        dilsp = di.searchLSP(g, random.choice(dilcc), dilcc)
        if(i<3):
            alsp = a.searchLSP(lcc,edges,g)
        else:
            alsp = "N/A"
        ownlsp = o.searchLSP(olcc,g)
        
        headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
        data = [
    ["DFS", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), dfslsp],
    ["Dijkstra", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), len(dilsp)],
    ["A*", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), alsp],
    ["Own Heuristic", len(g.verticeSet), r, len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), ownlsp]
    ]        
        formatted_table = format_table(headers, data)
    
        
        print()
        # Print the formatted table
        print(formatted_table)
        print()
        
    
def main():
    options = {
        1: generate,
        2: dfslsp,
        3: dijkstra,
        4: astar,
        5: own,
        6: all
    }

    while True:
        print("\nWelcome to Longest Simple Path Search!!")
        print("1. Generate Graphs with n=300, 400 and 500")
        print("2. DFS Based LSP Search")
        print("3. Dijkstra Based LSP Search")
        print("4. A* Based LSP Search")
        print("5. Own Heuristic LSP Search")
        print("6. Execute all Graphs")
        print("7. Exit")
        print("\033[3mPlease note that generating results for online graphs requires some time as the graphs are large in nature.\033[0m")

        
        try:
            num = int(input("Enter your choice (Choose option 6 for complete analysis): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if num == 7:
            print("Exiting program.")
            break
        
        selected_option = options.get(num)
        if selected_option:
            selected_option()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
    