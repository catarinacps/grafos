from grafo import Grafo
import os
import sys


entrada = Grafo(os.path.abspath(sys.argv[1]))
entrada.dijkstra()