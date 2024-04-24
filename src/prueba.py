import os
from department import Departament
from conexionsqlserver import ConexionSQLServer
from job import Job
from employee import Employee


# Ruta del archivo CSV
ruta_actual = os.path.abspath(os.path.dirname(__file__))
ruta_padre = os.path.dirname(ruta_actual)
dep_csv_file = os.path.join(ruta_padre, "files", "departments.csv") 
job_csv_file = os.path.join(ruta_padre, "files", "jobs.csv") 
emp_csv_file = os.path.join(ruta_padre, "files", "hired_employees.csv") 

print(dep_csv_file)
print(job_csv_file)
print(emp_csv_file)

# Crear instancia de la clase ConexionSQLServer
conexion = ConexionSQLServer()


# Crear instancia de la clase Departamento y cargar datos
departament = Departament(conexion.conn, dep_csv_file)

departament.crea_tabla_raw()
departament.cargar_datos_raw() 
departament.cargar_tabla_dept()


job = Job(conexion.conn, job_csv_file)

job.crea_tabla_raw()
job.cargar_datos_raw() 
job.cargar_tabla_job()

employee = Employee(conexion.conn, emp_csv_file)

employee.crea_tabla_raw()
#employee.cargar_datos_raw() 
employee.cargar_tabla_emp()
