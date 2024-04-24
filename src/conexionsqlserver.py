import pyodbc
from sqlalchemy import create_engine

class ConexionSQLServer:
    def __init__(self):
        self.server = 'globant-demo.c9s480uya5o5.us-east-2.rds.amazonaws.com'
        self.database = 'globant_db'
        self.username = 'masterUsername'
        self.password = 'admin123'
        self.conn = self.conectar()
        self.engine = self.obten_engine()

    def conectar(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        print(conn_str)
        return pyodbc.connect(conn_str)

    def obten_engine(self):
        engine_str = f'mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server'
        print(engine_str)
        return create_engine(engine_str)

