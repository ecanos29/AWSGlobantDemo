
-- Requirement 1

with quater as (
SELECT id, name, hired_datetime, department_id, job_id,
case when hired_datetime BETWEEN '2021-01-01 00:00:00' AND '2021-03-31 23:59:59' then 1 else 0 end as q1,
case when hired_datetime BETWEEN '2021-04-01 00:00:00' AND '2021-06-30 23:59:59' then 1 else 0 end as q2,
case when hired_datetime BETWEEN '2021-07-01 00:00:00' AND '2021-09-30 23:59:59' then 1 else 0 end as q3,
case when hired_datetime BETWEEN '2021-10-01 00:00:00' AND '2021-12-31 23:59:59' then 1 else 0 end as q4
FROM employees
WHERE strftime('%Y', hired_datetime) = '2021'
)
select department, job,
sum(q1) as q1, sum(q2) as q2, sum(q3) as q3, sum(q4) as q4 
from quater q
join departments d
on q.department_id = d.id
join jobs j
on q.job_id = j.id
group by department, job
order by 1,2 
;

-- Requirement 2

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
order by 3 desc
