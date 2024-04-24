import os
from flask import Flask
from department import Departament
from conexionsqlserver import ConexionSQLServer
from job import Job
from employee import Employee


app = Flask(__name__)



# Metodo que ejecuta toda la carga de la base de datos
@app.route('/db_migration', methods=['GET'])
def complete_migracion():
    # Ruta del archivo CSV
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_padre = os.path.dirname(ruta_actual)
    dep_csv_file = os.path.join(ruta_padre, "files", "departments.csv") 
    job_csv_file = os.path.join(ruta_padre, "files", "jobs.csv") 
    emp_csv_file = os.path.join(ruta_padre, "files", "hired_employees.csv") 

    conexion = ConexionSQLServer()

    # Crear instancia de la clase Departamento y cargar datos
    departament = Departament(conexion.conn, dep_csv_file, conexion.engine)

    departament.crea_tabla_raw()
    departament.cargar_datos_raw() 
    departament.cargar_tabla_dept()


    job = Job(conexion.conn, job_csv_file, conexion.engine)

    job.crea_tabla_raw()
    job.cargar_datos_raw() 
    job.cargar_tabla_job()

    employee = Employee(conexion.conn, emp_csv_file, conexion.engine)

    employee.crea_tabla_raw()
    employee.cargar_datos_raw() 
    employee.cargar_tabla_emp()


    return "Se ejecuta el proceso de carga de toda la base de datos"




# Metodo que ejecuta toda la carga la tabla "employee"
@app.route('/prueba_api', methods=['GET'])
def prueba_api():
    
    return "Servicio REST API de prueba"


# Ejecuta la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
