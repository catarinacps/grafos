class Grafo: 
	def __init__(self, arqtexto):
		with open(arqtexto, 'r') as arq:
			self.vertices = defaultdict(dict)
			

			regex = re.compile(r'[0-9]+ | [0-9]+')
			

