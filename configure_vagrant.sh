#!/usr/bin/env bash

apt-get update
apt-get -y install build-essential python-dev python-pip python-numpy python-scipy nodejs npm coffeescript

ln -s /usr/bin/nodejs /usr/bin/node

pip install -r /vagrant/requirements.txt

npm -g install cake
