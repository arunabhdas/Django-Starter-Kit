from __future__ import with_statement
import time
from fabric.api import env, require, run, local, put, cd, settings as fabric_settings
from fabric.contrib.console import confirm


def stage():
    '''
    Environment settings for stage.

    Usage:
         fab stage <task>
    '''
    env.name = 'live'
    env.project_root = '~/webapps/app/' % env
    env.hosts = ['']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv_root = '/home/%(user)s/venvs/app/' % env
    env.venv = 'source /home/%(user)s/venvs/app/bin/activate && ' % env
    env.gunicorn_app = 'tmai'
    env.gunicorn_log = 'app.log'
    env.nginx_conf = 'app.nginx.conf'

def live():
    '''
    Environment settings for live.

    Usage:
         fab live <task>
    '''
    yes = confirm("Are you sure you want to use LIVE and not stage?", default=False)
    if not yes:
        sys.exit()
    env.name = 'live'
    env.project_root = '~/webapps/app/' % env
    env.hosts = ['']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv_root = '/home/%(user)s/venvs/app/'  % env
    env.venv = 'source /home/%(user)s/venvs/app/bin/activate && ' % env
    env.gunicorn_app = 'tmai'
    env.gunicorn_log = 'app.log'
    env.nginx_conf = 'app.nginx.conf'


def deploy():
    '''
    Usage:

    $>fab <env name> deploy
    '''
    require('name')
    git_pull()
    setup_dirs()
    local_settings()
    collect_static()
    install_requirements()
    syncdb_migrate()
    nginx_restart()

def local_settings():
    with cd(env.project_root):
        run('%(venv)s cp conf/%(name)s/local_settings.py .' % env)

def collect_static():
    with cd(env.project_root):
        run('%(venv)s python manage.py collectstatic -v0 --noinput' % env)

def setup_dirs():
    with fabric_settings(warn_only=True):
        with cd(env.project_root):
            run("mkdir static" % env)
            run("mkdir media" % env)

        # CSS compress
        with cd(env.project_root):
            run("mkdir static/CACHE" % env)
            run("chmod 777 static/CACHE" % env)

        # logs
        run("touch /tmp/%(gunicorn_log)s" % env)
        run("chmod 777 /tmp/%(gunicorn_log)s" % env)

def git_reset(do_reset=True):
    do_reset = confirm("Are you sure you want to reset?", default=False)
    if do_reset:
        with cd(env.project_root):
                run('git reset --hard' % env)

def git_pull():
    with cd(env.project_root):
        run('git fetch;' % env)
        run('git checkout %(branch)s; git pull origin %(branch)s;' % env)

def clean():
    """Clear out extraneous files, like pyc/pyo"""
    with cd(env.project_root):
        run("""find -type f -name "*.py[co]" -delete""")

def syncdb_migrate():
    with cd(env.project_root):
        run('%(venv)s python manage.py syncdb' % env)
        run('%(venv)s python manage.py migrate' % env)

def gunicorn_restart():
    "Restart the web server"
    run("sudo supervisorctl restart %(gunicorn_app)s" % env)

def apache_conf():
    run("sudo cp ~/webapps/%(name)s/conf/%(name)s/%(name)s.apache.conf /etc/apache2/sites-available/." % env)
    run("sudo a2dissite %(name)s.apache.conf" % env)
    run("sudo a2ensite %(name)s.apache.conf" % env)

def apache_restart():
    "Restart the web server"
    run("sudo apache2ctl graceful")

def nginx_conf():
    "Restart the web server"
    with cd(env.project_root):
        run("sudo cp conf/%(name)s/%(nginx_conf)s /etc/nginx/sites-available/." % env)
        with fabric_settings(warn_only=True):
            run("sudo ln -s /etc/nginx/sites-available/%(nginx_conf)s /etc/nginx/sites-enabled/%(nginx_conf)s" % env)

def nginx_restart():
    "Restart the web server"
    run("sudo /etc/init.d/nginx restart")

# -------------
# Server Setup
# -------------
def install_externals():
    """
    For things that need to be installed via apt-get.
    These are installed before requirements.txt in the venv otherwise some python modules won't install properly
    """
    run('sudo apt-get update')
    run("sudo apt-get install mysql-server mysql-client locate python-setuptools git-core subversion mercurial htop screen byobu apache2.2-common gcc")
    run('sudo apt-get install python2.6-dev')
    run('sudo apt-get install libmysqlclient-dev')
    run('sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev python-pycurl-dbg libcurl4-openssl-dev')
    run('sudo apt-get install libxml2-dev libxslt-dev')

def install_requirements():
    with cd(env.project_root):
        run('%(venv)s pip install -r requirements.txt' % env)


# Shortcuts
#-----------
def push2stage():
    local('git pull origin master', capture=False)
    local('git push origin master', capture=False)
    local('fab stage deploy', capture=False)

def push2live():
    local('git pull origin master', capture=False)
    local('git push origin master', capture=False)
    local('fab live deploy', capture=False)

try:
    from local_fabfile import *
except:
    pass

