import random
from math import sqrt
from queue import PriorityQueue
from collections import defaultdict

# from Driver import Graph
from heapq import heappush, heappop

class Astar:
    
                        
    def Heuristic_Distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def searchLSP(self, lcc, edges, g):
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

                    for neighbor in g.adjList[current_node]: 
                        if neighbor in visited: 
                            continue

                        tentative_g_score = g_score[current_node] + 1 
                        if neighbor not in g_score or tentative_g_score > g_score[neighbor]:
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] - self.Heuristic_Distance((edges[neighbor][1], edges[neighbor][2]), (edges[neighbor][4], edges[neighbor][5]))
                            heappush(pq,(-f_score[neighbor], neighbor))

                max_distance = max(max_distance, current_distance)  
                
        return max_distance 
            