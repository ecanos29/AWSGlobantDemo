import pandas as pd
from datetime import datetime


class Departament:
    def __init__(self, conexion, csv_file, engine):
        self.conexion = conexion
        self.csv_file = csv_file
        self.engine = engine

    def crea_tabla_raw(self):

        print("ejecuta creación de tabla raw_departments")

        cursor = self.conexion.cursor()

        create_query = """IF OBJECT_ID(N'raw_departments', N'U') IS NULL
        CREATE TABLE raw_departments (
        id INTEGER PRIMARY KEY,
        department VARCHAR(300),
        sys_datetime DATETIME
        )
        TRUNCATE TABLE raw_departments
        ;
        """
        
        cursor.execute(create_query)
        self.conexion.commit()


    def cargar_datos_raw(self):

        print("se realiza carga a tabla raw_departments")

        df = pd.read_csv(self.csv_file, header=None, names=['id','department'])
        tabla_sql_server = 'raw_departments' 

        df.to_sql(tabla_sql_server, con=self.engine, if_exists='replace', index=False)



    def cargar_tabla_dept(self):

        print("ejecuta carga de tabla departments")

        cursor = self.conexion.cursor()
        exec_proc_query='exec populate_departments'
        cursor.execute(exec_proc_query)
        self.conexion.commit()
