import pandas as pd
from datetime import datetime


class Job:
    def __init__(self, conexion, csv_file, engine):
        self.conexion = conexion
        self.csv_file = csv_file
        self.engine = engine

    def crea_tabla_raw(self):

        print("ejecuta creación de tabla raw_jobs")

        cursor = self.conexion.cursor()

        create_query = """IF OBJECT_ID(N'raw_jobs', N'U') IS NULL
        CREATE TABLE raw_jobs (
        id INTEGER PRIMARY KEY,
        job VARCHAR(300),
        sys_datetime DATETIME
        )
        TRUNCATE TABLE raw_jobs
        ;
        """
        
        cursor.execute(create_query)
        self.conexion.commit()


    def cargar_datos_raw(self):

        print("se realiza carga a tabla raw_jobs")

        
        df = pd.read_csv(self.csv_file, header=None, names=['id','job'])
        tabla_sql_server = 'raw_jobs' 

        df.to_sql(tabla_sql_server, con=self.engine, if_exists='replace', index=False)




    def cargar_tabla_job(self):

        print("ejecuta carga de tabla jobs")

        cursor = self.conexion.cursor()
        exec_proc_query='exec populate_jobs'
        cursor.execute(exec_proc_query)
        self.conexion.commit()
