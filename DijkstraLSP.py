import heapq
from collections import defaultdict

class Dijkstra:
    def initialize(self, g):
            nodeMap = {}
            for v in g:
                v.distance = float("-inf")  # Distance value
                v.parent = None  # Predecessor
                nodeMap[v.node] = v
            return nodeMap
    
    def searchLSP(self, g, start, lcc):
            nodeMap = self.initialize(lcc)
            unvisited = set(lcc)
            start.distance = 0
            vlcc = 0

            while unvisited:
                farthest = max(unvisited, key=lambda vertex: vertex.distance)
                unvisited.remove(farthest)

                for neighbor in g.adjList[farthest.node]:
                    if nodeMap[neighbor] in unvisited:
                        new_distance = max(nodeMap[neighbor].distance, farthest.distance + 1)
                        self.relax(farthest, nodeMap[neighbor], new_distance)

            
            longest_path = []
            current = max(lcc, key=lambda vertex: vertex.distance)
            while current:
                longest_path.append(current)
                current = current.parent

            return longest_path

    def relax(self, farthest, neighbor, new_distance):
            if new_distance > neighbor.distance:
                neighbor.distance = new_distance
                neighbor.parent = farthest