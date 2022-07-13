drop database if exists abotmi_db;
create database abotmi_db CHARACTER SET utf8 COLLATE utf8_general_ci;
grant all on abotmi_db.* to 'nfadmin'@'localhost' identified by 'nfadmin@123#';
-- Remote Login uncomment to Enable
grant all on abotmi_db.* to 'nfadmin'@'%' identified by 'nfadmin@123#';
use abotmi_db;

