
CREATE PROCEDURE populate_jobs
AS

IF OBJECT_ID(N'jobs', N'U') IS NULL
CREATE TABLE  jobs (
        id INTEGER PRIMARY KEY,
        job VARCHAR(300),
        create_datetime DATETIME,
        update_datetime DATETIME
);


IF OBJECT_ID(N'wrk_jobs', N'U') IS NOT NULL
TRUNCATE TABLE wrk_jobs;

IF OBJECT_ID(N'wrk_jobs', N'U') IS NOT NULL
DROP TABLE wrk_jobs;


select r.*, j.id as id_job
, j.job as job_orig, j.create_datetime
into wrk_jobs
from raw_jobs r
left join jobs j 
on r.id = j.id;


insert into jobs
select id, job, getdate(), null
from wrk_jobs
where id_job is null ;

IF NOT EXISTS (SELECT * from jobs where id = 0)  
insert into jobs values (0, 'Desconocido', GETDATE(), null)


update j
set j.job = c.job,
j.update_datetime = GETDATE()
from jobs j
join wrk_jobs c
on j.id = c.id 
where j.job <> c.job_orig
;
