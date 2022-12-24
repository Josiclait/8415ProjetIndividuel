#!/bin/bash
# From https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04

sudo apt update
sudo apt install \
    git \
    libaio1 \
    libclass-methodmaker-perl \
    libmecab2 \
    -y

cd /home/ubuntu
git clone https://github.com/Josiclait/8415ProjetIndividuel.git

wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

sudo cp /home/ubuntu/8415ProjetIndividuel/my.cnf /etc/
mkdir -p /usr/local/mysql/data
sudo cp /home/ubuntu/8415ProjetIndividuel/ndbd.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable ndbd
sudo systemctl start ndbd