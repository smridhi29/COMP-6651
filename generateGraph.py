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
        with open("graphs/"+filename, 'w') as outFile:
            n = len(self.vertices)
            for i in range(n):
                for j in self.adjacencyList[i]:
                    if i < j:
                        outFile.write(f"{i + 1} {self.vertices[i].x} {self.vertices[i].y} "
                                      f"{j + 1} {self.vertices[j].x} {self.vertices[j].y}\n")
                        
    def saveGraphToMtxFile(self, filename):
        with open("graphs/"+filename, 'w') as outFile:
            n = len(self.vertices)
            nnz = sum(len(adj) for adj in self.adjacencyList)
            for i in range(n):
                for j in self.adjacencyList[i]:
                    if i <= j:
                        outFile.write(f"{i + 1} {j + 1}\n")