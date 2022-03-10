# Machine learning aplicado a resolución de laberintos en robotica simulada

## Problema:

Dado un laberinto el robot debe recorrerlo en su totalidad de la manera mas eficiente posible solo conociendo las partes que ya exploró, descubriendolo gradualmente.

![Laberinto](./images/laberinto.png)


(incluir representacion de laberinto)

V = vertice
P = pared
C = casilla

---------------------
| V | P | V | P | V |
---------------------
| P | C | P | C | P |
---------------------
| V | P | V | P | V |
---------------------
| P | C | P | C | P |
---------------------
| V | P | V | P | V |
---------------------

Cada node posee los digueintes datos:

* Tipo de nodo: puede ser
    * casilla
    * vertice
    * pared

* Estados:
    * ocupado
    * no ocupado
    * desconocido

* Tipo de casilla (solo para nodos con tipo de nodo "casilla"):
    * desconocido
    * normal
    * casilla de inicio
    * conexión de zona 1 a 2
    * conexión de zona 1 a 3
    * conexión de zona 3 a 2
    * pantano
    * pozo
    * checkpoint

    Todas ellas tienen distintas propiedades en la simulación.

Contamos con una version simplificada del problema en python prar evitar utilizar el simulado de webots para entrenar modelos y realizar pruevas, pero es nuestro objetivo final trasladarlo a ese simulador.

Video de ejemplo de una ronda de la competencia, utilizando el simulador:
https://www.youtube.com/watch?v=C_sho03AJmo

## Como reproducir pruebas y entorno

Instalar python 3.8.10 y pip:

https://www.python.org/downloads/release/python-3810/

Clonar repositorio

```
git clone https://github.com/CoolRobotsAndStuff/machine-learning-for-maze-exploration.git
```

instalar pipenv

```
pip install pipenv
```

crear entorno virutal

```
pipenv shell --python 3.8.10
```

instalar dependencias

```
pipenv install requirements.txt
```

correr entorno
```
#desde la shell del venv
python3 game.py
```





