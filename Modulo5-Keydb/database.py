import os
import json
import redis
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

HOST = os.getenv("KEYDB_HOST", "localhost")
PORT = int(os.getenv("KEYDB_PORT", 6379))
PASSWORD = os.getenv("KEYDB_PASSWORD") or None

class BibliotecaKeyDB:
    def __init__(self):
        try:
            # Inicializar la conexión con KeyDB/Redis
            self.client = redis.Redis(
                host=HOST,
                port=PORT,
                password=PASSWORD,
                decode_responses=True # Para obtener strings en lugar de bytes
            )
            # Probar la conexión
            self.client.ping()
            print(" Conexión exitosa a KeyDB.")
        except redis.ConnectionError as e:
            print(f" Error de conexión a KeyDB: {e}")
            raise

    def generar_id(self):
        """Genera un ID correlativo único para cada libro usando un contador."""
        return self.client.incr("contador_libros")

    def agregar_libro(self, titulo, autor, genero, estado):
        libro_id = self.generar_id()
        clave = f"libro:{libro_id}"
        
        data = {
            "id": libro_id,
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }
        
        # Guardar como JSON string usando SET
        self.client.set(clave, json.dumps(data))
        return libro_id

    def obtener_todos(self):
        """Obtiene el listado de todos los libros registrados usando SCAN."""
        libros = []
        cursor = 0
        # SCAN es más seguro que KEYS en producción para buscar patrones
        while True:
            cursor, keys = self.client.scan(cursor=cursor, match="libro:*", count=100)
            for key in keys:
                data_json = self.client.get(key)
                if data_json:
                    libros.append(json.loads(data_json))
            if cursor == 0:
                break
        return libros

    def actualizar_libro(self, libro_id, titulo, autor, genero, estado):
        clave = f"libro:{libro_id}"
        if not self.client.exists(clave):
            return False
        
        data = {
            "id": int(libro_id),
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }
        self.client.set(clave, json.dumps(data))
        return True

    def eliminar_libro(self, libro_id):
        clave = f"libro:{libro_id}"
        return self.client.delete(clave) > 0

    def buscar_libros(self, criterio):
        """Busca libros por título, autor o género (coincidencia parcial)."""
        criterio = criterio.lower()
        todos = self.obtener_todos()
        resultados = []
        for libro in todos:
            if (criterio in libro["titulo"].lower() or 
                criterio in libro["autor"].lower() or 
                criterio in libro["genero"].lower()):
                resultados.append(libro)
        return resultados