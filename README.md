# LogGuard – Analizador de Registros

## 1. Nombre del proyecto

**LogGuard: Analizador de Registros y Detector de Patrones Sospechosos**

Proyecto 2 de la materia Teoría Computacional.

## 2. Integrantes

- Integrante 1: Azul Azeneth Reyna Rocha-183894
- Integrante 2: Alexis Israel Rivas Lara-184204
- Integrante 3: Miriam Juana Acosta Loyola-183800
- Docente: Wilmer Ramírez Valdez

## 3. Descripción

LogGuard es un programa desarrollado en Python que permite analizar archivos de registros (logs), con el propósito de identificar, validar y organizar información relacionada con eventos de acceso.

El sistema utiliza expresiones regulares para extraer datos como direcciones IP, fechas, nombres de usuarios y tipos de eventos. Posteriormente, valida los registros, los ordena cronológicamente y agrupa los eventos por dirección IP.

Además, el proyecto utiliza autómatas para reconocer patrones de intentos fallidos de inicio de sesión y validar secuencias de sesiones y elevaciones de privilegios.

También se utiliza teoría de grafos para representar las relaciones entre usuarios, direcciones IP y eventos.

## 4. Requisitos

Para ejecutar el proyecto se necesita:

- Python 3 instalado.
- Visual Studio Code o un editor compatible con Python.
- Una terminal.
- Los archivos del proyecto.
- Un archivo `.txt` con los registros que se desean analizar.

El proyecto utiliza únicamente módulos de Python, por lo que no requiere instalar librerías externas.

## 5. Lenguaje utilizado

### Python

El proyecto fue desarrollado en **Python**.

Se utiliza para:

- Leer y procesar los archivos de registros.
- Validar la información.
- Aplicar expresiones regulares.
- Procesar los eventos.
- Ejecutar el AFN y AFD.
- Ejecutar el autómata de pila.
- Construir y recorrer el grafo.

También se utiliza el módulo `re` para las expresiones regulares, `sys` para recibir archivos desde la terminal y `collections.deque` para realizar el recorrido BFS del grafo.

## 6. Instrucciones para ejecutar

### Paso 1. Abrir el proyecto

Abrir la carpeta del proyecto en **Visual Studio Code**.

### Paso 2. Verificar los archivos

La carpeta debe contener los archivos principales del proyecto, incluyendo:

- `main.py`
- `automata_pila.py`
- `grafo.py`
- `registros.txt`

### Paso 3. Abrir la terminal

En Visual Studio Code abrir:

**Terminal → New Terminal**

### Paso 4. Ejecutar con el archivo predeterminado

Si se desea analizar `registros.txt`, ejecutar:

```bash
python main.py
```

El programa utilizará `registros.txt` como archivo de entrada de forma predeterminada.

### Paso 5. Ejecutar con otro archivo

También se puede indicar otro archivo de registros:

```bash
python main.py registros_sesiones.txt
```

De esta manera, el programa analizará el archivo especificado.

### Paso 6. Consultar los resultados

Los resultados se muestran directamente en la terminal.

El programa muestra información como:

- Registros válidos y no válidos.
- Análisis mediante AFN.
- Análisis mediante AFD.
- Análisis mediante autómata de pila.
- Lista de adyacencia del grafo.
- Actividad por IP.
- Recorridos BFS.

## 7. Estructura del proyecto

```text
LogGuard/
│
├── main.py
├── automata_pila.py
├── grafo.py
├── registros.txt
├── registros_sesiones.txt
├── test_automata_pila.py
├── test_integración.py
├── README.md
│
├── 01_Documentacion/
│   └── Proyecto_Final.pdf
│
├── 03_Automatas/
│   ├── AFN.png
│   ├── AFD.png
│   └── AP.png
│
├── 04_Grafos/
│   └── Grafo.png
│
├── 05_Pruebas/
│   └── casos_prueba.pdf
│
├── 06_Presentacion/
│   └── Presentacion.pdf
│
└── 07_Evidencias/
    └── Bitacora
```

### Descripción de los archivos principales

| Archivo | Descripción |
|---|---|
| `main.py` | Programa principal. Lee los registros, aplica las expresiones regulares y ejecuta los análisis mediante AFN, AFD, autómata de pila y grafos. |
| `automata_pila.py` | Contiene la implementación del autómata de pila para validar las sesiones y elevaciones de privilegios. |
| `grafo.py` | Contiene la implementación del grafo, la lista de adyacencia, el cálculo de actividad por IP y el recorrido BFS. |
| `registros.txt` | Archivo principal utilizado como entrada para las pruebas de análisis de logs. |
| `registros_sesiones.txt` | Archivo utilizado para probar diferentes secuencias de sesiones y eventos. |
| `test_automata_pila.py` | Contiene pruebas específicas para validar el funcionamiento del autómata de pila. |
| `test_integración.py` | Contiene pruebas de integración para comprobar el funcionamiento del programa completo en diferentes casos. |
| `README.md` | Documento con información del proyecto, requisitos e instrucciones de ejecución. |

