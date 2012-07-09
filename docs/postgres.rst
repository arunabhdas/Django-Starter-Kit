Postgres
-----------------------
Run the following script to install a clean Postgres 9.1 install with PostGIS template

    #!/bin/bash
    #
    # Install Postgres 9.1, PostGIS and create PostGIS template on a clean Ubuntu 11.10 Oneiric Ocelot box
    # http://wildfish.com
    sudo apt-get -y install python-software-properties
    sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
    sudo apt-get update

    sudo apt-get -y install postgis postgresql-9.1 postgresql-server-dev-9.1 postgresql-contrib-9.1 postgis  gdal-bin binutils libgeos-3.2.2 libgeos-c1 libgeos-dev libgdal1-dev libxml2 libxml2-dev libxml2-dev checkinstall proj libpq-dev

    sudo mkdir -p '/usr/share/postgresql/9.1/contrib/postgis-1.5'

    # fetch, compile and install PostGIS
    wget http://postgis.refractions.net/download/postgis-1.5.3.tar.gz
    tar zxvf postgis-1.5.3.tar.gz && cd postgis-1.5.3/
    sudo ./configure && sudo make && sudo checkinstall --pkgname postgis-1.5.3 --pkgversion 1.5.3-src --default

    # now create the template_postgis database template
    sudo su postgres -c'createdb -E UTF8 -U postgres template_postgis'
    sudo su postgres -c'createlang -d template_postgis plpgsql;'
    sudo su postgres -c'psql -U postgres -d template_postgis -c"CREATE EXTENSION hstore;"'
    sudo su postgres -c'psql -U postgres -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql'
    sudo su postgres -c'psql -U postgres -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql'
    sudo su postgres -c'psql -U postgres -d template_postgis -c"select postgis_lib_version();"'
    sudo su postgres -c'psql -U postgres -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"'
    sudo su postgres -c'psql -U postgres -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"'
    sudo su postgres -c'psql -U postgres -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"'
    echo "Done"

    sudo su - postgres
    createuser --createdb dummy
    # create new db dummy, which will contain our application schema.
    createdb -T template_postgis dummy

GUI tools, not needed on server

    $>sudo apt-get install pgadmin3

Configure default postgres user

    $>sudo -u postgres psql template1
    postgres# ALTER USER postgres with encrypted password 'postgres';
    postgres# \q

Create a postgres user for the current linux user i.e. 'ubuntu'. We'll set its password
and also create a default database by the same name.
You can replace ubuntu, or whatever user you're using.

    $>sudo -u postgres createuser --superuser ubuntu
    $>sudo -u postgres psql
    postgres=# \password ubuntu
    Enter new password: ubuntu
    Enter it again: ubuntu

    postgres=# create database ubuntu ENCODING 'UTF8';
    postgres=# \q

You can now just type in $>psql and it will automatically login to postgres using user 'ubuntu' and database of the same name 'ubuntu'.
You can switch database by typing $>psql template1

Finally we'll create an dummy  database and user

    $> sudo -u postgres createuser -P dummy
    could not change directory to "/home/sid/Projects/dummy"
    Enter password for new role:
    Enter it again:
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

Now let's create a DB(named 'dummy') for the project and set the owner the role 'dummy'
    $>psql
    ubuntu=# CREATE DATABASE dummy OWNER dummy ENCODING 'UTF8';

Next step is to make sure we're using md5 authentication for our 'dummy' role.

    sudo nano /etc/postgresql/8.4/main/pg_hba.conf

Add the line for dummy below the default user. Eg.

    local   all         postgres                          ident
    local   all         dummy                               md5

    $> sudo service postgresql restart

Now you should be able to syncdb with the database/username/password.


External requirements for making it easier to install modules like mysql + PIL inside virtualenv

    $>sudo apt-get install python2.6-dev libmysqlclient-dev libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev python-pycurl-dbg libcurl4-openssl-dev libxml2-dev libxslt-dev libapache2-mod-wsgi
