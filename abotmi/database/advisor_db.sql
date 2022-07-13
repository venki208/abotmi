drop database if exists advisor_db;
create database advisor_db CHARACTER SET utf8 COLLATE utf8_general_ci;
grant all on advisor_db.* to 'advisoradmin'@'localhost' identified by 'advisoradmin@123#';
grant all on advisor_db.* to 'advisoradmin'@'%' identified by 'advisoradmin@123#';
use advisor_db;
