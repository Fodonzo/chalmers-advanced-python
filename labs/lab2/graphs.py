class Graph:
    def __init__(self, edgelist=None):
        self._adjacency = {}
        if edgelist:
            for start, end in edgelist:
                self.add_edge(start, end)

    def __len__(self):
        return len(self._adjacency)

    def add_vertex(self, v):
        if v not in self._adjacency:
            self._adjacency[v] = []

    def add_edge(self, a, b):
        if a not in self._adjacency:
            self.add_vertex(a)
        if b not in self._adjacency:
            self.add_vertex(b)
        self._adjacency[a].append(b)

    def edges(self):
        return [(v, u) for v in self._adjacency for u in self._adjacency[v]]

    def vertices(self):
        return list(self._adjacency.keys())

    def neighbours(self, v):
        return self._adjacency.get(v, [])

    def remove_vertex(self, v):
        if v in self._adjacency:
            del self._adjacency[v]
            for neighbours in self._adjacency.values():
                if v in neighbours:
                    neighbours.remove(v)

    def remove_edge(self, a, b):
        if a in self._adjacency and b in self._adjacency[a]:
            self._adjacency[a].remove(b)

    def set_vertex_value(self, v, x):
        if v in self._adjacency:
            self._adjacency[v] = x

    def get_vertex_value(self, v):
        return self._adjacency.get(v, [])


class WeightedGraph(Graph):
    def __init__(self, edgelist=[]):
        super().__init__(edgelist)
        self.weights = {}

        for edge in edgelist:
            if len(edge) == 3:  # Ensure weights are provided
                self.weights[(edge[0], edge[1])] = edge[2]

    def get_weight(self, a, b):
        if (a, b) not in self._edges:  # Assuming self._edges stores edges
            return None
        return self._weights.get((a, b), None)  # self._weights stores edge weights

    def set_weight(self, a, b, w):
        if (a, b) in self.edges():
            self.weights[(a, b)] = w
        else:
            raise ValueError("Edge does not exist")
