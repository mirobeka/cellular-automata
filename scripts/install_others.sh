#!/bin/bash

# create /etc/puppet/modules directory if necessary
sudo mkdir -p /etc/puppet/modules

# install some puppet modules
sudo puppet module install stankevich-python
sudo puppet module install puppetlabs-nodejs

# install curl
sudo apt-get -y install curl
