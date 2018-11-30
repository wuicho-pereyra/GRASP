# GRASP
El algoritmo Greedy Randomized Adaptive Search Procedures (GRASP) se implementa para la optimización del problema de corte de materiales (Cutting Stock Problem)

# Ejecución
Para ejecutar el algoritmo es necesario indicar las rutas de los 3 archivos necesarios para el funcionamiento:

# Requerimientos
Tiene 3 columnas, la primera indica cuantos tramos se necesitan, la segunda, la cantidad lineal del tramo
de material y la tercera columna indica la clave del material. Por ejemplo:

requerimientos.csv

3 120 1

5 189 2

1 1231 1

Aquí se especifica que se requieren 3 tramos de 120 unidades lineales de material del tipo 1, 5 tramos de
189 unidades de material de tipo 2 y 1 tramo de 1231 unidades de material tipo 1.

# Presentaciones
En este se indica qué tipo de presentaciones existen para cada uno de los materiales. Este archivo se define de la siguiente forma, la primera columna indica la clave (nombre) del material, la segunda cuantas presentaciones existen de ese material y la tercera, cuanto miden cada una de esas presentaciones.

presentaciones.csv

1 3 150 310 1500

2 1 220

3 2 231 342

Aquí se puede observar que el material 1 tiene 3 presentaciones, de 150, 310 y 1500, respectivamente, el
material 2 tiene 1 sola presentación de 220 y el material 3 tiene 2 presentaciones, de 231 y 342,
respectivamente. En el archivo requerimientos.csv, para toda especificación de tramo de material debe por lo menos
existir 1 presentación que sea mayor, es decir no es posible soldar o pegar material (en este punto,
después en la versión multi-objetivo podría serlo).

# Salida

El archivo de salida que debe generar su algoritmo debe contener la siguiente información. Cada renglón
especifica cuantas y cuales presentaciones se están usando y el tipo de material (primeras 3 columnas),
después se detalla cuantos elementos y de qué tamaño se están produciendo (cortando), y finalmente la
última columna indica el desperdicio de esa producción. Al final del archivo se indica el desperdicio total
de material, que es la suma de los desperdicios individuales.

salida.csv

1 1500 1 3 1231 120 120 29

1 150 1 1 120 30

5 220 2 189 189 189 189 189 155

214

Aquí se indica que se empleará 1 presentación de material de longitud 1500 de material tipo 1, del cual
se cortarán 3 tramos, de 1231, 120 y 120 unidades, respectivamente, del cual se tendrá un desperdicio
de 29 unidades.
En la segunda línea, se puede observar que se empleará 1 presentación de material de 150 unidades de
tipo 1 y se cortara 1 tramo de 120 unidades para un desperdicio de 30 unidades.
En la tercera línea se observa que se emplearán 5 presentaciones de material de 220 unidades, de tipo
2, del cual se cortarán en tramos de 189 unidades (5 tramos) para un desperdicio de 155.
Finalmente se reporta el desperdicio total que es la suma de 29, 30 y 155, 214.


Para ejecutar el algoritmo basta con especificar los siguientes parámetros:

in_loop = 100 (Tamaño de la población inicial)

out_loop = 100 (Número de iteraciones

Las direcciones de los archivos de requerimientos.csv y presentaciones.csv

Por último se invoca la función:

GRASP(requeriments, materials ,in_loop = 100, out_loop = 100)
