use nfdb;
DELETE FROM datacenter_india_pincode;
ALTER TABLE datacenter_india_pincode AUTO_INCREMENT = 1;
-- load data local infile '/home/kantanand/projects/NF/database/pin_code_master.csv' into table  datacenter_india_pincode fields terminated by ',' enclosed by '"' lines terminated by '\n' (pin_code,district_name,state_name);
load data local infile '/home/northfacing/database/pin_code_master.csv' into table  datacenter_india_pincode fields terminated by ',' enclosed by '"' lines terminated by '\n' (pin_code,district_name,state_name);
