from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de la conexión a MariaDB (con tu usuario, contraseña y base de datos)
DATABASE_URL = "mysql+pymysql://root:1771@localhost:3306/bibliotecapersonal"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Base para los modelos
Base = declarative_base()

# Definición de la tabla de Libros
class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    anio = Column(Integer, nullable=False)

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Configurar la sesión para hacer operaciones (CRUD)
SessionLocal = sessionmaker(bind=engine)