## 8. Eventos reconocidos

LogGuard reconoce los siguientes tipos de eventos:

| Evento | Descripción |
|---|---|
| `LOGIN_OK` | Inicio de sesión exitoso. |
| `LOGIN_FAIL` | Intento de inicio de sesión fallido. |
| `ACCESS` | Acceso a un recurso del servidor. |
| `LOGOUT` | Cierre de una sesión. |
| `SU` | Cambio de usuario o elevación de privilegios. |
| `EXIT` | Salida de un proceso o sesión. |

## 9. Ejemplos de uso

### Ejemplo 1: ejecutar el archivo principal

```bash
python main.py
```

El programa analiza el archivo `registros.txt`.

### Ejemplo 2: ejecutar con otro archivo

```bash
python main.py registros_sesiones.txt
```

### Ejemplo 3: registro válido

```text
2026-11-14 10:15:30 IP=192.168.1.10 USER=alex EVENT=LOGIN_OK
2026-11-14 10:15:40 IP=192.168.1.10 USER=alex EVENT=ACCESS
2026-11-14 10:16:00 IP=192.168.1.10 USER=alex EVENT=LOGOUT
```

Este registro contiene una estructura válida, una dirección IP correcta y eventos reconocidos por el sistema.

### Ejemplo 4: registro no válido

```text
2026-11-14 10:21:00 IP=256.168.1.60 USER=ana EVENT=LOGIN_FAIL
```

Este registro es rechazado porque la dirección IP contiene un segmento mayor a 255.

### Ejemplo 5: detección de intentos fallidos

Si una misma IP contiene tres o más eventos `LOGIN_FAIL` consecutivos, el programa genera una alerta indicando que se detectó el patrón sospechoso.

### Ejemplo 6: análisis del grafo

El programa construye relaciones de la siguiente forma:

```text
Usuario → IP → Evento
```

Por ejemplo:

```text
ana → 192.168.1.20 → LOGIN_FAIL
```

Si el mismo evento aparece varias veces, la conexión aumenta su peso.

También se realiza un recorrido BFS desde los usuarios para consultar sus conexiones con las IP y los eventos.

## 10. Pruebas

El proyecto incluye archivos para realizar pruebas de diferentes partes del sistema.

Para ejecutar las pruebas del autómata de pila:

```bash
python test_automata_pila.py
```

Para ejecutar las pruebas de integración:

```bash
python test_integración.py
```

Las pruebas permiten comprobar casos normales, inválidos, límites e inesperados.

## 11. Conceptos de Teoría Computacional aplicados

### Expresiones regulares

Se utilizan para identificar y extraer los campos de información de los registros.

### Autómata Finito No Determinista (AFN)

Se utiliza para representar el reconocimiento de patrones relacionados con intentos fallidos de inicio de sesión.

### Autómata Finito Determinista (AFD)

Se utiliza para analizar secuencias de eventos y reconocer patrones definidos, como intentos consecutivos de inicio de sesión fallidos.

### Gramática Libre de Contexto (GLC)

Se utiliza para representar las reglas y estructuras válidas de las secuencias de sesiones y elevaciones de privilegios.

### Autómata de Pila (AP)

Se utiliza para validar secuencias de sesiones, accesos y elevaciones de privilegios, considerando la estructura de apertura y cierre de cada secuencia.

### Teoría de grafos

Se utiliza para representar las relaciones entre usuarios, direcciones IP y eventos, permitiendo analizar sus conexiones mediante una estructura de grafo dirigido y ponderado.

## 12. Resultados esperados

Al ejecutar LogGuard se espera obtener:

- Identificación de registros válidos y no válidos.
- Extracción de información mediante expresiones regulares.
- Organización de registros por fecha.
- Agrupación de eventos por IP.
- Identificación de patrones sospechosos.
- Detección de tres o más intentos consecutivos de inicio de sesión fallidos.
- Validación de sesiones y elevaciones de privilegios.
- Análisis de relaciones entre usuarios, IP y eventos mediante grafos.
- Recorridos BFS para consultar las conexiones del grafo.

## 13. Objetivo del proyecto

El objetivo de LogGuard es aplicar los conceptos de Teoría Computacional en el desarrollo de una herramienta de análisis de registros, utilizando modelos matemáticos y computacionales para reconocer patrones, validar secuencias de eventos e identificar comportamientos que requieren atención.

El proyecto permite demostrar la aplicación práctica de expresiones regulares, autómatas finitos, gramáticas libres de contexto, autómatas de pila y teoría de grafos mediante el desarrollo de un programa en Python.
