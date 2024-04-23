import random
import math
from collections import defaultdict
from AStarLSP import Astar
from DFSLSP import DFS
from DijkstraLSP import Dijkstra
from generateGraph import GeometricGraph
from OwnHeuristicLSP import OwnHeuristic
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, x, y,node):
        self.x = x
        self.y = y
        self.node = node
        self.distance = float('-inf')
        self.parent = None
        
class Graph:
    def __init__(self):
        self.adjList = defaultdict(list)
        self.verticeSet = set()
        self.vertices = []
        self.verticeMap = {}

    def addEdge(self, u, v):
        self.adjList[u].append(v)
        self.adjList[v].append(u)
        
    def addVertex(self, u, v, x1=0, y1=0, x2=0, y2=0):
        ver1 = Vertex(x1, y1, u)
        ver2 = Vertex(x2, y2, v)
        if(u not in self.verticeSet):
            self.vertices.append(ver1)
            self.verticeMap[u] = ver1
        
        if(v not in self.verticeSet):
            self.vertices.append(ver2)
            self.verticeMap[v] = ver2
        
        self.verticeSet.update([u, v])

    def DFS(self, v, visited, component, d):
        visited.add(v)
        
        if(d==1):
            component.append(self.verticeMap[v])
        else:
            component.append(v)    
        for neighbor in self.adjList[v]:
            if neighbor not in visited:
                self.DFS(neighbor, visited, component,d)

    def findLCC(self, d=0):
        visited = set()
        largestComponent = []
        # if(d==0):
        for v in self.verticeSet:
                if v not in visited:
                    component = []
                    self.DFS(v, visited, component, d)
                    if len(component) > len(largestComponent):
                        largestComponent = component    
        # else:
        #     for v in self.vertices:
        #         if v not in visited:
        #             component = []
        #             self.DFS(v, visited, component)
        #             if len(component) > len(largestComponent):
        #                 largestComponent = component
        return largestComponent
    
    def readGraphFromFile(self, filename):
        edges=[]
        with open("graphs/"+filename, 'r') as file:
            for line in file:
                components = line.strip().split()
                if(len(components)==2):
                    u, v = map(int, components)
                    self.addEdge(u, v)
                    self.addVertex(u, v)
                else:
                    u = int(components[0])
                    x1, y1 = map(float, components[1:3])
                    v = int(components[3])
                    x2, y2 = map(float, components[4:])
                    # print("u=",u)
                    self.addEdge(u, v)
                    self.addVertex(u, v, x1, y1, x2, y2)
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
    
    def getlccdegrees(self, lcc):

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
    
    with open("graphs/n_rValues", 'w') as outFile:   
        outFile.write(f"{n300} {optimalR300}\n"
                      f"{n400} {optimalR400}\n"
                      f"{n500} {optimalR500}\n")

    
def dfslsp():
    g = Graph()
    d = DFS()
    g.readGraphFromFile("graph_n300.edges")
    lcc = g.findLCC()
    longestPathEstimate = d.searchLSP(lcc,g)
    print("Estimated longest simple path length:", longestPathEstimate)

def dijkstra():
    g = Graph()
    d = Dijkstra()
    g.readGraphFromFile("graph_n300.edges")
    lcc = g.findLCC(1)
    longestPathEstimate = d.searchLSP(g, random.choice(lcc), lcc)
    print("Estimated longest simple path length:", len(longestPathEstimate))

def astar():
    g = Graph()
    a = Astar()
    edges = g.readGraphFromFile("graph_n300.edges")
    lcc = g.findLCC()
    print()
    longestPathEstimate = a.searchLSP(lcc,edges,g)
    print("Estimated longest simple path length:", longestPathEstimate)
    
def own():
    g = Graph()
    h = OwnHeuristic()  
    g.readGraphFromFile("graph_n300.edges")
    lcc = g.findLCC(1)
    longestPathEstimate = h.searchLSP(lcc, g)  
    print("Estimated longest simple path length:", longestPathEstimate)
    

