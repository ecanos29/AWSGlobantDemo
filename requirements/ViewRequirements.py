import os
import sqlite3
import matplotlib.pyplot as plt



def graph_hired_employees(conn,cur):

    try:
        
        #Query que muestra los departamente que contrataron más empleados que la media
        hired_query = """
        with hired_by_dept AS (
        select department_id, count(*) as num_hired
        FROM employees
        WHERE strftime('%Y', hired_datetime) = '2021'
        group by department_id
        )
        select h.department_id, d.department, h.num_hired from hired_by_dept h
        join departments d
        on h.department_id = d.id
        where num_hired > (select avg(num_hired) as avg_hired from hired_by_dept) 
        order by 3 desc;
        """

        print(hired_query)

        # Ejecutar el query
        cur.execute(hired_query)
        resultados = cur.fetchall()
        conn.close()

        # Separar los resultados en listas separadas para cada columna
        ids = [fila[0] for fila in resultados]
        departamentos = [fila[1] for fila in resultados]
        num_empleados = [fila[2] for fila in resultados]

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(ids, num_empleados)
        plt.xlabel('ID y Departamento')
        plt.ylabel('Número de Empleados')
        plt.title('Número de Empleados por ID y Departamento')
        plt.xticks(ids, departamentos, rotation=45)
        plt.tight_layout()
        plt.show()


    except Exception as e:
        print("Error al cargar el archivo:", e)
        conn.close()


current_directory = os.path.dirname(os.path.abspath(__file__))
sqlite_db = os.path.join(current_directory, "SQLIte_db", "GlobantDemo")


conn = sqlite3.connect(sqlite_db)
cur = conn.cursor()
graph_hired_employees(conn,cur)


