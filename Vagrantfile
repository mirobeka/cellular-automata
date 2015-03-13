# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # use default box
  config.vm.box = "hashicorp/precise32"

  # forward port guest machine:5000 -> host machine:5000
  # port 5000 is default for flask web app
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # execute apt-get update
  config.vm.provision :shell do |shell|
    shell.path = "./manifests/puppet_install.sh"
  end

  # Enable provisioning with Puppet stand alone.  Puppet manifests
  # are contained in a directory path relative to this Vagrantfile.
  config.vm.provision "puppet" do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file  = "ca_server_config.pp"
  end

end
