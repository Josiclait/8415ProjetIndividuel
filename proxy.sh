#!/bin/bash

sudo apt-get update
sudo apt-get install \
    python3-venv \
    -y

cd /home/ubuntu
git clone https://github.com/Josiclait/8415ProjetIndividuel.git

nano vockey.pem
# TODO: Add the content of the private key from AWS modules details
sudo chmod 400 /home/ubuntu/8415ProjetIndividuel/vockey.pem

cd /home/ubuntu/8415ProjetIndividuel
python3 -m venv virtualEnvironment
source virtualEnvironment/bin/activate
pip install -r requirement.txt

sudo cp /home/ubuntu/8415ProjetIndividuel/proxy.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl start proxy
sudo systemctl enable proxy

sudo systemctl start nginx
sudo systemctl enable nginx

sudo cp /home/ubuntu/LOG8415E/default /etc/nginx/sites-available

sudo systemctl restart proxy
sudo systemctl restart nginx