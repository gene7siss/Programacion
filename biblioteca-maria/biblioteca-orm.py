from sqlalchemy import Column, Integer, String, create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DB_USER = "root"
DB_PASSWORD = "1771"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "biblioteca-db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error al configurar el motor de base de datos: {e}")
    exit(1)

class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False)

    def __repr__(self):
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | Género: {self.genero} | Estado: {self.estado}"

try:
    Base.metadata.create_all(bind=engine)
except SQLAlchemyError as e:
    print(f"Error al crear las tablas en la base de datos: {e}")

def agregar_libro():
    session = SessionLocal()
    try:
        print("\n--- Agregar Nuevo Libro ---")
        titulo = input("Ingrese el título: ").strip()
        autor = input("Ingrese el autor: ").strip()
        genero = input("Ingrese el género: ").strip()
        estado = input("Ingrese el estado de lectura: ").strip()

        nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
        session.add(nuevo_libro)
        session.commit()
        print("Libro agregado exitosamente.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error de base de datos al agregar: {e}")
    finally:
        session.close()

def ver_libros():
    session = SessionLocal()
    try:
        libros = session.query(Libro).all()
        if not libros:
            print("\nNo hay libros registrados.")
            return
        print("\n--- Listado de Libros ---")
        for libro in libros:
            print(libro)
    except SQLAlchemyError as e:
        print(f"Error al consultar los libros: {e}")
    finally:
        session.close()

def actualizar_libro():
    session = SessionLocal()
    try:
        ver_libros()
        id_libro = int(input("\nIngrese el ID del libro que desea actualizar: "))
        libro = session.query(Libro).filter_by(id=id_libro).first()

        if not libro:
            print("No se encontró un libro con ese ID.")
            return

        print(f"Modificando a: {libro.titulo}. Deje en blanco si no desea cambiar el campo.")
        
        nuevo_titulo = input(f"Nuevo título [{libro.titulo}]: ").strip()
        nuevo_autor = input(f"Nuevo autor [{libro.autor}]: ").strip()
        nuevo_genero = input(f"Nuevo género [{libro.genero}]: ").strip()
        nuevo_estado = input(f"Nuevo estado [{libro.estado}]: ").strip()

        if nuevo_titulo: libro.titulo = nuevo_titulo
        if nuevo_autor: libro.autor = nuevo_autor
        if nuevo_genero: libro.genero = nuevo_genero
        if nuevo_estado: libro.estado = nuevo_estado

        session.commit()
        print("Libro actualizado correctamente.")
    except ValueError:
        print("Por favor, ingrese un ID válido.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al actualizar el libro: {e}")
    finally:
        session.close()

def eliminar_libro():
    session = SessionLocal()
    try:
        ver_libros()
        id_libro = int(input("\nIngrese el ID del libro que desea eliminar: "))
        libro = session.query(Libro).filter_by(id=id_libro).first()

        if not libro:
            print("No se encontró un libro con ese ID.")
            return

        session.delete(libro)
        session.commit()
        print("Libro eliminado exitosamente.")
    except ValueError:
        print("Por favor, ingrese un ID válido.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al eliminar el libro: {e}")
    finally:
        session.close()

def buscar_libros():
    session = SessionLocal()
    try:
        criterio = input("\nIngrese término de búsqueda: ").strip()
        resultados = session.query(Libro).filter(
            or_(
                Libro.titulo.ilike(f"%{criterio}%"),
                Libro.autor.ilike(f"%{criterio}%"),
                Libro.genero.ilike(f"%{criterio}%")
            )
        ).all()

        if not resultados:
            print("No se encontraron coincidencias.")
            return

        print(f"\n--- Resultados de Búsqueda ({len(resultados)}) ---")
        for libro in resultados:
            print(libro)
    except SQLAlchemyError as e:
        print(f"Error en la búsqueda: {e}")
    finally:
        session.close()

def main():
    while True:
        print("\n==============================")
        print("BIBLIOTECA PERSONAL (MARIADB)")
        print("==============================")
        print("1. Agregar nuevo libro")
        print("2. Ver listado de libros")
        print("3. Actualizar información de un libro")
        print("4. Eliminar libro existente")
        print("5. Buscar libros")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            ver_libros()
        elif opcion == "3":
            actualizar_libro()
        elif opcion == "4":
            eliminar_libro()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()