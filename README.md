# API REST - Sistema de Cine

## 1. Descripción

API REST desarrollada con Python y Flask para gestionar información de un cine.

El proyecto utiliza dos motores de bases de datos:

- **MySQL:** almacena películas, salas, funciones y usuarios.
- **MongoDB:** almacena reseñas y calificaciones de películas.

La API permite consultar, registrar y modificar películas, guardar reseñas y combinar información de ambas bases de datos.

## 2. Tecnologías utilizadas

- Python 3.13
- Flask
- MySQL 8.0
- MongoDB 7
- Docker y Docker Compose
- PyMySQL
- PyMongo
- Gunicorn

## 3. Requisitos

Para ejecutar el proyecto se necesita:

- Docker Desktop o Docker Engine con Docker Compose.
- Un cliente HTTP, como REST Client para Visual Studio Code, para realizar las pruebas.

No es necesario instalar MySQL, MongoDB ni las dependencias de Python directamente en el computador, ya que se ejecutan mediante Docker.

## 4. Instalación y ejecución

Abrir una terminal en la carpeta principal del proyecto.

Crear el archivo `.env` a partir de `.env.ejemplo`.

En PowerShell:

```powershell
Copy-Item .env.ejemplo .env
```

Iniciar los servicios:

```powershell
docker compose up -d --build
```

Comprobar su funcionamiento:

```powershell
docker compose ps
```

La API estará disponible en:

`http://localhost:5000`

## 5. Bases de datos

El proyecto utiliza dos bases de datos.

**MySQL**

Contiene cuatro tablas:

- `peliculas`
- `salas`
- `funciones`
- `usuarios`

Las tablas se crean mediante `sql/inicio.sql` cuando MySQL inicializa un volumen nuevo.

**MongoDB**

Utiliza la colección `resenas`, donde se almacenan las opiniones, calificaciones y aspectos destacados de las películas.

La colección se crea al registrar la primera reseña.

Los datos se conservan en volúmenes de Docker.

## 6. Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/peliculas` | Listar películas |
| GET | `/api/peliculas/1` | Consultar película por ID |
| POST | `/api/peliculas` | Registrar película |
| PATCH | `/api/peliculas/1` | Modificar película |
| GET | `/api/resenas` | Listar reseñas |
| POST | `/api/resenas` | Registrar reseña |
| GET | `/api/peliculas/1/resenas` | Consultar película junto con sus reseñas |

Los números incluidos en las rutas son ejemplos y pueden reemplazarse por los identificadores correspondientes.

## 7. Carga de datos y pruebas

Para registrar datos se utilizan los endpoints POST. No se requiere cargar datos iniciales manualmente para que la API funcione.

El archivo `pruebas/api.http` contiene solicitudes HTTP para probar las operaciones.

Para ejecutarlas:

1. Abrir el proyecto en Visual Studio Code.
2. Instalar la extensión REST Client.
3. Abrir `pruebas/api.http`.
4. Ejecutar las solicitudes mediante **Send Request**.

Primero se debe registrar una película mediante POST. Después se puede utilizar su identificador para registrar reseñas y probar el endpoint que combina ambas bases.

Las solicitudes POST pueden crear registros adicionales y PATCH modifica registros existentes.

## 8. Detener y reiniciar el proyecto

Para detener los contenedores:

```powershell
docker compose down
```

Para volver a iniciarlos:

```powershell
docker compose up -d
```

Los datos se mantienen almacenados en los volúmenes de MySQL y MongoDB.

No utilizar `docker compose down -v` si se desea conservar la información.