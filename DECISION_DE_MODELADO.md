# Decisión de modelado de datos
## API REST - Sistema de gestión de cine

### 1. Introducción

En este proyecto desarrollamos una API REST con Flask para gestionar información relacionada con un cine. El sistema trabaja con películas, salas, funciones, usuarios y reseñas.

Una de las principales partes del trabajo fue decidir cómo repartir los datos entre dos bases diferentes: MySQL y MongoDB.

La idea no era guardar información en ambas bases solamente para cumplir el requisito, sino buscar una distribución que tuviera sentido según el tipo de datos que manejamos.

Finalmente, decidimos utilizar MySQL para la información más estructurada del cine y MongoDB para las reseñas de las películas, ya que estas pueden contener información más variada.

### 2. Distribución de los datos

Para organizar el sistema decidimos repartir las entidades de la siguiente manera:

| Entidad   | Base de datos | Motivo                                                                               |
|-----------|---------------|--------------------------------------------------------------------------------------|
| Películas | MySQL         | Todas tienen datos definidos, como título, duración y clasificación.                 |
| Salas     | MySQL         | Cada sala tiene un número único y una capacidad que debe ser mayor que cero.         |
| Funciones | MySQL         | Cada función debe estar relacionada con una película y una sala existentes.          |
| Usuarios  | MySQL         | Los usuarios tienen campos definidos y no pueden compartir el mismo correo.          |
| Reseñas   | MongoDB       | Pueden incluir comentarios, listas de aspectos destacados y otros campos opcionales. |

Esta distribución nos permite mantener las relaciones más importantes en MySQL y aprovechar la flexibilidad de MongoDB para almacenar opiniones.

### 3. ¿Por qué elegimos esta distribución?

**Relación entre películas, salas y funciones**

Una de las razones para utilizar MySQL es que las funciones dependen directamente de otras entidades.

Por ejemplo, no tendría sentido registrar una función para una película que no existe o asignarla a una sala que tampoco está registrada.

Para evitar ese problema, utilizamos claves foráneas en la tabla `funciones`, que la relacionan con `peliculas` y `salas`.

De esta manera, MySQL se encarga de comprobar que esas relaciones sean válidas.

**Reglas que deben cumplir los datos**

Otra razón es que algunos datos necesitan cumplir ciertas condiciones.

Por ejemplo, una película no puede durar cero minutos o tener una duración negativa. Lo mismo ocurre con la capacidad de una sala, que siempre debe ser positiva.

También necesitamos evitar que dos salas tengan el mismo número o que dos usuarios compartan el mismo correo.

Para controlar estas situaciones utilizamos restricciones como `CHECK`, `NOT NULL` y `UNIQUE`.

Esto nos permite evitar información incorrecta desde la propia base de datos, sin depender solamente de las validaciones que hacemos en Flask.

**Las reseñas no siempre tienen la misma información**

Para las reseñas preferimos utilizar MongoDB porque no todas necesitan tener exactamente los mismos campos.

Por ejemplo, una persona puede dejar solamente una calificación, mientras que otra también puede escribir un comentario y agregar una lista con los aspectos que más le gustaron de la película.

En MongoDB podemos guardar estos datos dentro de un mismo documento, utilizando campos opcionales y arreglos.

Esto nos pareció más cómodo para manejar las reseñas, ya que no necesitamos obligar a todos los usuarios a completar la misma información.

### 4. ¿Cómo se relacionan las dos bases?

Aunque MySQL y MongoDB son bases de datos independientes, necesitamos relacionar la información que guardamos en ellas.

Para hacerlo utilizamos el campo `pelicula_id`, que se encuentra en los documentos de las reseñas de MongoDB.

Ese campo guarda el identificador de una película registrada en MySQL.

Por ejemplo, si una reseña tiene `pelicula_id: 1`, significa que está asociada con la película que tiene el ID 1 en MySQL.

Cuando alguien intenta registrar una reseña, la API primero consulta MySQL para comprobar que la película exista.

Si no la encuentra, devuelve un error `404` y no guarda la reseña.

También creamos el endpoint:

`GET /api/peliculas/<id>/resenas`

Este permite consultar una película junto con todas sus reseñas.

Para conseguirlo, Flask primero obtiene los datos de la película desde MySQL y después busca en MongoDB las reseñas que tengan el mismo `pelicula_id`.

Finalmente, junta ambas consultas y devuelve toda la información en una sola respuesta JSON.

Hay que considerar que MongoDB no puede utilizar directamente las claves foráneas de MySQL, por lo que esta relación la controlamos desde nuestra API.

Por ahora, comprobamos que la película exista antes de registrar una reseña. Todavía no implementamos la eliminación de películas, así que tampoco tenemos una función que elimine o actualice automáticamente sus reseñas si se borra una película.

### 5. ¿Qué otra alternativa consideramos?

Una alternativa que consideramos fue utilizar solamente MySQL para almacenar toda la información, incluyendo las reseñas.

Esta opción habría simplificado algunas cosas, porque tendríamos todos los datos en una sola base.

Sin embargo, las reseñas pueden incluir listas de aspectos destacados y campos que no siempre están presentes.

Para representarlas en MySQL podríamos utilizar campos JSON o crear tablas adicionales relacionadas con las reseñas.

Preferimos MongoDB porque permite almacenar toda esa información dentro de un mismo documento, sin tener que separar los aspectos destacados en varias filas.

Además, esto nos permite trabajar con dos formas diferentes de almacenar datos, manteniendo las entidades principales del cine en MySQL.

No significa que MySQL no pueda almacenar reseñas, sino que, para la estructura que decidimos utilizar, MongoDB nos pareció una alternativa conveniente.

### 6. Conclusión

En general, decidimos utilizar cada base de datos según el tipo de información que necesitábamos guardar.

MySQL nos sirve para mantener organizadas las películas, salas, funciones y usuarios, especialmente porque existen relaciones y reglas que deben cumplirse.

Por otro lado, MongoDB nos permite guardar las reseñas de una manera más flexible, ya que pueden incluir comentarios, listas y campos opcionales.

La conexión entre ambas bases la realizamos desde Flask, utilizando los identificadores de las películas para relacionar la información.

Con esta distribución conseguimos que las dos bases tengan una función dentro del sistema y que la API pueda trabajar con ellas de forma conjunta.