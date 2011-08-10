WebbyNode
==========
These are steps i did to install the app on the server and some basic sysadmin stuff.

Setting up User
---------------

# Log on as ROOT to the server and create
# an ubuntu user which will run our app
$>sudo useradd -d /home/ubuntu -m ubuntu
$>chsh ubuntu -s /bin/bash
$>mkdir /home/ubuntu/.ssh/
$>touch /home/ubuntu/.ssh/authorized_keys
$>chown ubuntu /home/ubuntu/.ssh/authorized_keys 
$>chgrp ubuntu /home/ubuntu/.ssh/authorized_keys 
$>chown ubuntu /home/ubuntu/.ssh/
$>chgrp ubuntu /home/ubuntu/.ssh/

# Added my key to auth keys.

# Add Ubuntu to sudoers
$>sudo visudo 
#Paste the following at the end.
#ubuntu  ALL=(ALL) NOPASSWD:ALL


Installing required tools
--------------------------
# Log on as ubuntu user
#$>ssh-keygen -C <ubuntu@server_ip>
$>sudo apt-get update
$>sudo apt-get upgrade

$>sudo apt-get install mysql-server mysql-client locate python-setuptools git-core subversion mercurial htop screen byobu apache2.2-common
# set passwd for mysql user root

# External requirements for making it easier to install modules like mysql + PIL inside virtualenv
$sudo apt-get install python2.6-dev libmysqlclient-dev libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev python-pycurl-dbg libcurl4-openssl-dev libxml2-dev libxslt-dev libapache2-mod-wsgi -y

Setting up virtualenv
----------------------
$>sudo easy_install pip
$>sudo pip install virtualenv

$>sudo pip install virtualenvwrapper
Note where it installs virtualenvwrapper.sh 
The installation script says something like ----> changing mode of /usr/bin/virtualenvwrapper.sh to 755

Copy these lines at the top of ~/.bashrc
The above lines should appear above [ -z "$PS1" ] && return

# ---------------------------------------------
# virtualenvwrapper
export WORKON_HOME=~/venvs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUALENV_BASE=$WORKON_HOME
export PIP_RESPECT_VIRTUALENV=true
# ---------------------------------------------

$>mkdir ~/venvs
$>source ~/.bashrc
$>mkvirtualenv --no-site-packages stage 

From this point you can always use the ``workon`` command to start a virtual environment
Here stage is the name we gave our virtualenv. For more info goto - http://www.doughellmann.com/docs/virtualenvwrapper/

$>workon stage

Setting up django app
---------------------------------------------
$>workon stage

$>mkdir ~/webapps/
$>cd ~/webapps/
$>git clone <repo_url> # assuming the dir name created is ``stage``. If not then rename it.
$>cd stage
$>pip install -r requirements.txt

Then on local machine you can install/run fabric script
$>pip install fabric
$>workon stage
$>cd <project_dir>
$>fab stage runserver

Setting up nginx
---------------
- add nginx conf to /etc/nginx/sites-available/stage
- enable it using
$>sudo ln -s /etc/nginx/sites-available/stage /etc/nginx/sites-enabled/stage


Local
======
*   On local you need to install pip, virtualenv, virtualenvwrapper. Only pip is a necessity here.

    $> easy_install pip
    $> pip install virtualenv
    $> pip install virtualenvwrapper


*   Install requirements
    
    $>cd <project_dir>
    $>pip install -r requirements.txt
    
*   Add a local_settings.py file in <project_dir>/settings/
    A sample is in settings/stage
    Add your DB settings
    $>python manage.py syncdb
    $>python manage.py runserver
    
