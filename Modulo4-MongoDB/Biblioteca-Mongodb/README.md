# Sistema de Gestion de Biblioteca Personal (MongoDB)

Aplicacion de linea de comandos desarrollada en Python que permite administrar una biblioteca personal utilizando MongoDB y el cliente oficial pymongo, cumpliendo con la migracion desde una base de datos relacional hacia una estructura no relacional basada en documentos JSON.

## 1. Requisitos Previos

- Python 3.8 o superior instalado en el equipo.
- Docker Desktop instalado y activo.

## 2. Configuracion de MongoDB mediante Docker

Para evitar instalaciones pesadas o complejas en el sistema operativo, esta aplicacion utiliza un contenedor de Docker para ejecutar MongoDB de manera local.

1. Asegurate de tener abierto Docker Desktop.
2. Abre tu terminal y ejecuta el siguiente comando para descargar y levantar el contenedor de MongoDB:
   docker run --name mi-mongo -d -p 27017:27017 mongo:latest
3. Verifica que el contenedor este corriendo correctamente ejecutando:
   docker ps

## 3. Instalacion de Dependencias

Ubícate en la carpeta del proyecto a traves de la terminal e instala la libreria necesaria con el siguiente comando:

pip install -r requirements.txt

## 4. Ejecucion de la Aplicacion

Una vez configurada la base de datos y las dependencias, inicia el sistema ejecutando el script principal:

python main.py

## 5. Estructura Esperada del Documento en MongoDB

Cada libro registrado se almacena como un documento independiente dentro de la coleccion libros en la base de datos biblioteca_personal. Su estructura JSON es la siguiente:

{
  "_id": {
    "$oid": "651a2b3c4d5e6f7a8b9c0d1e"
  },
  "titulo": "Cien anos de soledad",
  "autor": "Gabriel Garcia Marquez",
  "genero": "Realismo magico",
  "estado": "Leido"
}

## 6. Ejemplos de Entradas Validas

- Agregar libro (Opcion 1 del menu):
  - Titulo: El Hobbit
  - Autor: J.R.R. Tolkien
  - Genero: Fantasia
  - Estado: Pendiente

- Buscar libros (Opcion 3 del menu):
  - Seleccionar la opcion 1 (Buscar por titulo) e ingresar el termino: Hobbit.
