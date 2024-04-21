import random
import math

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GeometricGraph:
    def __init__(self, n):
        self.vertices = [Vertex(random.random(), random.random()) for _ in range(n)]
        self.adjacencyList = [[] for _ in range(n)]

    def addEdges(self, r):
        n = len(self.vertices)
        for i in range(n):
            for j in range(i + 1, n):
                if self.euclideanDistance(self.vertices[i], self.vertices[j]) <= r:
                    self.adjacencyList[i].append(j)
                    self.adjacencyList[j].append(i)

    def largestConnectedComponent(self):
        n = len(self.vertices)
        visited = [False] * n
        max_size = 0
        for i in range(n):
            if not visited[i]:
                size = [0]
                self.dfs(i, visited, size)
                max_size = max(max_size, size[0])
        return max_size

    def dfs(self, vertex, visited, size):
        visited[vertex] = True
        size[0] += 1
        for neighbor in self.adjacencyList[vertex]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, size)

    def euclideanDistance(self, u, v):
        return math.sqrt((u.x - v.x) ** 2 + (u.y - v.y) ** 2)

    def saveGraphToFile(self, filename):
        with open(filename, 'w') as outFile:
            n = len(self.vertices)
            for i in range(n):
                for j in self.adjacencyList[i]:
                    if i < j:
                        outFile.write(f"{i + 1} {self.vertices[i].x} {self.vertices[i].y} "
                                      f"{j + 1} {self.vertices[j].x} {self.vertices[j].y}\n")
                        
    def saveGraphToMtxFile(self, filename):
        with open(filename, 'w') as outFile:
            n = len(self.vertices)
            nnz = sum(len(adj) for adj in self.adjacencyList)
            for i in range(n):
                for j in self.adjacencyList[i]:
                    if i <= j:
                        outFile.write(f"{i + 1} {j + 1}\n")

def findOptimalR(n, minFraction, maxFraction):
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

if __name__ == "__main__":
    # Graph with n = 300
    n300 = 300
    optimalR300 = findOptimalR(n300, 0.9, 0.95)
    print("Optimal r for n = 300:", optimalR300)
    graph300 = GeometricGraph(n300)
    graph300.addEdges(optimalR300)
    graph300.saveGraphToFile("graph_n300.edges")
    graph300.saveGraphToMtxFile("graph_n300.mtx")

    # Graph with n = 400
    n400 = 400
    optimalR400 = findOptimalR(n400, 0.8, 0.9)
    print("Optimal r for n = 400:", optimalR400)
    graph400 = GeometricGraph(n400)
    graph400.addEdges(optimalR400)
    graph400.saveGraphToFile("graph_n400.edges")
    graph400.saveGraphToMtxFile("graph_n400.mtx")
    
    # Graph with n = 500
    n500 = 500
    optimalR500 = findOptimalR(n500, 0.7, 0.8)
    print("Optimal r for n = 500:", optimalR500)
    graph500 = GeometricGraph(n500)
    graph500.addEdges(optimalR500)
    graph500.saveGraphToFile("graph_n500.edges")
    graph500.saveGraphToMtxFile("graph_n500.mtx")
