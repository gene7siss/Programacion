from database import BibliotecaKeyDB

def mostrar_menu():
    print("\n==============================")
    print("  BIBLIOTECA PERSONAL (KeyDB)")
    print("==============================")
    print("1. Agregar nuevo libro")
    print("2. Ver listado de libros")
    print("3. Actualizar información de un libro")
    print("4. Eliminar libro existente")
    print("5. Buscar libros (título, autor o género)")
    print("6. Salir")

def main():
    try:
        db = BibliotecaKeyDB()
    except Exception:
        print("No se pudo iniciar la aplicación debido a un error de conexión.")
        return

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- Agregar Nuevo Libro ---")
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            genero = input("Género: ").strip()
            estado = input("Estado de lectura (ej. Pendiente, Leyendo, Terminado): ").strip()

            if not titulo or not autor:
                print(" El título y el autor son obligatorios.")
                continue

            nuevo_id = db.agregar_libro(titulo, autor, genero, estado)
            print(f" ¡Libro agregado con éxito con ID: {nuevo_id}!")

        elif opcion == "2":
            print("\n--- Listado de Libros ---")
            libros = db.obtener_todos()
            if not libros:
                print(" No hay libros registrados en la base de datos.")
            else:
                for lib in libros:
                    print(f"ID: {lib['id']} | Título: {lib['titulo']} | Autor: {lib['autor']} | Género: {lib['genero']} | Estado: {lib['estado']}")

        elif opcion == "3":
            print("\n--- Actualizar Libro ---")
            libro_id = input("Ingrese el ID del libro a actualizar: ").strip()
            
            # Verificar si existe consultando directamente
            clave = f"libro:{libro_id}"
            if not db.client.exists(clave):
                print(f" No se encontró ningún libro con el ID {libro_id}.")
                continue

            print("Ingrese los nuevos datos:")
            titulo = input("Nuevo Título: ").strip()
            autor = input("Nuevo Autor: ").strip()
            genero = input("Nuevo Género: ").strip()
            estado = input("Nuevo Estado de lectura: ").strip()

            db.actualizar_libro(libro_id, titulo, autor, genero, estado)
            print(" ¡Libro actualizado correctamente!")

        elif opcion == "4":
            print("\n--- Eliminar Libro ---")
            libro_id = input("Ingrese el ID del libro a eliminar: ").strip()
            
            eliminado = db.eliminar_libro(libro_id)
            if eliminado:
                print(f" Libro con ID {libro_id} eliminado exitosamente.")
            else:
                print(f" No se encontró ningún libro con el ID {libro_id}.")

        elif opcion == "5":
            print("\n--- Buscar Libros ---")
            criterio = input("Ingrese palabra clave (título, autor o género): ").strip()
            
            resultados = db.buscar_libros(criterio)
            if not resultados:
                print("🔍 No se encontraron coincidencias.")
            else:
                print(f"Se encontraron {len(resultados)} coincidencia(s):")
                for lib in resultados:
                    print(f"ID: {lib['id']} | Título: {lib['titulo']} | Autor: {lib['autor']} | Género: {lib['genero']} | Estado: {lib['estado']}")

        elif opcion == "6":
            print("\n Saliendo del programa de forma segura. ¡Hasta luego!")
            break
        else:
            print(" Opción inválida. Por favor, elija un número entre 1 y 6.")

if __name__ == "__main__":
    main()