import copy

import geopy
import networkx as nx

from database.DAO import DAO
from geopy import distance


class Model:
    def __init__(self):
        self._idMap = {}
        self._grafo = nx.Graph()
        self._years = DAO.getAllYears()
        self._shapes = []

    def _fillShapes(self, anno):
        self._shapes = DAO.getShapeYear(anno)

    def _clearShapes(self):
        self._shapes = []

    def _crea_grafo(self, forma, anno):
        self._nodes = DAO.getAllStates()
        for s in self._nodes:
            self._idMap[s.id] = s
        self._grafo.add_nodes_from(self._nodes)
        archi = DAO.getAllNeighbors()
        for a in archi:
            peso_u = DAO.getPeso(a[0], forma, anno)[0][1]
            peso_v = DAO.getPeso(a[1], forma, anno)[0][1]
            peso_arco = peso_u + peso_v
            self._grafo.add_edge(self._idMap[a[0]], self._idMap[a[1]], weight=peso_arco)

    def get_dettagli_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def peso_nodi(self):
        result = []
        for n in self._nodes:
            peso_adiacenti = 0
            vicini = self._grafo.neighbors(n)
            for v in vicini:
                peso_adiacenti += self._grafo[n][v]["weight"]
            result.append((n, peso_adiacenti))
        return result

    def _handle_percorso(self):
        self._bestPath = []
        self._bestDistanza = 0
        for n in self._nodes:
            self._ricorsione(n, [])
        return self._bestPath, self._bestDistanza

    def _ricorsione(self, nodo, parziale):
        distanza_parziale = self.getDistanzaParziale(parziale)
        if distanza_parziale > self._bestDistanza:
            self._bestDistanza = distanza_parziale
            self._bestPath = copy.deepcopy(parziale)
        vicini = self._grafo.neighbors(nodo)
        vicini_ordinati = []
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
            vicini_ordinati.append((nodo, v, peso_arco))
        vicini_ordinati.sort(key=lambda x: x[2])
        for a in vicini_ordinati:
            coord_u = (a[0].Lat, a[0].Lng)
            coord_v = (a[1].Lat, a[1].Lng)
            distanza_arco = geopy.distance.geodesic(coord_u, coord_v).kilometers
            peso_arco = self._grafo[a[0]][a[1]]["weight"]
            if len(parziale) > 0:
                peso_ultimo = self._grafo[parziale[-1][0]][parziale[-1][1]]["weight"]
                if peso_arco > peso_ultimo:
                    parziale.append((a[0], a[1], distanza_arco, peso_arco))
                    self._ricorsione(a[1], parziale)
                    parziale.pop()
            else:
                parziale.append((a[0], a[1], distanza_arco, peso_arco))
                self._ricorsione(a[1], parziale)
                parziale.pop()

    def getDistanzaParziale(self, parziale):
        totL = 0
        for a in parziale:
            totL += a[2]
        return totL
