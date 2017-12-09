import re

INF = 1000000
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

                self.vertices[encontrados[0]][encontrados[1]] = int(
                    encontrados[2])
                self.vertices[encontrados[1]][encontrados[0]] = int(
                    encontrados[2])

    def __str__(self):
        return self.__rep_grafo()


    def dijkstra(self, begin, end, passo):
        inicial = str(begin)
        final = str(end)
        visitados = [inicial]
        #print(list(self.vertices.keys()))
        unvistidados = list(self.vertices.keys())
        unvistidados.remove(inicial)

        dist_inicial = {}
        for vertices in self.vertices:
            dist_inicial[vertices] = INF

        dist_inicial[inicial] = 0

        for vertice, peso in self.vertices[inicial].items():
            dist_inicial[vertice] = peso
        
        #print(self.vertices[inicial].items())
        #print(dist_inicial)
        #print(self.vertices)

        while set(visitados) != set(self.vertices):
            menor = self.__min(unvistidados, dist_inicial)
            menor_vertice = menor[0]
            menor_distancia = menor[1]
            if(menor_vertice != ''):
                if(passo == 1):
                    print('Nodo atual: '+ menor_vertice)
                    print('Distancia ate nodo inicial: '+ str(menor_distancia))

                visitados.append(menor_vertice)
                if(passo):    
                    print('Nodos visitados (S)')
                    print(visitados)

                unvistidados.remove(menor_vertice)

                for vertice, peso in self.vertices[menor_vertice].items():
              	    if(peso + menor_distancia < dist_inicial[vertice]):
                        dist_inicial[vertice] = peso + menor_distancia

                if passo ==1:        
                    self.__print_tabela(dist_inicial,unvistidados)
                    print(" ")

                if(menor_vertice == final):
                	break
            else:
            	break

            #print(dist_inicial)
        print("Menor distancia: " + str(dist_inicial[final]))    
                

    def __min(self, unvisitados, dist_inicial):
        minimo = INF
        menor_vertice =  str()
        for vertice in unvisitados:
            dist = int(dist_inicial[vertice])
            if dist < minimo and dist > 0:
                minimo = dist
                menor_vertice = vertice


        return [menor_vertice, minimo]

        
    def __rep_grafo(self):
        string = ''
        for nodo, arestas in self.vertices.items():
            string += nodo + '\n'
            for vizinho, peso in arestas.items():
                string += '  ' + '-> ' + vizinho + \
                    '  (peso: ' + str(peso) + ')\n'
        return string

    def __print_tabela(self, dist_inicial, unvisitados):
    	print("Tabela de distancias ate o nodo inicial")
    	for variavel, peso in dist_inicial.items():
            if variavel in unvisitados:
                string = variavel+ " - "
                if(peso == INF):
                	string+= INF_CHAR
                else:
            	    string+= str(peso)
                print(string)
