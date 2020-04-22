class Graph:
    def __init__(self, triples):
        triples = [(int(s.split()[0]), s.split()[1], int(s.split()[2])) for s in triples]
        self.vertices = []
        self.edges = triples
        self.edge_labels = []
        for u, c, v in triples:
            if u not in self.vertices:
                self.vertices.append(u)
            if v not in self.vertices:
                self.vertices.append(v)
            if c not in self.edge_labels:
                self.edge_labels.append(c)

    def vertices_amount(self):
        return len(self.vertices)
