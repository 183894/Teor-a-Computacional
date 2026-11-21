import re

regex_ip = r'IP=(\d{1,3}(?:\.\d{1,3}){3})'
regex_fecha = r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}'
regex_usuario = r'USER=(\w+)'
regex_evento = r'EVENT=(LOGIN_OK|LOGIN_FAIL|ACCESS)'

registros_validos = []

with open("registros.txt", "r", encoding="utf-8") as archivo:
    registros = archivo.readlines()

print("========== REGISTROS ANALIZADOS ==========")

for registro in registros:

    if not registro.strip():
        continue

    ip = re.search(regex_ip, registro)
    fecha = re.search(regex_fecha, registro)
    usuario = re.search(regex_usuario, registro)
    evento = re.search(regex_evento, registro)

    if ip and fecha and usuario and evento:

        datos = {
            "ip": ip.group(1),
            "fecha": fecha.group(),
            "usuario": usuario.group(1),
            "evento": evento.group(1)
        }

        registros_validos.append(datos)

    else:
        print("Registro no válido:", registro.strip())


# Ordenar los registros por fecha y hora

registros_validos.sort(key=lambda registro: registro["fecha"])

for registro in registros_validos:
    print(registro)


# Agrupar eventos por dirección IP

eventos_por_ip = {}

for registro in registros_validos:

    ip = registro["ip"]

    if ip not in eventos_por_ip:
        eventos_por_ip[ip] = []

    eventos_por_ip[ip].append(registro["evento"])


# Definición del AFN

transiciones = {
    "q0": {
        "LOGIN_OK": {"q0"},
        "LOGIN_FAIL": {"q0", "q1"},
        "ACCESS": {"q0"}
    },
    "q1": {
        "LOGIN_OK": set(),
        "LOGIN_FAIL": {"q2"},
        "ACCESS": set()
    },
    "q2": {
        "LOGIN_OK": set(),
        "LOGIN_FAIL": {"q3"},
        "ACCESS": set()
    },
    "q3": {
        "LOGIN_OK": {"q3"},
        "LOGIN_FAIL": {"q3"},
        "ACCESS": {"q3"}
    }
}


# Reconocimiento de secuencias mediante el AFN

print("\n========== ANALISIS DEL AFN ==========")

for ip, eventos in eventos_por_ip.items():

    estados_actuales = {"q0"}

    for evento in eventos:

        nuevos_estados = set()

        for estado in estados_actuales:
            nuevos_estados.update(transiciones[estado][evento])

        estados_actuales = nuevos_estados

    if "q3" in estados_actuales:

        print("ALERTA: Tres o más intentos fallidos consecutivos")
        print("Direccion IP:", ip)

    else:

        print("Sin patrones sospechosos en la IP:", ip)


# Definición del AFD

transiciones_afd = {
    "A": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "B",
        "ACCESS": "A"
    },
    "B": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "C",
        "ACCESS": "A"
    },
    "C": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "D",
        "ACCESS": "A"
    },
    "D": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "D",
        "ACCESS": "E"
    },
    "E": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "F",
        "ACCESS": "E"
    },
    "F": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "D",
        "ACCESS": "E"
    }
}

estados_finales = {"D", "E", "F"}


# Reconocimiento de secuencias mediante el AFD

print("\n========== ANALISIS DEL AFD ==========")

for ip, eventos in eventos_por_ip.items():

    estado_actual = "A"

    for evento in eventos:

        estado_actual = transiciones_afd[estado_actual][evento]

    if estado_actual in estados_finales:

        print("ALERTA: Tres o más intentos fallidos consecutivos")
        print("Direccion IP:", ip)
        print("Estado final:", estado_actual)

    else:

        print("Sin patrones sospechosos en la IP:", ip)
        print("Estado final:", estado_actual)
