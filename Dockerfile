FROM python:3.9

WORKDIR /app

# Instala las bibliotecas ODBC
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

# Instala el controlador de SQL Server
RUN apt-get update && \
    apt-get install -y gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copia los archivos de configuración del controlador de SQL Server
COPY odbc.ini /etc/odbc.ini
COPY odbcinst.ini /etc/odbcinst.ini


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

CMD ["python", "-u" , "src/restapi.py"]