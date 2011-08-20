Starting out from a fresh server
================================
These are steps i did to install the app on the server and some basic sysadmin stuff. This guide is applicable to Ubuntu Maverick, with python 2.6. Minimal changes would be required for higher versions.

Setting up User
---------------

# Log on as ROOT to the server and create
# an ubuntu user which will run our app
    sudo useradd -d /home/ubuntu -m ubuntu -s /bin/bash
    mkdir /home/ubuntu/.ssh/
    touch /home/ubuntu/.ssh/authorized_keys
    chown ubuntu /home/ubuntu/.ssh/authorized_keys 
    chgrp ubuntu /home/ubuntu/.ssh/authorized_keys 
    chown ubuntu /home/ubuntu/.ssh/
    chgrp ubuntu /home/ubuntu/.ssh/

# Added my key to /home/ubuntu/.ssh/authorized_keys

# Add Ubuntu to sudoers
    sudo visudo 
    
#Paste the following at the end.
#ubuntu  ALL=(ALL) NOPASSWD:ALL


Installing required tools
--------------------------
# Log on as ubuntu user
ssh-keygen -C <ubuntu@server_ip>
sudo apt-get update
sudo apt-get upgrade

$>sudo apt-get install mysql-server mysql-client locate python-setuptools git-core subversion mercurial htop screen byobu nginx
# Replace nginx by apache2.2-common if needed
# set passwd for mysql user root

# External requirements for making it easier to install modules like mysql + PIL inside virtualenv
$sudo apt-get install python2.6-dev libmysqlclient-dev libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev python-pycurl-dbg libcurl4-openssl-dev libxml2-dev libxslt-dev libapache2-mod-wsgi -y

Change default SSH Port
-----------------------
# change to "Port XXXX"
    nano /etc/ssh/sshd_config
    /etc/init.d/ssh restart


virtualenv/virtualenvwrapper
-----------------------------
    sudo easy_install pip
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    
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

Create the directory to hold virtual environments and then load virtualenv.
    mkdir ~/venvs
    source ~/.bashrc
    mkvirtualenv --no-site-packages stage 

From this point you can always use the ``workon`` command to start a virtual environment
Here stage is the name we gave our virtualenv. For more info goto - http://www.doughellmann.com/docs/virtualenvwrapper/

    workon stage

Django
-------
    workon stage

    mkdir ~/webapps/
    cd ~/webapps/
    git clone <repo_url> # assuming the dir name created is ``stage``. If not then rename it to something appropriate
    cd stage
    pip install -r requirements.txt

Supervisord
-----------
    sudo pip install supervisor 
    sudo echo_supervisord_conf > /etc/supervisord.conf   # as root

    
    sudo nano /etc/supervisord.conf
    
Add this at the bottom of the file
    [program:app]
    command=/home/ubuntu/venvs/app/bin/python /home/ubuntu/webapps/app/manage.py run_gunicorn -b 0.0.0.0:8000 --log-file=/tmp/gunicorn.log
    directory=/home/ubuntu/webapps/app/
    user=www-data
    autostart=true
    autorestart=true
    stdout_logfile=/tmp/supervisord.log
    redirect_stderr=true


Install supervisord to upstart

    sudo nano /etc/init.d/supervisord 

and add the following to the file 

    # Supervisord auto-start
    #
    # description: Auto-starts supervisord
    # processname: supervisord
    # pidfile: /var/run/supervisord.pid

    SUPERVISORD=/usr/local/bin/supervisord
    SUPERVISORCTL=/usr/local/bin/supervisorctl

    case $1 in
    start)
            echo -n "Starting supervisord: "
            $SUPERVISORD
            echo
            ;;
    stop)
            echo -n "Stopping supervisord: "
            $SUPERVISORCTL shutdown
            echo
            ;;
    restart)
            echo -n "Stopping supervisord: "
            $SUPERVISORCTL shutdown
            echo
            echo -n "Starting supervisord: "
            $SUPERVISORD
            echo
            ;;
    esac


Then run these 

    sudo chmod +x /etc/init.d/supervisord
    sudo update-rc.d supervisord defaults
    sudo /etc/init.d/supervisord start
    
    sudo supervisorctl status

After any edits to the supervisord.conv, you should restart it

    sudo /etc/init.d/supervisord restart
    
    
    
nginx
---------------
Remove default app
    sudo rm /etc/nginx/sites-enabled/000-default
    
Create new nginx config for the site

    sudo touch /etc/nginx/sites-available/<app>
    
Copy the following to the file /etc/nginx/sites-available/<app>
    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }

Enable it using 
    sudo ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/<app>


Local
======
*   On local you need to install pip, virtualenv, virtualenvwrapper. Only pip is a necessity here.

    easy_install pip
    pip install fabric
    pip install virtualenv
    pip install virtualenvwrapper


*   Install requirements
    
    cd <project_dir>
    pip install -r requirements.txt
    
*   Add a local_settings.py file in <project_dir>/settings/
    A sample is in settings/stage
    Add your DB settings
    python manage.py syncdb
    python manage.py runserver
    

Sources
--------
* http://brandonkonkle.com/blog/2010/jun/25/provisioning-new-ubuntu-server-django/
* http://supervisord.org/installing.html
