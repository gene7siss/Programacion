from conexion import SessionLocal, Libro

def mostrar_menu():
    print("\n--- BIBLIOTECA PERSONAL ---")
    print("1. Agregar libro")
    print("2. Ver libros")
    print("3. Salir")

def agregar_libro(session):
    titulo = input("Ingresa el título del libro: ")
    autor = input("Ingresa el autor del libro: ")
    anio = int(input("Ingresa el año de publicación: "))

    nuevo_libro = Libro(titulo=titulo, autor=autor, anio=anio)
    session.add(nuevo_libro)
    session.commit()
    print("¡Libro agregado con éxito!")

def ver_libros(session):
    libros = session.query(Libro).all()
    if not libros:
        print("\nNo hay libros registrados en la biblioteca.")
    else:
        print("\n--- LISTA DE LIBROS ---")
        for libro in libros:
            print(f"ID: {libro.id} | Título: {libro.titulo} | Autor: {libro.autor} | Año: {libro.anio}")

def main():
    session = SessionLocal()
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            agregar_libro(session)
        elif opcion == "2":
            ver_libros(session)
        elif opcion == "3":
            print("¡Saliendo de la aplicación. Adiós!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")
    
    session.close()

if __name__ == "__main__":
    main()