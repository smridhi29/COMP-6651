import random
from collections import defaultdict

class OurHeuristic:
    def searchLSP(self, connected_comp, graph_obj):
        
        path_max = 0
        num_attempts = int(len(connected_comp) ** 0.5)  
        path_records = {}  
        for _ in range(num_attempts):
            pivot_point = random.choice(connected_comp)
            path_extent = self.findLongestFromNode(pivot_point, graph_obj, path_records)
            path_max = max(path_max, path_extent)
        return path_max

    def findLongestFromNode(self, init_point, network, path_records):
        
        exploration_stack = [(init_point, set([init_point.node]), 0)]  
        optimal_length = 0

        while exploration_stack:
            active_vertex, seen_nodes, path_len = exploration_stack.pop()
            
            if active_vertex.node in path_records and path_records[active_vertex.node] >= path_len:
                continue  

            path_records[active_vertex.node] = path_len

            
            potential_next = [n for n in network.adjList[active_vertex.node] if n not in seen_nodes]
            if not potential_next:
                optimal_length = max(optimal_length, path_len)  
            else:
                for next_node in potential_next:
                    next_vertex = network.verticeMap[next_node]
                    new_seen = set(seen_nodes)  
                    new_seen.add(next_node)
                    exploration_stack.append((next_vertex, new_seen, path_len + 1))

        return optimal_length
