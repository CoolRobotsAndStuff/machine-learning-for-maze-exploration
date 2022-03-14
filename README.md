<div align="center">
<h1>Machine learning aplicado a resolución de laberintos en robotica simulada<h1/>

</div>

![IITA](./images/iita.png)

Estamos participando en la competencia de rescate simulado de la RoboCup, utilizando el simulador de  Webots . En esta categoría el robot debe recorrer un laberinto, buscando víctimas y reportando su posición. A raíz de esta consigna, surge el problema de cómo recorrerlo en el menor tiempo posible, para el cual pensamos en aplicar machine larning.

## Problema:

**Dado un laberinto el robot debe recorrerlo en su *totalidad*, de la manera mas eficiente posible, solo conociendo las partes que ya exploró, descubriendolo gradualmente.**

Video de ejemplo de una ronda de la competencia, utilizando el simulador:
https://www.youtube.com/watch?v=C_sho03AJmo
   
## Avances
   
Contamos con una **version simplificada** del problema en python para evitar utilizar el simulador de webots para entrenar modelos y realizar pruevas, **pero es nuestro objetivo final trasladarlo a ese simulador.**
   
Seguimos incursionando en el aprendizaje teorico y practico de posibles modelos acordes a la problematica,para evaluar su desempeño y luego implementar los mas optimos

## El laberinto

Para representar el laberinto utilizamos una serie de nodos organizados en una array bidimensional. Cada nodo puede representar una casilla, una pared o un vértice, como se muestra a continuación:

*Dado un laberinto:*

![Lo que buscamos representar](./images/tile_vortex_wall.png)

Lo representamos de la siguiente manera, donde:

V = nodo de vertice

P = nodo de pared

C = nodo de casilla

```
[[V, P, V, P, V],                
 [P, C, P, C, P],                 
 [V, P, V, P, V],                  
 [P, C, P, C, P],                 
 [V, P, V, P, V]]

```
                     
   
## El Nodo:

Cada **Nodo** posee los sigueintes datos:

* Tipo de nodo, puede ser:
    * *casilla*
    * *vértice*
    * *pared*

* Estado, puede ser:
    * *ocupado*
    * *no ocupado*
    * *desconocido*

* Tipo de casilla (solo para nodos con tipo de nodo "casilla"), puede ser:
    * *desconocido*
    * *normal*
    * *casilla de inicio*
    * *conexión de zona 1 a 2*
    * *conexión de zona 1 a 3*
    * *conexión de zona 3 a 2*
    * *pantano*
    * *pozo*
    * *checkpoint*

    **Todas ellas tienen distintas propiedades en la simulación.**

## Ejemplo

![Ejemplo](./images/laberinto.png)
   

## Como reproducir pruebas y entorno

Instalar python 3.8.10 y pip:

https://www.python.org/downloads/release/python 3810/

Clonar repositorio

```
git clone https://github.com/CoolRobotsAndStuff/machine learning for maze exploration.git
```

instalar pipenv

```
pip install pipenv
```

crear entorno virutal

```
pipenv shell   python 3.8.10
```

instalar dependencias

```
pipenv install
```

correr entorno
```
#desde la shell del venv
python3 game.py
```


## Dudas y Preguntas

   * **Que modelo es mas conveniente para entrenar con respecto a nuestro problema?**
   * **Que librerias son mas recomendables?**
   
   
   
## Recursos Utiles
   
   Curso introductorio a TensorFlow:
   
   https://www.youtube.com/watch?v=tPYj3fFJGjk&t=6898s&ab_channel=freeCodeCamp.org

