class Router:
    def __init__(self, router_id, n):
        self.router_id = router_id
        self.distance_vector = [float('inf')] * n
        self.distance_vector[router_id] = 0
        self.neighbors = {}

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def update_distance_vector(self, all_routers):
        updated = False
        for neighbor_id, cost in self.neighbors.items():
            for destination, dist in enumerate(all_routers[neighbor_id].distance_vector):
                if self.distance_vector[destination] > cost + dist:
                    self.distance_vector[destination] = cost + dist
                    updated = True
        return updated


def distance_vector_routing(network):
    routers = [Router(i, len(network)) for i in range(len(network))]
    
    for i, row in enumerate(network):
        for j, cost in enumerate(row):
            if cost != float('inf') and i != j:
                routers[i].add_neighbor(j, cost)

    updated = True
    while updated:
        updated = False
        for router in routers:
            if router.update_distance_vector(routers):
                updated = True

    # Print the final distance vectors for each router
    for router in routers:
        print(f"Router {router.router_id}'s distance vector: {router.distance_vector}")

network = [
    [0, 2, float('inf'), 1, float('inf')],
    [2, 0, 3, 2, float('inf')],
    [float('inf'), 3, 0, 4, 6],
    [1, 2, 4, 0, 2],
    [float('inf'), float('inf'), 6, 2, 0]
]

distance_vector_routing(network)
