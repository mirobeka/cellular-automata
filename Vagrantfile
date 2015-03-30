# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # use default box
  config.vm.box = "ubuntu/trusty64"

  # forward port guest machine:5000 -> host machine:5000
  # port 5000 is default for flask web app
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # install & configure required software
  config.vm.provision :shell, :path => "configure_vagrant.sh"
end
