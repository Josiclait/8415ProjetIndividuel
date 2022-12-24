#!/bin/bash

sudo apt-get update
sudo apt-get install \
        mysql-server \
        sysbench \
        -y

wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvf sakila-db.tar.gz

sudo mysql -u root -f ~/sakila-db/sakila-schema.sql
sudo mysql -u root -f ~/sakila-db/sakila-data.sql