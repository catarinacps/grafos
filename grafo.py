import re
from text_format import Color

"""Pacote da implementacao de um grafo em Python.

Contem todas as dependencias para o funcionamento correto da classe.
"""


INF = 1001
INF_CHAR = u'\u221E'


class Grafo:
    """A classe Grafo representa um grafo simples.

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

        # Inicializacao do nodo inicial
        inicial = str(begin)
        # Inicializacao do nodo final
        final = str(end)

        # Inicializacao da lista de nodos visitados
        visitados = [inicial]
        # E a inicializacao da lista de nodos nao visitados, para auxilio na execucao
        nao_visitados = list(self.vertices.keys())
        nao_visitados.remove(inicial)

        # A relacao de distancias ao nodo inicial e representada por um dicionario
        dist_inicial = {}
        # onde cada vertice e uma chave, e o valor desse vertice e a distancia ate o inicial
        for vertices in self.vertices:
            dist_inicial[vertices] = INF

        dist_inicial[inicial] = 0
        # No primeiro passo do algoritmo, ocorre a avaliacao dos nodos vizinhos ao inicial
        for vertice, peso in self.vertices[inicial].items():
            # e, assim, inicializamos as chaves do dicionario de distancias vizinhas ao inicial
            # com o peso de suas arestas
            dist_inicial[vertice] = peso

        # Aqui ocorre a impressao do primeiro passo do algoritmo, caso o usuario tenha escolhido
        # a execucao passo a passo.
        if flag_passo == 1:
            print(Color.BOLD + 'Nodo atual: ' + Color.END + Color.RED + inicial + Color.END)
            print(Color.BOLD + 'Nodos visitados (S):' + Color.END)
            print('{' + ', '.join(visitados) + '}')
            self.__print_tabela(dist_inicial)

        # Enquanto o conjunto de nodos visitados nao for igual ao conjunto de vertices...
        while set(visitados) != set(self.vertices):
            menor = self.__min(nao_visitados, dist_inicial)
            menor_vertice = menor[0]
            menor_distancia = menor[1]
            # e existir um vertice com uma distancia menor que infinito (representada no codigo
            # por existir uma distancia nao vazia)...
            if menor_vertice != '':
                # Comecamos a execucao do passo adicionando o vertice mais proximo do que estavamos
                visitados.append(menor_vertice)
                nao_visitados.remove(menor_vertice)

                # E, para cada vertice vizinho ao vertice que estamos olhando
                for vertice, peso in self.vertices[menor_vertice].items():
                    # Testamos se o peso dessa aresta + a distancia ate o nodo que estamos e menor
                    # que a distancia do nodo inicial ate o vertice que essa aresta leva a
                    if peso + menor_distancia < dist_inicial[vertice]:
                        # Se for menor, redefinimos a distancia do nodo incial ate esse vertice
                        # com a soma anterior
                        dist_inicial[vertice] = peso + menor_distancia

                # Aqui ocorre a impressao do passo da execucao, se o usuario escolheu tal opcao
                if flag_passo == 1:
                    # Nodo atual da execucao...
                    print(Color.BOLD + 'Nodo atual: ' + Color.END +
                          Color.RED + menor_vertice + Color.END)
                    # distancia desse nodo ate o incial...
                    print(Color.BOLD + 'Distancia ate nodo inicial: ' +
                          Color.END + Color.BLUE + str(menor_distancia) + Color.END)
                    # e o conjunto de nodos visitados...
                    print(Color.BOLD + 'Nodos visitados (S):' + Color.END)
                    print('{' + ', '.join(visitados) + '}')
                    # assim como a tabela de distancias ate o nodo incial
                    self.__print_tabela(dist_inicial)
                # Finalmente, se o nodo atual for o nodo desejado, terminamos o processamento
                if menor_vertice == final:
                    break
            # Se nao existir um nodo mais proximo ao nodo anteriormente executado, tambem terminamos
            # o processamento
            else:
                break
        # E, ao terminar, ocorre a impressao na tela da menor distancia do nodo inicial ao final
        print("\nMenor distancia entre " + Color.BOLD + inicial + Color.END + ' e ' + Color.BOLD +
              final + Color.END + ': ' + Color.CYAN + str(dist_inicial[final]) + Color.END)

    def __min(self, nao_visitados, dist_inicial):
        """Retorna uma tupla contendo o vertice mais proximo e a distancia ate ele.

        Dada a lista de vertices nao visitados e a lista de distancia dos vertices
        ate o inicial, testa os nodos ainda nao visitados de dist_inicial procurando
        o mais proximo ainda nao visitado.

        Arguments:
            nao_visitados {list} -- Lista de nodos ainda nao visitados
            dist_inicial {dict} -- Relacao de vertices e distancias em relacao ao inicial
        """

        # Para encontrar o vertice mais proximo, inicializamos variaveis auxiliares
        minimo = INF
        # com a distancia "infinita"
        menor_vertice = str()
        # e com o vertice indefinido

        # Para cada vertice ainda nao visitado
        for vertice in nao_visitados:
            dist = int(dist_inicial[vertice])
            # Verificamos a distancia ate ele e menor que a distancia atualmente na variavel aux
            if dist < minimo and dist > 0:
                minimo = dist
                menor_vertice = vertice

        # Ao testar todos os nodos nao visitados, retornamos o mais proximo
        return (menor_vertice, minimo)

    def __rep_grafo(self):
        string = Color.CYAN + 'Representacao do grafo:' + Color.END + '\n'
        for nodo, arestas in self.vertices.items():
            string += Color.BOLD + nodo + Color.END + '\n'
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
        print('')
