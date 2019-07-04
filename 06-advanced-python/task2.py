"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной

Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)

"""


class Graph:
    def __init__(self, E):
        self.E = E
        self.iterable_graph = []

    def __iter__(self):
        for node in sorted(self.E.keys()):
            if node not in self.iterable_graph:
                self.iterable_graph.append(node)
            for child in self.E[node]:
                if child not in self.iterable_graph:
                    self.iterable_graph.append(child)
        return iter(self.iterable_graph)


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph = Graph(E)

for vertice in graph:
    print(vertice)
