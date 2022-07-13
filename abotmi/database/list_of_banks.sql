use uplife_db;
DELETE FROM datacenter_listofbanks;
ALTER TABLE datacenter_listofbanks AUTO_INCREMENT = 1;
-- load data local infile '/home/kantanand/projects/NF/database/list_of_banks.csv' into table  datacenter_listofbanks fields terminated by '|' enclosed by '"' lines terminated by '\n' (bank,ifsc,micr,branch,address,contact,city,district,state);
load data local infile '/home/northfacing/database/list_of_banks.csv' into table  datacenter_listofbanks fields terminated by '|' enclosed by '"' lines terminated by '\n' (bank,ifsc,micr,branch,address,contact,city,district,state);