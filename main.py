import re
#Expresiones regulares
regex_ip = r'IP=(\d{1,3}(?:\.\d{1,3}){3})'
regex_fecha = r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}'
regex_usuario = r'USER=(\w+)'
regex_evento = r'EVENT=(LOGIN_OK|LOGIN_FAIL|ACCESS|LOGOUT|SU|EXIT)'
#comprobar que la direccion IP tenga cuatro numeros separador ppr puntos y que cada uno este entre 0 y 255
def validar_ip(ip):
    partes = ip.split(".")

    if len(partes) != 4:
        return False

    for parte in partes:
        numero = int(parte)

        if numero < 0 or numero > 255:
            return False

    return True

registros_validos = []#lista donde se alamcenan los registros que sean validos

#abir el archivo que contiene los registros
with open("registros.txt", "r", encoding="utf-8") as archivo:
    registros = archivo.readlines()#para leer todas las lineas del archivo

print("========== REGISTROS ANALIZADOS ==========")
#recorrer cada registro del archivo para comprobar su formato
for registro in registros:
    #ignorar lineas vacias
    if not registro.strip():
        continue
     # Buscar la IP, fecha, usuario y evento dentro del registro
    ip = re.search(regex_ip, registro)
    fecha = re.search(regex_fecha, registro)
    usuario = re.search(regex_usuario, registro)
    evento = re.search(regex_evento, registro)
    #comprobar que se encontraron todos los datos y que la ip sea valida
    if ip and fecha and usuario and evento and validar_ip(ip.group(1)):
        #guardar la informacion encontrada en un diccionario
        datos = {
            "ip": ip.group(1),
            "fecha": fecha.group(),
            "usuario": usuario.group(1),
            "evento": evento.group(1)
        }
        #agregar el registro a la lista de registros validos
        registros_validos.append(datos)

    else:
        #mostrar los registros que no cumplen con el formato
        print("Registro no válido:", registro.strip())


# Ordenar los registros por fecha y hora
registros_validos.sort(key=lambda registro: registro["fecha"])
#mostrar los registros que fueron aceptados
for registro in registros_validos:
    print(registro)


# Agrupar eventos por dirección IP
eventos_por_ip = {}
#recorrer los registros validos para agrupar sus eventos
for registro in registros_validos:
    #obtener la direccion ip del registro actual
    ip = registro["ip"]
    #si la ip no existe en el diccionario se crea una lista vacia
    if ip not in eventos_por_ip:
        eventos_por_ip[ip] = []
    #agregar el evento a la lista correspondiente de esa ip
    eventos_por_ip[ip].append(registro["evento"])


# Definición del AFN

transiciones = {
    "q0": {
        "LOGIN_OK": {"q0"},
        "LOGIN_FAIL": {"q0", "q1"},
        "ACCESS": {"q0"},
        "LOGOUT": {"q0"},
        "SU": {"q0"},
        "EXIT": {"q0"}
    },
    "q1": {
        "LOGIN_OK": set(),
        "LOGIN_FAIL": {"q2"},
        "ACCESS": set(),
        "LOGOUT": set(),
        "SU": set(),
        "EXIT": set()
    },
    "q2": {
        "LOGIN_OK": set(),
        "LOGIN_FAIL": {"q3"},
        "ACCESS": set(),
        "LOGOUT": set(),
        "SU": set(),
        "EXIT": set()
    },
    "q3": {
        "LOGIN_OK": {"q3"},
        "LOGIN_FAIL": {"q3"},
        "ACCESS": {"q3"},
        "LOGOUT": {"q3"},
        "SU": {"q3"},
        "EXIT": {"q3"}
    }
}


# Reconocimiento de secuencias mediante el AFN

print("\n========== ANALISIS DEL AFN ==========")
#recorrer cada ip y su lista de eventos
for ip, eventos in eventos_por_ip.items():
    #iniciar el automata en el estado q0
    estados_actuales = {"q0"}
    #leer cada evento de la secuencia de esa IP
    for evento in eventos:
        #Crear un conjunto para guardar los nuevos estados
        nuevos_estados = set()
        #revisar las transiciones de cada estado actual
        for estado in estados_actuales:
            nuevos_estados.update(transiciones[estado][evento])
        #actualizar los estados despues de procesar el evento
        estados_actuales = nuevos_estados
    #comprobar si se alcanza el estado de acepatcion q3
    if "q3" in estados_actuales:
        #mostar alerta si se detectaron tres o mas fallos consecutivos
        print("ALERTA: Tres o más intentos fallidos consecutivos")
        print("Direccion IP:", ip)

    else:
        #informar que no se encontro secuencia sospechosa
        print("Sin patrones sospechosos en la IP:", ip)


# Definición del AFD

transiciones_afd = {
    "A": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "B",
        "ACCESS": "A",
        "LOGOUT": "A",
        "SU": "A",
        "EXIT": "A"
    },
    "B": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "C",
        "ACCESS": "A",
        "LOGOUT": "A",
        "SU": "A",
        "EXIT": "A"
    },
    "C": {
        "LOGIN_OK": "A",
        "LOGIN_FAIL": "D",
        "ACCESS": "A",
        "LOGOUT": "A",
        "SU": "A",
        "EXIT": "A"
    },
    "D": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "D",
        "ACCESS": "E",
        "LOGOUT": "E",
        "SU": "E",
        "EXIT": "E"
    },
    "E": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "F",
        "ACCESS": "E",
        "LOGOUT": "E",
        "SU": "E",
        "EXIT": "E"
    },
    "F": {
        "LOGIN_OK": "E",
        "LOGIN_FAIL": "D",
        "ACCESS": "E",
        "LOGOUT": "E",
        "SU": "E",
        "EXIT": "E"
    }
}
#conjunto de estados finales o de aceptacion del afd
estados_finales = {"D", "E", "F"}


# Reconocimiento de secuencias mediante el AFD
print("\n========== ANALISIS DEL AFD ==========")
#recorrer cada ip y su lista de eventos utilizando el afd
for ip, eventos in eventos_por_ip.items():
    #iniciar el automata en el estado A
    estado_actual = "A"
    #procesar los eventos de la ip en orden
    for evento in eventos:
        #consultar la tabla de transiciones y cambiar de estado
        estado_actual = transiciones_afd[estado_actual][evento]
    #comprobar si el estado final alcanzado es de aceptacion
    if estado_actual in estados_finales:
        #mostrar alerta si se reconocio la secuencia sospechosa
        print("ALERTA: Tres o más intentos fallidos consecutivos")
        print("Direccion IP:", ip)
        print("Estado final:", estado_actual)

    else:
        #mostrar que no se detecto la secuencia de fallos
        print("Sin patrones sospechosos en la IP:", ip)
        print("Estado final:", estado_actual)
