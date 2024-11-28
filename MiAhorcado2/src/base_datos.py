import mysql.connector

class BaseDeDatos:
    def __init__(self, host="localhost", user="root", password="", database="ahorcado"):
        # Inicializa los parámetros de conexión a la base de datos
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None  # Inicializa la conexión como None

    def conectar(self):
        """Establece la conexión a la base de datos."""
        # Crea la conexión utilizando los parámetros proporcionados
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        # Cierra la conexión si está abierta
        if self.conexion:
            self.conexion.close()

class GestorAhorcado:
    def __init__(self, db: BaseDeDatos):
        # Recibe una instancia de BaseDeDatos y conecta automáticamente
        self.db = db
        self.db.conectar()

    def obtener_palabras(self, categoria):
        """Recupera una lista de palabras de la base de datos según la categoría seleccionada."""
        cursor = self.db.conexion.cursor()

        if categoria == 'Frutas':
            cursor.execute("SELECT nombre FROM Frutas")
        elif categoria == 'Conceptos_informaticos':
            cursor.execute("SELECT nombre FROM Conceptos_informaticos")
        elif categoria == 'Nombres_persona':
            cursor.execute("SELECT nombre FROM Nombres_persona")

        palabras = cursor.fetchall()  # Obtiene todas las palabras de la consulta
        cursor.close()
        return [palabra[0] for palabra in palabras]  # Devuelve una lista de palabras

    def actualizar_victorias(self, usuario):
        """Actualiza el contador de partidas ganadas del usuario en la base de datos."""
        cursor = self.db.conexion.cursor()
        # Incrementa el contador de partidas ganadas para el usuario especificado
        cursor.execute("UPDATE usuarios SET partidas_ganadas = partidas_ganadas + 1 WHERE nombre = %s", (usuario,))
        self.db.conexion.commit()
        cursor.close()

    def actualizar_derrotas(self, usuario):
        """Actualiza el contador de partidas perdidas del usuario en la base de datos."""
        cursor = self.db.conexion.cursor()  # Crea un cursor
        # Incrementa el contador de partidas perdidas para el usuario especificado
        cursor.execute("UPDATE usuarios SET partidas_perdidas = partidas_perdidas + 1 WHERE nombre = %s", (usuario,))
        self.db.conexion.commit()
        cursor.close()

    def obtener_datos_usuario(self, usuario):
        """Recupera los datos del usuario (partidas ganadas y perdidas) desde la base de datos."""
        cursor = self.db.conexion.cursor()
        # Obtiene el total de partidas ganadas y perdidas para el usuario
        cursor.execute("SELECT SUM(partidas_ganadas), SUM(partidas_perdidas) FROM usuarios WHERE nombre = %s", (usuario,))
        datos = cursor.fetchone()  # Recupera los datos

        if datos is None or datos[0] is None or datos[1] is None:
            # Si el usuario no existe, insertarlo en la base de datos
            cursor.execute("INSERT INTO usuarios (nombre, partidas_ganadas, partidas_perdidas) VALUES (%s, 0, 0)", (usuario,))
            self.db.conexion.commit()
            datos = (0, 0)  # Devuelve un conteo inicial de cero

        cursor.close()
        return datos
