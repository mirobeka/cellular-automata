# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # use default box
  config.vm.box = "ubuntu/trusty64"

  # forward port guest machine:5000 -> host machine:5000
  # port 5000 is default for flask web app
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # execute apt-get update
  config.vm.provision :shell, :path => "scripts/install_puppet.sh"
  config.vm.provision :shell, :path => "scripts/install_others.sh"
  
# provision with Puppet stand alone
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file = "default.pp"
  end
end
