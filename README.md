# IBM-Data-Engineering-5.Week-Project
SQL (MSSQL Database) and Python
------------------------------------------------------------------
Here is my project for the 5th week of IBM Data Engineer course. Using MSSQL database, I have created a membership system for the rock-paper-scissors game where players can register and keep track of their points. The system allows real-time recording of points, enabling basic analysis of the data. There is also an analysis page too supported by line and bar charts.

In future versions: 
1. Detailed analysis of the data will be performed using the pandas module. Maybe we can use other modul too.
2. I will try to run the local database on Azure Cloud or IBM Cloud in the future.

------------------------------------------------------------------
We firstly need to create a database in MSSQL.

"CREATE DATABASE game_database"

then we must add tables.

scores table =
CREATE TABLE scores(id int not null, game nvarchar(20) not null,
date nvarchar(50) not null, score int not null)

userpas table = 
CREATE TABLE userpas(id int not null PRIMARY KEY, username varchar(20) not null,
password varchar(20) not null);

------------------------------------------------------------------

Ps: if you dont know how to open database in MSSQL, you must use to (SQL Server Authentication) tab in login page.

------------------------------------------------------------------

Ps: if you get any error or question please contact with me. :)

------------------------------------------------------------------
