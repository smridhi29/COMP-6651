import random
from collections import defaultdict
# from Driver import Graph

class DFS:

    def searchLSP(self, component, g):
        Lmax = 0
        trials = int(len(component) ** 0.5)
        for _ in range(trials):
            u = random.choice(component)
            v = self.findDeepestNode(u,g)
            w = self.findDeepestNode(v,g)
            Lmax = max(Lmax, w)
        return Lmax

    def findDeepestNode(self, start, g):
        depth = {start: 0}
        stack = [start]
        maxDepth = 0
        while stack:
            v = stack.pop()
            for neighbor in g.adjList[v]:
                if neighbor not in depth:
                    depth[neighbor] = depth[v] + 1
                    maxDepth = max(maxDepth, depth[neighbor])
                    stack.append(neighbor)
        return maxDepth
