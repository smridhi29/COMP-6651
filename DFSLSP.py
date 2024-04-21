import random
from collections import defaultdict

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

    def heuristicLSP(self, component):
        Lmax = 0
        trials = int(len(component) ** 0.5)
        for _ in range(trials):
            u = random.choice(component)
            v = self.findDeepestNode(u)
            w = self.findDeepestNode(v)
            Lmax = max(Lmax, w)
        return Lmax

    def findDeepestNode(self, start):
        depth = {start: 0}
        stack = [start]
        maxDepth = 0
        while stack:
            v = stack.pop()
            for neighbor in self.adjList[v]:
                if neighbor not in depth:
                    depth[neighbor] = depth[v] + 1
                    maxDepth = max(maxDepth, depth[neighbor])
                    stack.append(neighbor)
        return maxDepth

def readGraphFromFile(filename, g):
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.strip().split())
            g.addEdge(u, v)

def main():
    g = Graph()
    readGraphFromFile("graph_n300.mtx", g)
    lcc = g.findLCC()
    longestPathEstimate = g.heuristicLSP(lcc)
    print("Estimated longest simple path length:", longestPathEstimate)

if __name__ == "__main__":
    main()
