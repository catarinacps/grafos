import re
INF = -1
INF_CHAR = u'\u221E'


class Grafo:
    def __init__(self, arqtexto):
        with open(arqtexto, 'r') as arq:
            self.vertices = {}

            regex = re.compile(r'[0-9]+')

            arq.readline()

            for linha in arq:
                encontrados = regex.findall(linha)
                if encontrados[0] not in self.vertices:
                    self.vertices[encontrados[0]] = {}
                if encontrados[1] not in self.vertices:
                    self.vertices[encontrados[1]] = {}

                self.vertices[encontrados[0]] = {
                    encontrados[1]: int(encontrados[2])}
                self.vertices[encontrados[1]] = {
                    encontrados[0]: int(encontrados[2])}

    def __str__(self):
        return self.__rep_grafo()

    def dijkstra(self, inicial, final):
        visitados = [inicial]
        unvistidados = list(self.vertices.keys())
        unvistidados.remove(inicial)

        dist_inicial = {}
        for vertices in self.vertices:
            dist_inicial[vertices] = INF

        dist_inicial[inicial] = 0

        for vertice, peso in self.vertices[inicial].items():
            dist_inicial[vertice] = peso

            while set(visitados) != set(self.vertices):
                menor = self.__min(unvistidados, dist_inicial)

                visitados.append(menor)
                unvistidados.remove(menor)

                if final != menor:
                    for vertice, peso in self.vertices[menor].items():
                        dist_inicial[vertice] = peso
                        print(vertice + ' ' + peso)
                else:
                    break

    def __min(self, unvistidados, dist_inicial):
        minimo = INF
        for vertice in unvistidados:
            dist = dist_inicial[vertice]
            if dist < minimo and dist > 0:
                minimo = dist

        return minimo

    def __rep_grafo(self):
        string = ''
        for nodo, arestas in self.vertices.items():
            string += nodo + '\n'
            for vizinho, peso in arestas.items():
                string += '  ' + '-> ' + vizinho + \
                    '  (peso: ' + str(peso) + ')\n'
        return string
