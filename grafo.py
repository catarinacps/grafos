import re
INF = -1
class Grafo: 
	def __init__(self, arqtexto):
		with open(arqtexto, 'r') as arq:
			self.vertices = defaultdict(dict)

			regex = re.compile(r'[0-9]+')

			header = arq.readline()

			for linha in arq:
				encontrados = regex.findall();
				if encontrados not in self.vertices:
					self.vertices[encontrados[0]] = {}
				if encontrados not in self.vertices:
					self.vertices[encontrados[1]] = {}

				self.vertices[encontrados[0]] = {encontrados[1]:encontrados[2]} 
				self.vertices[encontrados[1]] = {encontrados[0]:encontrados[2]}

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
			menor = minimo(self, unvistidados, dist_inicial)

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
			if  dist < minimo and dist > 0:
				minimo = dist

		return minimo



			

