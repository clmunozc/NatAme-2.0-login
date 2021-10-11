import cx_Oracle

class connect():

    def __init__(self,user="natame",passw="natame"):
        host = "localhost"
        tsname = "XE"
        self.connected=False

        #lib_dir = r"C:\Users\USER\Downloads\Instaladores\instantclient_19_10"
        lib_dir = r"C:\oracle_instantclient\instantclient_19_11"

        try:
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        except Exception as err:
            print("Error connecting: cx_Oracle.init_oracle_client()")
            print(err)
        else:
            print("Libreria cargada exitosamente")

        try:
            self.conexion = cx_Oracle.connect(user, passw, host+"/"+tsname)
            self.connected=True
        except Exception as error:
            print("No se pudo conectar a la base de datos. Error: ")
            print(error)
        print("Conexion Establecida!!!")

    @staticmethod
    def getConnection(self):
        return self.conexion

    def getConnectionState(self):
        if self.connected:
            return True
        else:
            return False

    def close(self):
        if self.conexion:
            self.conexion.close()

    def commint(self):
        self.conexion.commit()
        
    def sentenciaSimple(self, sentencia):
        cursor = self.conexion.cursor()
        cursor.execute(sentencia)
        cursor.close()

    def sentenciaCompuesta(self, sentencia):
        cursor = self.conexion.cursor()
        cursor.execute(sentencia)
        datos = cursor.fetchall()
        cursor.close
        return datos