
CREATE PROC populate_departments
AS

IF OBJECT_ID(N'departments', N'U') IS NULL
CREATE TABLE  departments (
        id INTEGER PRIMARY KEY,
        department VARCHAR(300),
        create_datetime DATETIME,
        update_datetime DATETIME
);


IF OBJECT_ID(N'wrk_departments', N'U') IS NOT NULL
TRUNCATE TABLE wrk_departments;

IF OBJECT_ID(N'wrk_departments', N'U') IS NOT NULL
DROP TABLE wrk_departments;


select r.*, d.id as id_department
, d.department as department_orig, d.create_datetime
into wrk_departments
from raw_departments r
left join departments d 
on r.id = d.id;


insert into departments
select id, department, getdate(), null
from wrk_departments
where id_department is null ;

IF NOT EXISTS (SELECT * from departments where id = 0)  
insert into departments values (0, 'Desconocido', GETDATE(), null)


update d
set d.department = c.department,
d.update_datetime = GETDATE()
from departments d
join wrk_departments c
on d.id = c.id 
where d.department <> c.department_orig
;
