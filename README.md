# AWS Globant’s Data Engineering Coding Challenge

## Description

The development of a REST API that inserts information from flat files into three tables (departments, jobs, employees). 
The solution was developed on AWS Amazon EC2, in addition to a SQL Server database installed on Amazon RDS.

## Project Content

The project is composed of several folders, which are described below.

src:  Python code for the REST API is placed in this folder.
Requirements:  Here is the Python and SQL code that demonstrates the requirements requested in section 2.
files: csv files is placed in this folder.
SQL: SQL code that populates tables departments, jobs and employees from raw tables.

## Technologies

This project was built with the following technologies:

* Python
* Pandas
* Flask
* SQL Server
* Amazon EC2
* Amazon RDS

## Prerequisites

Git and Docker must be installed into devolpment environment.

## Installation

Create new directory where project will be located and move to new directory.

To clone the repository from GitHub into local directory, execute the following command:

* git clone https://github.com/ecanos29/AWSGlobantDemo.git


Create a docker image, execute: 

* docker build -t restapidemo_img .


Creatate a docker container, execute:

* docker run --name=restapidemo_app -e PYTHONUNBUFFERED=1 -d -p 5000:5000 restapidemo_img



