# Machine learning aplicado a resolución de laberintos en robotica simulada

## Problema:

Dado un laberinto el robot debe recorrerlo en su tottalidad de la manera mas eficiente posible solo conociendo las partes que ya exploró, descubriendolo gradualmente.

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