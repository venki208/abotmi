#! /bin/bash
echo "::::: Load Indian PinCodes to DB :::::"
echo -n "Please Enter your Mysql Root username $"
# Read Username
read -s username
echo

echo -n "Please Enter your MySQL Root Password $"
# Read Password
read -s passwd
echo

echo "--> Inserting Indian Pincode Records ... if not happened check path in pincodes.sql"
mysql --local-infile -p$passwd -u$username < pincodes.sql

echo "--> NFDB is Ready to use ."

