from collections import deque


class GrafoLogs:

    # Crear un grafo vacío
    def __init__(self):
        self.grafo = {}

    # Agregar una conexión entre dos vértices
    def agregar_arista(self, origen, destino, peso=1):

        # Si el origen no existe, se crea
        if origen not in self.grafo:
            self.grafo[origen] = {}

        # Si la conexión no existe, inicia con peso 0
        if destino not in self.grafo[origen]:
            self.grafo[origen][destino] = 0

        # Aumentar el peso de la conexión
        self.grafo[origen][destino] += peso

    # Construir el grafo usando los registros válidos
    def construir_desde_registros(self, registros):

        # Recorrer cada registro
        for registro in registros:

            # Obtener usuario, IP y evento
            usuario = registro["usuario"]
            ip = registro["ip"]
            evento = registro["evento"]

            # Conectar usuario con su IP
            self.agregar_arista(usuario, ip)

            # Conectar IP con el evento realizado
            self.agregar_arista(ip, evento)

    # Mostrar las conexiones del grafo
    def mostrar_lista_adyacencia(self):

        print("\n========== LISTA DE ADYACENCIA ==========")

        # Recorrer cada vértice y sus conexiones
        for origen, destinos in self.grafo.items():

            # Lista donde se guardarán las conexiones
            lista = []

            # Recorrer los destinos y sus pesos
            for destino, peso in destinos.items():
                lista.append((destino, peso))

            # Mostrar el origen, destino y peso
            print(origen, "->", lista)

    # Recorrer el grafo usando BFS
    def bfs(self, inicio):

        # Si el vértice no existe, regresar una lista vacía
        if inicio not in self.grafo:
            return []

        # Guardar los vértices que ya fueron visitados
        visitados = set()

        # Crear una cola comenzando desde el vértice inicial
        cola = deque([inicio])

        # Guardar el orden del recorrido
        recorrido = []

        # Mientras haya vértices en la cola
        while cola:

            # Sacar el primer vértice de la cola
            actual = cola.popleft()

            # Si ya fue visitado, no procesarlo otra vez
            if actual in visitados:
                continue

            # Marcarlo como visitado
            visitados.add(actual)

            # Guardarlo en el recorrido
            recorrido.append(actual)

            # Obtener sus vecinos
            for vecino in self.grafo.get(actual, {}):

                # Agregar a la cola los que no han sido visitados
                if vecino not in visitados:
                    cola.append(vecino)

        # Regresar el recorrido completo
        return recorrido

    # Mostrar el resultado del recorrido BFS
    def mostrar_bfs(self, inicio):

        # Ejecutar BFS desde el vértice indicado
        recorrido = self.bfs(inicio)

        print("\n========== RECORRIDO BFS ==========")

        # Si no existe el vértice
        if not recorrido:
            print("No existe el vértice:", inicio)
            return

        # Mostrar desde dónde comenzó el recorrido
        print("Inicio:", inicio)

        # Mostrar los vértices visitados
        print("Recorrido:", " -> ".join(recorrido))

    # Mostrar cuánta actividad tiene cada IP
    def mostrar_actividad_ips(self):

        print("\n========== ACTIVIDAD POR IP ==========")

        # Recorrer todos los vértices del grafo
        for origen, destinos in self.grafo.items():

            # Comprobar si el vértice es una IP
            if self.es_ip(origen):

                # Variable para contar los eventos
                total = 0

                # Sumar los pesos de todos sus eventos
                for destino, peso in destinos.items():
                    total += peso

                # Mostrar la IP y su cantidad de eventos
                print("IP:", origen)
                print("Total de eventos:", total)

                # Mostrar cada evento y cuántas veces ocurrió
                for destino, peso in destinos.items():
                    print("  ", destino, "->", peso)

    # Comprobar si un texto tiene formato de IP válida
    def es_ip(self, texto):

        # Separar la IP usando los puntos
        partes = texto.split(".")

        # Una IP debe tener exactamente 4 partes
        if len(partes) != 4:
            return False

        # Revisar cada número de la IP
        for parte in partes:

            # Verificar que sea un número
            if not parte.isdigit():
                return False

            # Convertirlo a entero
            numero = int(parte)

            # Cada número debe estar entre 0 y 255
            if numero < 0 or numero > 255:
                return False

        # Si todo es correcto, es una IP válida
        return True