def format_table(headers, data):
    # Find the maximum width for each column including headers
    column_widths = [max(len(str(row[i])) for row in data) for i in range(len(headers))]
    for i, header in enumerate(headers):
        column_widths[i] = max(column_widths[i], len(header))
    
    # Create a format string for the header and row data with the correct padding for each column
    header_format_string = " | ".join("{:^" + str(width) + "}" for width in column_widths)
    row_format_string = " | ".join("{:<" + str(width) + "}" for width in column_widths)
    
    # Create the header string
    formatted_header = ("+ " + " + ".join("-" * width for width in column_widths) + " +\n"
                        "| " + header_format_string.format(*headers) + " |\n"
                        "+=" + "=+".join("=" * width for width in column_widths) + "=+")
    
    # Apply the row format string to each row in the data
    formatted_rows = [row_format_string.format(*row) for row in data]
    
    # Join the rows into a single string with line breaks
    formatted_rows = "\n".join("| " + row + " |" for row in formatted_rows)
    
    # Combine the header and rows with the appropriate top and bottom borders
    formatted_table = (formatted_header + "\n" + formatted_rows +
                       "\n+ " + " + ".join("-" * width for width in column_widths) + " +")
    
    return formatted_table


def all():
    graphs = ['graph_n300.edges', 'graph_n400.edges', 'graph_n500.edges']
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
        
        edges = g.readGraphFromFile(graph)
        
        lcc = g.findLCC()
        dilcc = g.findLCC(1)
        olcc=g.findLCC(1)     
        
        mD, aD = g.getlccdegrees(lcc)
        
        dfslsp = d.searchLSP(lcc,g)
        dilsp = di.searchLSP(g, random.choice(dilcc), dilcc)
        alsp = a.searchLSP(lcc,edges,g)
        ownlsp = o.searchLSP(olcc,g)
        
        headers = ["Algorithm", "n", "r", "LCC Length", "Maximum Degree", "Average Degree", "LSP"]
        data = [
    ["DFS", len(g.verticeSet), "{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3])))), len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), dfslsp],
    ["Dijkstra", len(g.verticeSet), "{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3])))), len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), len(dilsp)],
    ["A*", len(g.verticeSet), "{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3])))), len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), alsp],
    ["Own Heuristic", len(g.verticeSet), "{:.3f}".format(float(extracted_values.get(int(graph[graph.index("graph_n") + len("graph_n"):][:3])))), len(lcc), "{:.2f}".format(mD), "{:.2f}".format(aD), ownlsp]
    ]        
        formatted_table = format_table(headers, data)
    
        # Print the formatted table
        print(formatted_table)
        
        max_col_widths = [max(len(str(row[i])) for row in data) for i in range(len(headers))]
    
        # Calculate the total width of the table
        total_width = sum(max_col_widths) + len(headers) * 3 + 1
        
        # Print the table
        # print("+" + "-".join(["-" * width for width in max_col_widths]) + "+")
        # print("| " + " | ".join(header.ljust(width) for header, width in zip(headers, max_col_widths)) + " |")
        # print("=" + "=+".join(["=" * width for width in max_col_widths]) + "=+")
        # for row in data:
        #     print("| " + " | ".join(str(cell).ljust(width) for cell, width in zip(row, max_col_widths)) + " |")
        # print("+" + "-".join(["-" * width for width in max_col_widths]) + "+")
    
def main():
    
    options = {
    1: generate,
    2: dfslsp,
    3: dijkstra,
    4: astar,
    5: own,
    6: all
}
    print("Welcome to Longest Simple Path Search!!")
    print("1. Generate Graphs with n=300, 400 and 500")
    print("2. DFS Based LSP Search")
    print("3. Dijkstra Based LSP Search")
    print("4. A* Based LSP Search")
    print("5. Own Hueristic LSP Search")
    print("6. Execute all Graphs")
    num = int(input("Enter your choice: "))
    selected_option = options.get(num)
    if selected_option:
        selected_option()
    else:
        print("Invalid choice")
        
if __name__ == "__main__":
    main()
