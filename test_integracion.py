import os, subprocess, sys, tempfile, time

CAMPO_USUARIO = "USER"
CAMPO_EVENTO = "EVENT"
ACCESS = "ACCESS"

AQUI = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(AQUI, "main.py")
n = [0]


def l(ip, ev, usuario="ana", seg=None):
    """Una línea de log con el formato del equipo."""
    n[0] += 1
    s = n[0] if seg is None else seg
    return "2026-11-14 10:%02d:%02d IP=%s %s=%s %s=%s" % (s // 60 % 60, s % 60, ip, CAMPO_USUARIO, usuario, CAMPO_EVENTO, ev)


def ejecutar(lineas, nombre="caso.txt", binario=False, existe=True):
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, nombre)
        if existe:
            if binario:
                open(ruta, "wb").write(b"\x00\xff\xfe\x80" * 100)
            else:
                open(ruta, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
        t0 = time.time()
        p = subprocess.run([sys.executable, MAIN, ruta], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=AQUI, timeout=120,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
        return p.stdout + p.stderr, time.time() - t0


def seccion(salida, titulo):
    """Devuelve solo el texto de una sección del reporte ('ANALISIS DEL AFD', etc.)."""
    marca = "========== " + titulo
    if marca not in salida:
        return ""
    resto = salida.split(marca, 1)[1]
    return resto.split("==========", 1)[1].split("\n\n=====", 1)[0] if "==========" in resto else resto


def sesion(salida): return seccion(salida, "ANALISIS DEL AUTOMATA DE PILA")
def afd(salida): return seccion(salida, "ANALISIS DEL AFD")


CASOS = []
def caso(id_, tipo, entrada, esperado, lineas, verificar, obtenido, **kw):
    CASOS.append((id_, tipo, entrada, esperado, lineas, verificar, obtenido, kw))

A = "10.0.0.1"
caso("T01", "Normal", "LOGIN_OK, ACCESS, LOGOUT", "Sesión bien formada", [l(A, "LOGIN_OK"), l(A, ACCESS), l(A, "LOGOUT")],
     lambda o: "Sesiones bien formadas en la IP: " + A in o, "Sesión bien formada")
caso("T02", "Normal", "Sesión con SU y EXIT anidados", "Sesión bien formada",
     [l(A, "LOGIN_OK"), l(A, "SU"), l(A, ACCESS), l(A, "EXIT"), l(A, "LOGOUT")],
     lambda o: "Sesiones bien formadas en la IP: " + A in o, "Sesión bien formada")
caso("T03", "Normal", "3 LOGIN_FAIL seguidos", "Alerta en AFN y AFD",
     [l(A, "LOGIN_FAIL")] * 1 + [l(A, "LOGIN_FAIL"), l(A, "LOGIN_FAIL")],
     lambda o: "ALERTA: Tres o más" in afd(o) and "ALERTA: Tres o más" in o.split("ANALISIS DEL AFD")[0], "Alerta AFN y AFD")
caso("T04", "Normal", "2 LOGIN_FAIL, LOGIN_OK, LOGOUT", "Sin alerta de fuerza bruta",
     [l(A, "LOGIN_FAIL"), l(A, "LOGIN_FAIL"), l(A, "LOGIN_OK"), l(A, "LOGOUT")],
     lambda o: "ALERTA: Tres o más" not in o, "Sin alerta")
caso("T05", "Normal", "2 fallos de cada una de 2 IPs, intercalados", "Sin alerta (no se mezclan IPs)",
     [l("10.0.0.5", "LOGIN_FAIL"), l("10.0.0.6", "LOGIN_FAIL"), l("10.0.0.5", "LOGIN_FAIL"), l("10.0.0.6", "LOGIN_FAIL")],
     lambda o: "ALERTA: Tres o más" not in o, "Sin alerta")
caso("T06", "Normal", "Dos sesiones seguidas", "Sesión bien formada",
     [l(A, "LOGIN_OK"), l(A, "LOGOUT"), l(A, "LOGIN_OK"), l(A, ACCESS), l(A, "LOGOUT")],
     lambda o: "Sesiones bien formadas en la IP: " + A in o, "Sesión bien formada")
caso("T07", "Normal", "3 fallos, LOGIN_OK, LOGOUT", "AFD alerta y pila acepta",
     [l(A, "LOGIN_FAIL")] * 3 + [l(A, "LOGIN_OK"), l(A, "LOGOUT")],
     lambda o: "ALERTA: Tres o más" in afd(o) and "Sesiones bien formadas" in sesion(o), "AFD alerta, pila acepta")
caso("T08", "Inválida", "IP con 3 números (192.168.1)", "Registro no válido",
     ["2026-11-14 10:00:00 IP=192.168.1 %s=pedro %s=LOGIN_OK" % (CAMPO_USUARIO, CAMPO_EVENTO)],
     lambda o: "Registro no válido" in o, "Registro no válido")
caso("T09", "Inválida", "IP 999.1.1.1 (fuera de rango)", "Registro no válido",
     ["2026-11-14 10:00:00 IP=999.1.1.1 %s=pedro %s=LOGIN_OK" % (CAMPO_USUARIO, CAMPO_EVENTO)],
     lambda o: "Registro no válido" in o, "Registro no válido")
caso("T10", "Inválida", "Evento LOGSSIN_OK", "Registro no válido",
     ["2026-11-14 10:00:00 IP=%s %s=pedro %s=LOGSSIN_OK" % (A, CAMPO_USUARIO, CAMPO_EVENTO)],
     lambda o: "Registro no válido" in o, "Registro no válido")
caso("T11", "Inválida", "Línea sin fecha", "Registro no válido",
     ["IP=%s %s=pedro %s=LOGIN_OK" % (A, CAMPO_USUARIO, CAMPO_EVENTO)],
     lambda o: "Registro no válido" in o, "Registro no válido")
caso("T12", "Inválida", "LOGOUT sin haber iniciado sesión", "Alerta: sesión inválida",
     [l(A, "LOGOUT")], lambda o: "ALERTA: Sesión inválida" in o and "LOGOUT sin sesión" in o, "Alerta: LOGOUT sin sesión abierta")
caso("T13", "Inválida", "SU sin EXIT antes de LOGOUT", "Alerta: falta EXIT",
     [l(A, "LOGIN_OK"), l(A, "SU"), l(A, "LOGOUT")], lambda o: "falta EXIT" in o, "Alerta: falta EXIT")
caso("T14", "Inválida", "ACCESS fuera de una sesión", "Alerta: sesión inválida",
     [l(A, ACCESS)], lambda o: "ACCESS fuera de una sesión" in o, "Alerta: ACCESS fuera de sesión")
caso("T15", "Inválida", "Sesión que nunca se cierra", "Alerta: sesión sin cerrar",
     [l(A, "LOGIN_OK"), l(A, ACCESS)], lambda o: "1 sesión(es)" in o, "Alerta: 1 sesión sin cerrar")
caso("T16", "Inválida", "LOGIN_OK dentro de una sesión abierta", "Alerta: sesión inválida",
     [l(A, "LOGIN_OK"), l(A, "LOGIN_OK"), l(A, "LOGOUT"), l(A, "LOGOUT")],
     lambda o: "LOGIN_OK dentro de una sesión" in o, "Alerta: LOGIN_OK dentro de sesión")
caso("T17", "Límite", "Archivo vacío", "Sin registros ni errores", [],
     lambda o: "Traceback" not in o and "ALERTA" not in o, "Sin registros ni errores")
caso("T18", "Límite", "Solo líneas en blanco", "Se ignoran", ["", "   ", ""],
     lambda o: "Traceback" not in o and "Registro no válido" not in o, "Se ignoran")
caso("T19", "Límite", "500 SU anidados con sus 500 EXIT", "Sesión bien formada",
     [l(A, "LOGIN_OK", seg=0)] + [l(A, "SU", seg=1)] * 500 + [l(A, "EXIT", seg=2)] * 500 + [l(A, "LOGOUT", seg=3)],
     lambda o: "Sesiones bien formadas en la IP: " + A in o, "Sesión bien formada")
caso("T20", "Límite", "10 000 registros", "Termina en menos de 30 s",
     [l("10.1.%d.%d" % (i % 20, i % 200), ACCESS, seg=i % 3600) for i in range(10000)],
     lambda o: "Traceback" not in o, "Termina sin errores")
caso("T21", "Inesperada", "Archivo que no existe", "Mensaje de error claro", [],
     lambda o: "no se encontró" in o and "Traceback" not in o, "ERROR: no se encontró el archivo", existe=False)
caso("T22", "Inesperada", "Archivo binario", "Mensaje de error claro", [],
     lambda o: "binario" in o and "Traceback" not in o, "ERROR: archivo no es de texto", binario=True)
caso("T23", "Inesperada", "Línea de 5000 caracteres", "Sin errores del programa",
     [l(A, "LOGIN_OK") + " " + "x" * 5000, l(A, "LOGOUT")],
     lambda o: "Traceback" not in o, "Sin errores del programa")


def principal(imprimir=True):
    filas, malos = [], 0
    for id_, tipo, entrada, esperado, lineas, ver, obt, kw in CASOS:
        try:
            salida, seg = ejecutar(lineas, **kw)
            ok = bool(ver(salida))
            extra = " (%.1f s)" % seg if id_ == "T20" else ""
        except Exception as e:
            ok, extra, salida = False, "", repr(e)
        malos += not ok
        filas.append([id_, tipo, entrada, esperado, (obt + extra) if ok else "FALLÓ: " + salida.strip().splitlines()[-1][:50] if salida.strip() else "FALLÓ", "Correcto" if ok else "ERROR"])
    if imprimir:
        print("%-4s %-11s %-44s %-34s %s" % ("ID", "Tipo", "Entrada", "Resultado esperado", "Estado"))
        for f in filas:
            print("%-4s %-11s %-44s %-34s %s" % (f[0], f[1], f[2][:44], f[3][:34], f[5]))
        print("\nResultado: %d casos, %d correctos, %d con error" % (len(filas), len(filas) - malos, malos))
    return filas, malos


if __name__ == "__main__":
    sys.exit(1 if principal()[1] else 0)
