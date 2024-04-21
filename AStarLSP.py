import random
from math import sqrt
from queue import PriorityQueue
from collections import defaultdict
import matplotlib.pyplot as plt
from heapq import heappush, heappop

class Graph:
    
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
        
    def __init__(self):
        self.adjList = defaultdict(list)
        self.vertices = set()

    def addEdge(self, u, v):
        self.adjList[u].append(v)
        self.adjList[v].append(u)
        self.vertices.update([u, v])
        
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
    
    def DFS(self, v, visited, component):
        visited.add(v)
        component.append(v)
        for neighbor in self.adjList[v]:
            if neighbor not in visited:
                self.DFS(neighbor, visited, component)
                    
    def Heuristic_Distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def Get_Longest_Simple_Path(self, lcc, edges):
        n_samples = int(sqrt(len(lcc)))
        sources = random.sample(lcc, n_samples)
        targets = random.sample(lcc, n_samples)

        max_distance = float('-inf')  

        for source in sources:
            for target in targets:
                pq = []  
                g_score = {source: 0}  
                f_score = {source: self.Heuristic_Distance((edges[source][1], edges[source][2]), (edges[target][4], edges[target][5]))}  
                heappush(pq,(-f_score[source], source))

                visited = set() 
                current_distance = 0 

                while pq: 
                    estimated_total_distance,current_node = heappop(pq)  
                    estimated_total_distance = -estimated_total_distance

                    if current_node == target: 
                        current_distance = g_score[current_node] 
                        break 

                    visited.add(current_node) 

                    for neighbor in self.adjList[current_node]: 
                        if neighbor in visited: 
                            continue

                        tentative_g_score = g_score[current_node] + 1 
                        if neighbor not in g_score or tentative_g_score > g_score[neighbor]:
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] - self.Heuristic_Distance((edges[neighbor][1], edges[neighbor][2]), (edges[neighbor][4], edges[neighbor][5]))
                            heappush(pq,(-f_score[neighbor], neighbor))

                max_distance = max(max_distance, current_distance)  
                
        return max_distance 

def readGraphFromFile(filename, g):
    edges=[]
    with open(filename, 'r') as file:
        for line in file:
            components = line.strip().split()
            u = int(components[0])
            x1, y1 = map(float, components[1:3])
            v = int(components[3])
            x2, y2 = map(float, components[4:])
            # print("u=",u)
            g.addEdge(u, v)
            edges.append((int(u), x1, y1, int(v), x2, y2))
    return edges
            
            
def main():
    g = Graph()
    edges = readGraphFromFile("graph_n300.edges", g)
    lcc = g.findLCC()
    longestPathEstimate = g.Get_Longest_Simple_Path(lcc,edges)
    print("Estimated longest simple path length:", longestPathEstimate)
    # g.visualize()

if __name__ == "__main__":
    main()