"""Pruebas del autómata de pila y de la gramática. Ejecutar:  python test_pda.py"""
import sys, itertools
sys.path.insert(0, ".")
import automata_pila as pda

CASOS = [
 # id, descripción, secuencia, esperado
 ("P01", "normal", "LOGIN_FAIL", True),
 ("P02", "normal", "LOGIN_OK LOGOUT", True),
 ("P03", "normal", "LOGIN_OK ACCESS LOGOUT", True),
 ("P04", "normal", "LOGIN_FAIL LOGIN_OK ACCESS LOGOUT", True),
 ("P05", "anidada", "LOGIN_OK SU ACCESS EXIT LOGOUT", True),
 ("P06", "límite: dos SU", "LOGIN_OK SU SU EXIT EXIT LOGOUT", True),
 ("P07", "límite: log vacío", "", True),
 ("P08", "dos sesiones", "LOGIN_OK LOGOUT LOGIN_OK ACCESS LOGOUT", True),
 ("P09", "inválida", "LOGOUT", False),
 ("P10", "inválida", "ACCESS", False),
 ("P11", "inválida", "LOGIN_OK ACCESS", False),
 ("P12", "inválida", "LOGIN_OK SU LOGOUT", False),
 ("P13", "inválida", "LOGIN_OK LOGIN_OK LOGOUT LOGOUT", False),
 ("P14", "inválida", "LOGIN_OK EXIT LOGOUT", False),
 ("P15", "inválida", "LOGIN_OK SU EXIT EXIT LOGOUT", False),
 ("P16", "inesperada", "LOGIN_ERROR", False),
 ("P17", "límite: 500 niveles", " ".join(["LOGIN_OK"] + ["SU"]*500 + ["EXIT"]*500 + ["LOGOUT"]), True),
 ("P18", "límite: 500 SU sin cerrar", " ".join(["LOGIN_OK"] + ["SU"]*500 + ["LOGOUT"]), False),
]

def main():
    malos = 0
    print("%-4s %-26s %-9s %-9s %s" % ("ID", "Tipo", "Esperado", "Obtenido", "Estado"))
    for id_, tipo, cad, esp in CASOS:
        ok, motivo, _ = pda.validar_sesiones(cad.split())
        est = "Correcto" if ok == esp else "ERROR"
        malos += ok != esp
        print("%-4s %-26s %-9s %-9s %s" % (id_, tipo, "Acepta" if esp else "Rechaza", "Acepta" if ok else "Rechaza", est))
    print("\nResultado:", "TODAS CORRECTAS" if not malos else "%d ERRORES" % malos)
    return malos

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
