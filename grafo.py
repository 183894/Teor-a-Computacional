from collections import deque


class GrafoLogs:
    def __init__(self):
        self.grafo = {}

    def agregar_arista(self, origen, destino, peso=1):
        if origen not in self.grafo:
            self.grafo[origen] = {}

        if destino not in self.grafo[origen]:
            self.grafo[origen][destino] = 0

        self.grafo[origen][destino] += peso

    def construir_desde_registros(self, registros):
        for registro in registros:
            usuario = registro["usuario"]
            ip = registro["ip"]
            evento = registro["evento"]

            self.agregar_arista(usuario, ip)
            self.agregar_arista(ip, evento)

    def mostrar_lista_adyacencia(self):
        print("\n========== LISTA DE ADYACENCIA ==========")

        for origen, destinos in self.grafo.items():
            lista = []

            for destino, peso in destinos.items():
                lista.append((destino, peso))

            print(origen, "->", lista)

    def bfs(self, inicio):
        if inicio not in self.grafo:
            return []

        visitados = set()
        cola = deque([inicio])
        recorrido = []

        while cola:
            actual = cola.popleft()

            if actual in visitados:
                continue

            visitados.add(actual)
            recorrido.append(actual)

            for vecino in self.grafo.get(actual, {}):
                if vecino not in visitados:
                    cola.append(vecino)

        return recorrido

    def mostrar_bfs(self, inicio):
        recorrido = self.bfs(inicio)

        print("\n========== RECORRIDO BFS ==========")

        if not recorrido:
            print("No existe el vértice:", inicio)
            return

        print("Inicio:", inicio)
        print("Recorrido:", " -> ".join(recorrido))

    def mostrar_actividad_ips(self):
        print("\n========== ACTIVIDAD POR IP ==========")

        for origen, destinos in self.grafo.items():

            if self.es_ip(origen):
                total = 0

                for destino, peso in destinos.items():
                    total += peso

                print("IP:", origen)
                print("Total de eventos:", total)

                for destino, peso in destinos.items():
                    print("  ", destino, "->", peso)

    def es_ip(self, texto):
        partes = texto.split(".")

        if len(partes) != 4:
            return False

        for parte in partes:
            if not parte.isdigit():
                return False

            numero = int(parte)

            if numero < 0 or numero > 255:
                return False

        return True
