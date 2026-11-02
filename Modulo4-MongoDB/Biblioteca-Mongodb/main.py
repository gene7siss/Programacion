import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson.objectid import ObjectId

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "biblioteca_personal"
COLLECTION_NAME = "libros"

def conectar_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except ConnectionFailure:
        print("Error critico: No se pudo conectar a la base de datos MongoDB. Verifique que el servidor este activo.")
        sys.exit(1)
    except PyMongoError as e:
        print(f"Error de MongoDB: {e}")
        sys.exit(1)

def agregar_libro(collection):
    print("\n--- Agregar Nuevo Libro ---")
    titulo = input("Ingrese el titulo del libro: ").strip()
    autor = input("Ingrese el autor del libro: ").strip()
    genero = input("Ingrese el genero del libro: ").strip()
    estado = input("Ingrese el estado de lectura (Ej. Pendiente, Leyendo, Leido): ").strip()

    if not titulo or not autor or not genero or not estado:
        print("Error: Todos los campos son obligatorios.")
        return

    documento = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        resultado = collection.insert_one(documento)
        print(f"Libro agregado exitosamente con ID: {resultado.inserted_id}")
    except PyMongoError as e:
        print(f"Error al insertar el documento: {e}")

def ver_libros(collection):
    print("\n--- Listado de Libros ---")
    try:
        libros = list(collection.find())
        if not libros:
            print("No hay libros registrados en la base de datos.")
            return

        for idx, libro in enumerate(libros, start=1):
            print(f"{idx}. ID: {libro['_id']}")
            print(f"   Titulo: {libro.get('titulo')}")
            print(f"   Autor: {libro.get('autor')}")
            print(f"   Genero: {libro.get('genero')}")
            print(f"   Estado: {libro.get('estado')}")
            print("-" * 30)
    except PyMongoError as e:
        print(f"Error al consultar los libros: {e}")

def buscar_libros(collection):
    print("\n--- Buscar Libros ---")
    print("1. Buscar por titulo")
    print("2. Buscar por autor")
    print("3. Buscar por genero")
    opcion = input("Seleccione una opcion de busqueda (1-3): ").strip()

    campo_map = {"1": "titulo", "2": "autor", "3": "genero"}
    if opcion not in campo_map:
        print("Opcion invalida.")
        return

    campo = campo_map[opcion]
    termino = input(f"Ingrese el texto a buscar para {campo}: ").strip()

    if not termino:
        print("El termino de busqueda no puede estar vacio.")
        return

    try:
        query = {campo: {"$regex": termino, "$options": "i"}}
        resultados = list(collection.find(query))

        if not resultados:
            print(f"No se encontraron resultados para '{termino}' en {campo}.")
            return

        print(f"\nSe encontraron {len(resultados)} resultados:")
        for libro in resultados:
            print(f"- ID: {libro['_id']} | Titulo: {libro['titulo']} | Autor: {libro['autor']} | Genero: {libro['genero']} | Estado: {libro['estado']}")
    except PyMongoError as e:
        print(f"Error en la busqueda: {e}")

def actualizar_libro(collection):
    print("\n--- Actualizar Libro ---")
    id_input = input("Ingrese el ID (ObjectId) del libro que desea actualizar: ").strip()

    try:
        obj_id = ObjectId(id_input)
    except Exception:
        print("Error: El ID proporcionado no tiene un formato valido de MongoDB.")
        return

    libro_actual = collection.find_one({"_id": obj_id})
    if not libro_actual:
        print("No se encontro ningun libro con ese ID.")
        return

    print(f"Libro actual encontrado: {libro_actual['titulo']} por {libro_actual['autor']}")
    print("Deje el campo en blanco si no desea modificarlo.")

    nuevo_titulo = input(f"Nuevo titulo [{libro_actual.get('titulo')}]: ").strip()
    nuevo_autor = input(f"Nuevo autor [{libro_actual.get('autor')}]: ").strip()
    nuevo_genero = input(f"Nuevo genero [{libro_actual.get('genero')}]: ").strip()
    nuevo_estado = input(f"Nuevo estado [{libro_actual.get('estado')}]: ").strip()

    updates = {}
    if nuevo_titulo:
        updates["titulo"] = nuevo_titulo
    if nuevo_autor:
        updates["autor"] = nuevo_autor
    if nuevo_genero:
        updates["genero"] = nuevo_genero
    if nuevo_estado:
        updates["estado"] = nuevo_estado

    if not updates:
        print("No se realizaron cambios.")
        return

    try:
        collection.update_one({"_id": obj_id}, {"$set": updates})
        print("Libro actualizado exitosamente.")
    except PyMongoError as e:
        print(f"Error al actualizar el documento: {e}")

def eliminar_libro(collection):
    print("\n--- Eliminar Libro ---")
    id_input = input("Ingrese el ID (ObjectId) del libro que desea eliminar: ").strip()

    try:
        obj_id = ObjectId(id_input)
    except Exception:
        print("Error: El ID proporcionado no tiene un formato valido de MongoDB.")
        return

    try:
        resultado = collection.delete_one({"_id": obj_id})
        if resultado.deleted_count > 0:
            print("Libro eliminado exitosamente.")
        else:
            print("No se encontro ningun libro con ese ID.")
    except PyMongoError as e:
        print(f"Error al eliminar el documento: {e}")

def main():
    collection = conectar_db()

    while True:
        print("\n==============================")
        print(" SISTEMA DE BIBLIOTECA - MONGODB")
        print("==============================")
        print("1. Agregar nuevo libro")
        print("2. Ver listado de libros")
        print("3. Buscar libros")
        print("4. Actualizar informacion de un libro")
        print("5. Eliminar libro existente")
        print("6. Salir")
        
        opcion = input("Seleccione una opcion (1-6): ").strip()

        if opcion == "1":
            agregar_libro(collection)
        elif opcion == "2":
            ver_libros(collection)
        elif opcion == "3":
            buscar_libros(collection)
        elif opcion == "4":
            actualizar_libro(collection)
        elif opcion == "5":
            eliminar_libro(collection)
        elif opcion == "6":
            print("Saliendo del sistema. Hasta luego.")
            break
        else:
            print("Opcion invalida. Por favor, ingrese un numero del 1 al 6.")

if __name__ == "__main__":
    main()