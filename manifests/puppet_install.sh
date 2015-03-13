#!/bin/bash
# install script for puppet on clean vagrant box
# copied from:
#     https://docs.puppetlabs.com/guides/install_puppet/install_debian_ubuntu.html
wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb
sudo dpkg -i puppetlabs-release-precise.deb
sudo apt-get -y update
sudo apt-get -y install puppet

# create /etc/puppet/modules directory
sudo mkdir --parents /etc/puppet/modules

# install some puppet modules
sudo puppet module install stankevich-python

# requirements for numpy
sudo apt-get -y install build-essential python-dev
