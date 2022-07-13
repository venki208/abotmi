use uplife_db;
DELETE FROM datacenter_indiapincode;
ALTER TABLE datacenter_indiapincode AUTO_INCREMENT = 1;
-- load data local infile '/home/kantanand/projects/NF/database/pin_code_master.csv' into table  datacenter_indiapincode fields terminated by ',' enclosed by '"' lines terminated by '\n' (pin_code,district_name,state_name);
load data local infile '/home/northfacing/database/pin_code_master.csv' into table  datacenter_indiapincode fields terminated by ',' enclosed by '"' lines terminated by '\n' (pin_code,district_name,state_name);
