import pandas as pd
from datetime import datetime
import hashlib


class Employee:
    def __init__(self, conexion, csv_file, engine):
        self.conexion = conexion
        self.csv_file = csv_file
        self.engine = engine

    def crea_tabla_raw(self):

        print("ejecuta creación de tabla raw_employees")

        cursor = self.conexion.cursor()

        create_query = """IF OBJECT_ID(N'raw_employees', N'U') IS NULL
        CREATE TABLE raw_employees (
        id             INTEGER PRIMARY KEY,
        name           VARCHAR(300),
        hired_datetime DATETIME,
        department_id  INTEGER,
        job_id         INTEGER,
        md5_hash       VARCHAR(50),
        sys_datetime   DATETIME
        )
        TRUNCATE TABLE raw_employees
        ;
        """
        
        cursor.execute(create_query)
        self.conexion.commit()


    def cargar_datos_raw(self):

        print("se realiza carga a tabla raw_employees")

        df = pd.read_csv(self.csv_file, header=None, names=['id','raw_name','raw_hired_datetime','raw_department_id', 'raw_job_id'])
        tabla_sql_server = 'raw_employees'

        # Se realiza transformación para aplicar calidad a los datos
        df['sys_datetime'] = datetime.now()
        df['name'] = df['raw_name'].fillna('Desconocido')
        df['department_id'] = df['raw_department_id'].fillna(0).astype(int)
        df['job_id'] = df['raw_job_id'].fillna(0).astype(int)
        df['null_hired_datetime'] = df['raw_hired_datetime'].fillna('1900-01-01')
        df['substr_hired_datetime'] = df['null_hired_datetime'].str.slice(0, 10)
        df['hired_datetime'] = pd.to_datetime(df['substr_hired_datetime'], format='%Y-%m-%d') 

        cols = ['name','hired_datetime','department_id', 'job_id']
        df_cadena_concatenada = df[cols].astype(str).apply(lambda x: '|'.join(x), axis=1)
        df['md5_hash'] = df_cadena_concatenada.apply(lambda x: hashlib.md5(x.encode()).hexdigest())

        nuevas_columnas = ['id','name','hired_datetime','department_id', 'job_id','md5_hash','sys_datetime']
        raw_df  = df[nuevas_columnas]

        raw_df.to_sql(tabla_sql_server, con=self.engine, if_exists='replace', index=False)


    def cargar_tabla_emp(self):

        print("ejecuta carga de tabla employees")

        cursor = self.conexion.cursor()
        exec_proc_query='exec populate_employees'
        cursor.execute(exec_proc_query)
        self.conexion.commit()
