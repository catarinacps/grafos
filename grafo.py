import re
from text_format import Color

INF = 1001
INF_CHAR = u'\u221E'


class Grafo:
    """A classe Grafo representa um grafo conexo.

    Deve receber como entrada de seu construtor um arquivo
    de texto que define as arestas e vertices ddo grafo desejado
    """

    def __init__(self, arqtexto):
        with open(arqtexto, 'r') as arq:
            self.vertices = {}

            regex = re.compile(r'[0-9]+')

            header = regex.findall(arq.readline())

            for number in range(0, int(header[0])):
                self.vertices[str(number)] = {}

            for linha in arq:
                encontrados = regex.findall(linha)

                self.vertices[encontrados[0]][encontrados[1]] = int(encontrados[2])
                self.vertices[encontrados[1]][encontrados[0]] = int(encontrados[2])

    def __str__(self):
        return self.__rep_grafo()

    def dijkstra(self, begin, end, flag_passo):
        """O metodo calcula a distancia minima entre dois nodos.

        Utilizando o algoritmo de dijkstra, o metodo imprime na tela
        a menor distancia entre os nodos recebidos como parametro.
        Opcionalmente, imprime cada passo do algoritmo caso o terceiro
        parametro contenha um True.

        Arguments:
            begin {int} -- Nodo inicial
            end {int} -- Nodo final
            flag_passo {bool} -- Flag booleana para impressao passo a passo
        """

        inicial = str(begin)
        final = str(end)
        visitados = [inicial]
        nao_visitados = list(self.vertices.keys())
        nao_visitados.remove(inicial)

        dist_inicial = {}
        for vertices in self.vertices:
            dist_inicial[vertices] = INF

        dist_inicial[inicial] = 0
        for vertice, peso in self.vertices[inicial].items():
            dist_inicial[vertice] = peso

        if flag_passo == 1:
            print(Color.BOLD + 'Nodo atual: ' + Color.END + Color.RED + inicial + Color.END)
            print(Color.BOLD + 'Nodos visitados (S)' + Color.END)
            print('{' + ', '.join(visitados) + '}')
            self.__print_tabela(dist_inicial)

        while set(visitados) != set(self.vertices):
            menor = self.__min(nao_visitados, dist_inicial)
            menor_vertice = menor[0]
            menor_distancia = menor[1]
            if menor_vertice != '':
                visitados.append(menor_vertice)
                nao_visitados.remove(menor_vertice)

                for vertice, peso in self.vertices[menor_vertice].items():
                    if peso + menor_distancia < dist_inicial[vertice]:
                        dist_inicial[vertice] = peso + menor_distancia

                if flag_passo == 1:
                    print(Color.BOLD + 'Nodo atual: ' + Color.END + Color.RED + menor_vertice + Color.END)
                    print(Color.BOLD + 'Distancia ate nodo inicial: ' +
                          Color.END + Color.BLUE + str(menor_distancia) + Color.END)
                    print(Color.BOLD + 'Nodos visitados (S)' + Color.END)
                    print('{' + ', '.join(visitados) + '}')
                    self.__print_tabela(dist_inicial)
                if menor_vertice == final:
                    break
            else:
                break
        print("\nMenor distancia: " + str(dist_inicial[final]))

    def __min(self, unvisitados, dist_inicial):
        """Retorna uma tupla contendo o vertice mais proximo e a distancia ate ele.

        Dada a lista de vertices nao visitados e a lista de distancia dos vertices
        ate o inicial, testa os nodos ainda nao visitados de dist_inicial procurando
        o mais proximo ainda nao visitado.

        Arguments:
            unvisitados {list} -- Lista de nodos ainda nao visitados
            dist_inicial {dict} -- Relacao de vertices e distancias em relacao ao inicial
        """

        minimo = INF
        menor_vertice = str()
        for vertice in unvisitados:
            dist = int(dist_inicial[vertice])
            if dist < minimo and dist > 0:
                minimo = dist
                menor_vertice = vertice

        return (menor_vertice, minimo)

    def __rep_grafo(self):
        string = ''
        for nodo, arestas in self.vertices.items():
            string += nodo + '\n'
            for vizinho, peso in arestas.items():
                string += '  ' + '-> ' + vizinho + \
                    '  (peso: ' + str(peso) + ')\n'
        return string

    def __print_tabela(self, dist_inicial):
        print(Color.BOLD + "Tabela de distancias ate o nodo inicial:" + Color.END)
        for variavel, peso in dist_inicial.items():
            string = Color.RED + variavel + Color.END + " - "
            if peso == INF:
                string += str(INF_CHAR)
            else:
                string += str(peso)
            print(string)
        print(' ')
