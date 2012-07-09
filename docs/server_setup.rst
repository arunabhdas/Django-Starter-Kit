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

    ubuntu  ALL=(ALL) NOPASSWD:ALL


Installing required tools
--------------------------
# Log on as ubuntu user

    ssh-keygen -C <ubuntu@server_ip>
    sudo apt-get update
    sudo apt-get upgrade


# External requirements for making it easier to install modules like mysql + PIL inside virtualenv
# set passwd for mysql user root

    yes| sudo apt-get install mysql-server mysql-client locate python-setuptools python-pip git-core subversion mercurial htop screen byobu memcached

    yes| sudo apt-get install python-dev libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libxml2-dev libxslt-dev libmysqlclient-dev # for lxml, pil, mysql
    yes| sudo apt-get install python-pycurl-dbg libcurl4-openssl-dev librtmp-dev libcurl3-gnutls-dev # for pycurl
    yes| sudo apt-get install libapache2-mod-wsgi

# Replace nginx by apache2.2-common if needed

    sudo apt-get install nginx


Misc conf
-----------------------

# Install python-based intrusion prevention software

    sudo apt-get install fail2ban


# change default ssh port to "Port XXXX"

    sudo nano /etc/ssh/sshd_config
    sudo /etc/init.d/ssh restart


virtualenv/virtualenvwrapper
-----------------------------

    sudo easy_install pip
    sudo pip install virtualenv virtualenvwrapper

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
    sudo touch /etc/supervisord.conf             # as root

    or you can also create a sample file using
    #sudo echo_supervisord_conf > /etc/supervisord.conf   # as root

Configure supervisor to watch our app.
    sudo nano /etc/supervisord.conf

Remove all content from /etc/supervisord.conf and replace with the following text. Also replace mentions of <app>, and virtualenv names below.
    [unix_http_server]
    file=/tmp/supervisor.sock   ; (the path to the socket file)

    [supervisord]
    logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
    logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
    logfile_backups=10          ; (num of main logfile rotation backups;default 10)
    loglevel=info               ; (log level;default info; others: debug,warn,trace)
    pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
    nodaemon=false              ; (start in foreground if true;default false)
    minfds=1024                 ; (min. avail startup file descriptors;default 1024)
    minprocs=200                ; (min. avail process descriptors;default 200)

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

    [program:app]
    command=/home/ubuntu/venvs/venv_name/bin/python /home/ubuntu/webapps/app/manage.py run_gunicorn -b 127.0.0.1:8000 --log-file=/tmp/app_gunicorn.log
    directory=/home/ubuntu/webapps/app/
    user=www-data
    autostart=true
    autorestart=true
    stdout_logfile=/tmp/app_supervisord.log
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

After any edits to the supervisord.conf, you should restart it

    sudo /etc/init.d/supervisord restart


Now you should be able to start/stop your app:

    sudo supervisorctl restart app

nginx
---------------
Remove default app
    sudo rm /etc/nginx/sites-enabled/000-default

Create new nginx config for the site

    sudo touch /etc/nginx/sites-available/<app>

Copy the following to the file /etc/nginx/sites-available/<app>

    server {
        listen 80;
        client_max_body_size 4G;
        server_name example.cloudshuffle.com;

        keepalive_timeout 5;

        location /static/admin {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location /static/ {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location /media/ {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:8000;

            #gzip on;
            #gzip_types       text/plain application/xml text/xml;
            #gzip_proxied any;
        }

        #error_page 500 502 503 504 /500.html;
        #location = /500.html {
        #    root /path/to/app/current/public;
        #}
    }

Enable it using
    sudo ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/<app>

For this project, you can find the nginx config file under conf/<env>/*.nginx.conf


Solr-Tomcat
===========

    sudo apt-get install solr-tomcat


Local
======
*   On local you need to install pip, virtualenv, virtualenvwrapper. Only pip is a necessity here.

    easy_install pip
    pip install fabric
    pip install virtualenv
    pip install virtualenvwrapper

*   Create your virtualenv as described above.

    workon <env>

*   Install requirements

    cd <project_dir>
    pip install -r requirements.txt

*   Add a local_settings.py file in <project_dir>/
    A sample is in settings/stage
    Add your DB settings
    python manage.py syncdb
    python manage.py migrate
    python manage.py check_permissions
    python manage.py runserver



Sources
--------
* http://brandonkonkle.com/blog/2010/jun/25/provisioning-new-ubuntu-server-django/
* http://supervisord.org/installing.html
* http://bluebream.zope.org/doc/1.0/manual/deployment.html
