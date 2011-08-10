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
    env.name = 'stage'
    env.project_root = '~/webapps/%(name)s/' % env
    env.hosts = ['']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv = 'source /home/%(user)s/venvs/%(name)s/bin/activate && ' % env
    
    
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
    env.project_root = '~/webapps/%(name)s/' % env
    env.hosts = ['']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv = 'source /home/%(user)s/venvs/%(name)s/bin/activate && ' % env
    
    
def deploy():
    '''
    Usage: 
    
    $>fab <env name> deploy
    '''
    require('name')
    git_pull()
    setup_dirs()
    local_settings()
    install_requirements()
    syncdb_migrate()
    apache_restart()

def local_settings():
    with cd(env.project_root):
        run('%(venv)s cp conf/%(name)s/local_settings.py .' % env)
        
def setup_dirs():
    with fabric_settings(warn_only=True):
        # Admin media, for Apache
        run("ln -s /home/%(user)s/venvs/%(name)s/lib/python2.6/site-packages/django/contrib/admin/media/ /home/%(user)s/webapps/%(name)s/media/admin-media" % env)
        
        # CSS compress
        with cd(env.project_root):
            run("sudo mkdir media/CACHE" % env)
            run("sudo chmod 777 media/CACHE" % env)
        
def apache_conf():
    run("sudo cp ~/webapps/%(name)s/conf/%(name)s/%(name)s.apache.conf /etc/apache2/sites-available/." % env)
    run("sudo a2dissite %(name)s.apache.conf" % env)
    run("sudo a2ensite %(name)s.apache.conf" % env)
    
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
    
def apache_restart():
    "Restart the web server"
    run("sudo apache2ctl graceful")
    
# -------------
# Server Setup
# -------------
def install_externals():
    """
    For things that need to be installed via apt-get. 
    These are installed before requirements.txt in the venv otherwise some python modules won't install properly
    """
    run('sudo apt-get update')
    run("sudo apt-get install mysql-server mysql-client locate python-setuptools git-core subversion mercurial htop screen byobu apache2.2-common gcc -y")
    run('sudo apt-get install python2.6-dev -y')
    run('sudo apt-get install libmysqlclient-dev -y')
    run('sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev python-pycurl-dbg libcurl4-openssl-dev -y')
    run('sudo apt-get install libxml2-dev libxslt-dev -y')

def install_requirements():
    with cd(env.project_root):
        run('%(venv)s pip install -r requirements.txt' % env)
        
def setup_server():
    install_externals()
    # Todo: create virtualenv.
    install_requirements()


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
    
