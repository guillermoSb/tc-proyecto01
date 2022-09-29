# Proyecto 01 - Teoría de la Computación
`Catedrático: Alan Reyes`

## Información general del programa
- Para la concatenación se debe de utilizar un caracter `@`. Por ejemplo: ab = a@b
- La estrella de Kleene utiliza el caracter `*`
- La unión utiliza el caracter `|`

## Estructura del programa
- `automata.py` Clase autómata encargada de:
  - Crear un AFN a partir de una regex
  - Simular un AFN y un AFD
  - Convertir de AFN a AFD
- `regex.py` Clase regex encargada de:
  - Convertir una regex a notación Posfix.
- `test_proyecto1.py` Pruebas unitarias
- `node.py` Clase encargada de definir la estructura de un Nodo para la elaboración de el árbol sintáctico.
- `proyecto1.py` Archivo principal

## Ejecutar el programa
`python proyecto1.py`

## Ejecutar pruebas unitarias
1. `pip install pytest`
2. `pytest`