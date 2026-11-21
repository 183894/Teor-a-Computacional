"""
automata_pila.py - Autómata de pila de LogGuard (Integrante 3 - Miriam)
=====================================================
Reconoce el lenguaje de "sesiones bien formadas" definido por la gramática:

    Log    -> Item Log | ε
    Item   -> LOGIN_FAIL | Sesion
    Sesion -> LOGIN_OK Cuerpo LOGOUT
    Cuerpo -> ACCESS Cuerpo | SU Cuerpo EXIT Cuerpo | ε

AP = (Q, Σ, Γ, δ, q0, Z0, F)
    Q  = {q0, qf}
    Σ  = {LOGIN_OK, LOGIN_FAIL, ACCESS, LOGOUT, SU, EXIT}
    Γ  = {Z0, S, U}     Z0 = fondo de la pila, S = sesión abierta, U = SU abierto
    F  = {qf}
Aceptación: se consumió toda la entrada y la pila solo contiene Z0.

Uso desde main.py:
    from automata_pila import validar_sesiones
    ok, motivo, traza = validar_sesiones(["LOGIN_OK", "SU", "EXIT", "LOGOUT"])
"""

Z0 = "Z0"
SESION = "S"
ELEVACION = "U"
ALFABETO = ("LOGIN_OK", "LOGIN_FAIL", "ACCESS", "LOGOUT", "SU", "EXIT")

# δ(estado, símbolo, tope) -> (estado nuevo, acción)   acción: "PUSH x" | "POP" | "NADA"
DELTA = {
    ("q0", "LOGIN_FAIL", Z0):        ("q0", "NADA"),
    ("q0", "LOGIN_OK",   Z0):        ("q0", "PUSH " + SESION),
    ("q0", "ACCESS",     SESION):    ("q0", "NADA"),
    ("q0", "ACCESS",     ELEVACION): ("q0", "NADA"),
    ("q0", "SU",         SESION):    ("q0", "PUSH " + ELEVACION),
    ("q0", "SU",         ELEVACION): ("q0", "PUSH " + ELEVACION),
    ("q0", "EXIT",       ELEVACION): ("q0", "POP"),
    ("q0", "LOGOUT",     SESION):    ("q0", "POP"),
}
# Transición ε: con la entrada terminada y solo Z0 en la pila pasa a qf y ACEPTA.


def _motivo(simbolo, tope):
    """Mensaje comprensible cuando no existe transición."""
    if simbolo == "LOGOUT":
        if tope == Z0:
            return "LOGOUT sin sesión abierta"
        return "LOGOUT mientras hay un SU sin cerrar (falta EXIT)"
    if simbolo == "EXIT":
        return "EXIT sin un SU abierto"
    if simbolo == "ACCESS":
        return "ACCESS fuera de una sesión"
    if simbolo == "SU":
        return "SU fuera de una sesión"
    if simbolo == "LOGIN_OK":
        return "LOGIN_OK dentro de una sesión ya abierta"
    if simbolo == "LOGIN_FAIL":
        return "LOGIN_FAIL dentro de una sesión abierta (no modelado)"
    return "símbolo '%s' no pertenece al alfabeto" % simbolo


class AutomataPila:
    """El autómata de pila avanzando UN símbolo a la vez (un objeto por cada IP)."""

    def __init__(self):
        self.estado = "q0"
        self.pila = [Z0]

    @property
    def tope(self):
        return self.pila[-1]

    def avanzar(self, simbolo):
        """
        Aplica una transición. Devuelve (True, "") si existe, o (False, motivo) si no.
        Cuando NO existe transición, el símbolo se descarta y la pila no cambia
        (así un error no provoca una cadena de errores falsos después).
        """
        regla = DELTA.get((self.estado, simbolo, self.tope)) if simbolo in ALFABETO else None
        if regla is None:
            return False, _motivo(simbolo, self.tope)
        _, accion = regla
        if accion == "POP":
            self.pila.pop()
        elif accion.startswith("PUSH"):
            self.pila.append(accion.split()[1])
        return True, ""

    def sesiones_abiertas(self):
        return self.pila.count(SESION)

    def elevaciones_abiertas(self):
        return self.pila.count(ELEVACION)

    def acepta(self):
        """Condición de aceptación: la pila quedó solo con Z0."""
        return self.pila == [Z0]


def validar_sesiones(eventos):
    """
    Procesa una lista completa de eventos (modo teórico: rechaza en el primer error).
    Devuelve (aceptada, motivo, traza).  Cada elemento de la traza es
    (entrada_restante, pila) ANTES de leer el siguiente símbolo.
    """
    ap = AutomataPila()
    traza = []
    for i, simbolo in enumerate(eventos):
        traza.append((list(eventos[i:]), list(ap.pila)))
        ok, motivo = ap.avanzar(simbolo)
        if not ok:
            return False, "evento %d: %s" % (i + 1, motivo), traza
    traza.append(([], list(ap.pila)))
    if ap.acepta():
        return True, "todas las sesiones están cerradas", traza
    return False, "fin del log con %d sesión(es) y %d SU sin cerrar" % (
        ap.sesiones_abiertas(), ap.elevaciones_abiertas()), traza


def mostrar_traza(traza):
    """Imprime la traza como la tabla 'Entrada / Pila' de clase."""
    for restante, pila in traza:
        entrada = " ".join(restante) if restante else "(fin)"
        contenido = " ".join(x for x in pila if x != Z0) or "vacía"
        print("  %-55s | %s" % (entrada, contenido))


if __name__ == "__main__":
    import sys
    cadena = sys.argv[1:] or ["LOGIN_OK", "SU", "ACCESS", "EXIT", "LOGOUT"]
    ok, motivo, traza = validar_sesiones(cadena)
    mostrar_traza(traza)
    print("ACEPTADA" if ok else "RECHAZADA", "-", motivo)
