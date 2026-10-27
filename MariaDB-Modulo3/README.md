# Aplicacion de Biblioteca Personal con MariaDB y SQLAlchemy

## Requisitos previos e instalacion de MariaDB

1. Descarga e instala MariaDB Server en tu sistema operativo correspondiente desde el sitio oficial de MariaDB.
2. Inicia el servicio de MariaDB y accede a la consola como administrador:
   mysql -u root -p

O bien, puedes utilizar HeidiSQL para crear la base de datos ejecutando la siguiente consulta:
CREATE DATABASE bibliotecapersonal;
USE bibliotecapersonal;

## Estructura del Proyecto

MariaDB-Modulo3/
│
├── Codigo Fuente/
│   ├── conexion.py
│   └── menu principal.py
│
├── requirements.txt
└── README.md

## Instalacion y Configuracion

1. Abre una terminal en la carpeta principal del proyecto (MariaDB-Modulo3) e instala las dependencias necesarias ejecutando:
   pip install -r requirements.txt

2. Asegurate de configurar tus credenciales (usuario y contraseña) en el archivo Codigo Fuente/conexion.py.

## Ejecucion de la Aplicacion

1. Desde la terminal, entra a la carpeta del codigo fuente:
   cd "Codigo Fuente"

2. Ejecuta el programa principal:
   python "menu principal.py"