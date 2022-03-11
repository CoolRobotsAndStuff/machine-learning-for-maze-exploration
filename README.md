<div align="center">
<h1>Machine learning aplicado a resolución de laberintos en robotica simulada<h1/>

</div>

![IITA](https://i0.wp.com/iita.com.ar/wp-content/uploads/2021/12/cropped-LogoITTA-versiones-01-02-02.png?fit=2618%2C977&ssl=1)

## Problema:

**Dado un laberinto el robot debe recorrerlo en su *totalidad* de la manera mas eficiente posible solo conociendo las partes que ya exploró, descubriendolo gradualmente.**
   
## Avances
   
Contamos con una **version simplificada** del problema en python para evitar utilizar el simulado de webots para entrenar modelos y realizar pruevas, **pero es nuestro objetivo final trasladarlo a ese simulador.**
   
Seguimos incursionando en el aprendizaje teorico y practico de posibles modelos acordes a la problematica,para evaluar su desempeño y luego implementar los mas optimos

## Representacion grafica del Laberinto en el entorno Simplificado

![Laberinto](./images/laberinto.png)

(incluir representacion de laberinto)


## Explicacion 

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

(incluir representacion en memoria)
   
## El Nodo:

Cada **Nodo** posee los digueintes datos:

* Tipo de nodo: puede ser
    * *casilla*
    * *vertice*
    * *pared*

* Estados:
    * *ocupado*
    * *no ocupado*
    * *desconocido*

* Tipo de casilla (solo para nodos con tipo de nodo "casilla"):
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

