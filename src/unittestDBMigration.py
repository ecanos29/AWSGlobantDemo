import unittest
import os
import pandas as pd
from conexionsqlserver import ConexionSQLServer 

class TestDatabaseMigration(unittest.TestCase):
    
    # Genera las rutas para los insumos del unit test 
    def setUp(self):
        self.ruta_actual = os.path.abspath(os.path.dirname(__file__))
        self.ruta_padre = os.path.dirname(self.ruta_actual)
        self.dep_csv_file = os.path.join(self.ruta_padre, "files", "departments.csv")
        self.job_csv_file = os.path.join(self.ruta_padre, "files", "jobs.csv")
        self.emp_csv_file = os.path.join(self.ruta_padre, "files", "hired_employees.csv")
       


    # Prueba para validar el número de registros entre fuente y destino para departments
    def test_departments_count(self):

        df_dep_csv = pd.read_csv(self.dep_csv_file, header=None)

        conn = ConexionSQLServer()

        query = "SELECT count(*) FROM departments where id > 0"

        df_dep_db = pd.read_sql_query(query, conn)
        
        num_rec_csv = len(df_dep_csv)
        num_rec_db =  df_dep_db.iloc[0, 0]
        conn.close()

        self.assertEqual(num_rec_csv, num_rec_db, "El número de registros en el archivo CSV no coincide con el número de registros en la tabla 'departments' de la base de datos")



    # Prueba para validar la integridad de los datos entre fuente y destino para departments
    def test_departments_values(self):

        df_dep_csv = pd.read_csv(self.dep_csv_file, header=None, names=['id','department'])

        conn = ConexionSQLServer()
        query = "SELECT * FROM departments where id > 0"

        df_dep_db = pd.read_sql_query(query, conn)

        df_join = pd.merge(df_dep_db, df_dep_db, on='id', suffixes=('_db', '_csv'))        
        diff = df_join[df_join['department_db'] != df_join['department_csv']]

        conn.close()

        
        self.assertTrue(diff.empty, f"Hay diferencias entre los datos de la tabla 'departments' en la base de datos y los datos del archivo CSV original:\n{diff}")



    # Prueba para validar el número de registros entre fuente y destino para jobs
    def test_jobs_count(self):

        df_job_csv = pd.read_csv(self.job_csv_file, header=None)

        conn = ConexionSQLServer()
        query = "SELECT count(*) FROM jobs where id > 0"

        df_job_db = pd.read_sql_query(query, conn)
        
        num_job_csv = len(df_job_csv)
        num_job_db =  df_job_db.iloc[0, 0]
        conn.close()

        self.assertEqual(num_job_csv, num_job_db, "El número de registros en el archivo CSV no coincide con el número de registros en la tabla 'jobs' de la base de datos")



    # Prueba para validar la integridad de los datos entre fuente y destino para jobs
    def test_jobs_values(self):

        df_job_csv = pd.read_csv(self.job_csv_file, header=None, names=['id','job'])

        conn = ConexionSQLServer()
        query = "SELECT * FROM jobs where id > 0"

        df_job_db = pd.read_sql_query(query, conn)

        df_join = pd.merge(df_job_db, df_job_db, on='id', suffixes=('_db', '_csv'))        
        diff = df_join[df_join['job_db'] != df_join['job_csv']]

        conn.close()

        # Asegurar que no hay diferencias
        self.assertTrue(diff.empty, f"Hay diferencias entre los datos de la tabla 'jobs' en la base de datos y los datos del archivo CSV original:\n{diff}")



    # Prueba para validar el número de registros entre fuente y destino para employees
    def test_employees_count(self):

        df_emp_csv = pd.read_csv(self.emp_csv_file, header=None)

        conn = ConexionSQLServer()
        query = "SELECT count(*) FROM employees"

        df_emp_db = pd.read_sql_query(query, conn)
        
        num_emp_csv = len(df_emp_csv)
        num_emp_db =  df_emp_db.iloc[0, 0]
        conn.close()

        self.assertEqual(num_emp_csv, num_emp_db, "El número de registros en el archivo CSV no coincide con el número de registros en la tabla 'employees' de la base de datos")



    # Prueba para validar la integridad relacional entre la tabla employees y las tablas jobs y departments
    def test_employees_ref_integrity(self):

        conn = ConexionSQLServer()

        query_a = "SELECT count(*) FROM employees"
        df_emp_a_db = pd.read_sql_query(query_a, conn)


        query_b = """SELECT count(*) FROM employees e 
                   join departments d on e.department_id = d.id 
                   join jobs j on e.job_id = j.id
                   """
        df_emp_b_db = pd.read_sql_query(query_b, conn)


        
        num_emp_db_a = df_emp_a_db.iloc[0, 0]
        num_emp_db_b =  df_emp_b_db.iloc[0, 0]

        conn.close()

        self.assertEqual(num_emp_db_a, num_emp_db_b, "El número de registros no coincide en la tabla 'employees' no coincide al unir las tablas catálogo")



    # Prueba para validar la integridad de los datos entre fuente y destino para employees
    def test_employees_values(self):

        
        df = pd.read_csv(self.emp_csv_file, header=None, names=['id','raw_name','raw_hired_datetime','raw_department_id', 'raw_job_id'])


        df['name'] = df['raw_name'].fillna('Desconocido')
        df['department_id'] = df['raw_department_id'].fillna(0).astype('int64')
        df['job_id'] = df['raw_job_id'].fillna(0).astype('int64')
        df['null_hired_datetime'] = df['raw_hired_datetime'].fillna('1900-01-01')
        df['substr_hired_datetime'] = df['null_hired_datetime'].str.slice(0, 10)
        df['hired_datetime'] = pd.to_datetime(df['substr_hired_datetime'], format='%Y-%m-%d')

        nuevas_columnas = ['id','name','hired_datetime','department_id', 'job_id']
        df_emp_csv  = df[nuevas_columnas]

        conn = ConexionSQLServer()
        query = "SELECT id, name, hired_datetime, department_id, job_id FROM employees"

        df_emp_db = pd.read_sql_query(query, conn)

        
       
        df_join = pd.merge(df_emp_db, df_emp_csv, on='id', suffixes=('_db', '_csv'))

        diff_name = df_join[df_join['name_db'] != df_join['name_csv']]
        diff_job_id = df_join[df_join['job_id_db'] != df_join['job_id_csv']]
        diff_department_id = df_join[df_join['department_id_db'] != df_join['department_id_csv']]
        diff_date = df_join[df_join['hired_datetime_db'] != df_join['hired_datetime_csv']]

        diff = pd.concat([diff_name, diff_job_id, diff_department_id, diff_date])

        conn.close()
        
        
        self.assertTrue(diff.empty, f"Hay diferencias entre los datos de la tabla 'employees' en la base de datos y los datos del archivo CSV original en las siguientes columnas:\n{diff}")

        


if __name__ == '__main__':
    unittest.main()