            ____     _ _       _            
           / ___|___| | |_   _| | __ _ _ __ 
          | |   / _ \ | | | | | |/ _` | '__|
          | |__|  __/ | | |_| | | (_| | |   
           \____\___|_|_|\__,_|_|\__,_|_|   

                    _         _                        _        
                   / \  _   _| |_ ___  _ __ ___   __ _| |_ __ _ 
                  / _ \| | | | __/ _ \| '_ ` _ \ / _` | __/ _` |
                 / ___ \ |_| | || (_) | | | | | | (_| | || (_| |
                /_/   \_\__,_|\__\___/|_| |_| |_|\__,_|\__\__,_|


#Cellular Automata
This project contains 2 main parts:

 -> Web application / UI
 -> Cellular Automata framework

Unfortunately, this project contains an awfull lot of bad practices in programming.
It was my first "big" project and I made several bad choices in implementing
various parts. After discovering this mistakes, there was no time to refactor
whole project, because of deadline of my thesis.

#Requirements
for developments I recommend to use vagrant. In script `configure_vagrant.sh`
is defined requirements that must be installed on dev machine.

##OS
I recommend to use [Ubuntu 14.04 Trusty Tahr 64bit](http://releases.ubuntu.com/14.04/)

##Python
Main programming language is python. I used python 2.7, other versions were not tested.

    sudo apt-get update
    sudo apt-get install python2.7

Later we will need to install numpy / scipy which needs build essential

    sudo apt-get install build-essential python-dev python-pip

For sake of simplicity, we install numpy and scipy with `aptitude`

    sudo apt-get install python-numpy python-scipy

And at the end, we'll install other dependencies with `requirements.txt` file.

    sudo pip install -r requirements.txt

##Coffeescript
Web UI of this project contains coffeescript on client side, so we need install requirements
for that
    
    sudo apt-get install nodejs npm coffeescript

Ubuntu has other package that is called node, so we need to make quick fix

    sudo ln -s /usr/bin/nodejs /usr/bin/node

To support autocompile of coffeescript files after change in files, we need to have cake installed.
It's required by `flask-cake`

    sudo npm -g install cake


#Vagrant
Vagrant makes initial set up of development environment breeze. Just install
[vagrant](http://www.vagrantup.com/downloads.html) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads),
in root project dir execute

    vagrant up

Wait until configuration finish and log in to virtual machine

    vagrant ssh

Now you are logged in as user `vagrant` with password `vagrant`

Any changes on host filest (all project files and sub-dirs) are propagated to guest (virtual machine) and
the other way. Changes on guest are propagated on host.

Content of root directory is located on guest in `/vagrant`.

#How to start Web UI
Web Interface for Cellular Automata (wica) is in `wica` directory. Web app is made
in microframework [Flask](http://flask.pocoo.org/). To start web app, execute following

    python wica/growing_ca.py

or

    ./run_server.sh

It is important that web app is executed form project root directory. Otherwise web app
would not load other required modules.

After flask starts is web server, open `localhost:5000`

##Issues
Sice this is unfinished project, there are several issues in UI to be aware of:
+ Only functional tab is `projects` tab
+ Do not use Project settings editor, edit project configuration by hand
+ Evolving weights does not work from web. You should use script `evolve.py` for that
+ Recording "replay" doesn't show any progress on web. You should check messages in terminal where flask app is printing stdout

#Cellular Automata project
In directory `/data/` are several example projects. Every project has following structure

    twobands45
    |-- patterns
    |   `-- twobands45.ptn
    |-- replays
    |   `-- 2015_03_30_20_48_01.replay
    |-- weights
    |   `-- Mon_Mar_30_20:51:35_2015.wgh
    `-- project.cfg

`project.cfg` contains configuration of project. Which evolve strategy to use, what are inital
neural network weights, dimensions of grid, neighbourhood, etc.

`patterns` contains shape data. This data is used to compare to evolved CA.
First row has space separated values. Example:

    400 400 20 grayscale

`400` and `400` are width and height. `20` is resolution of grid. (400/20=20 cells in width and 20 cells in height).
grayscale defines that cells has simple grayscale value as a state.

Rest of file is executed as python code, which returns list of state values for each cell. This is
used to create a mock lattice which is compared to the evolved one.

`replays` are picked data of python multidimensional array containing progress of CA. There can be viewed in
web ui in _replays_ tab.

`weights` are generated files containing information about evolved weights. Best way to examine this data is
in _weights_ tab.


TODO: create example project.cfg + description of options

#How to evolve cellular automata
In project root is `evolve.py` script. Executing script without parameters will show help:

    usage: evolve.py [-h] -p PROJECT
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PROJECT, --project PROJECT
                            Project path

So to evolve new weights for my configuration, I would execute

    python evolve.py -p data/twobands45

Now you can keep the evolution running as long as you wish.

If you want to check data on the fly, open actual `weights` file and examine data.

You can safely terminate evolution with `ctrl-c` shortcut. All data will be saved in `weights` file
before termination.

#How to create replays
To create replay for visual examination of progress of CA, go to _weights_ tab and select weights which
should be used. Copy weights and paste into project configuration file, in section *replay*, option *weights*.
Next, open _replay_ tab and press *record replay* button. There is no visual feedback if operation was successfull,
but you can check output in terminal. When creating of replay is done, there will be message:

    08:48:56 PM - [THREAD.INFO] Runngin finished! Replay saved in data/twobands45/replays/2015_03_30_20_48_01.replay
    
After this, refresh web page and click on recorded replay. Data will be loaded and you can visually examine progress
of CA

