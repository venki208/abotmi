from fabric.api import task, env, cd, run, sudo, shell_env, local
from fabric.tasks import execute
from fabric.contrib import files
from fabric.contrib.project import rsync_project
from fabric.contrib.files import sed, append


def get_host():
    hosts = env.hosts
    host_user = hosts[0].split("@")[0]
    host_name = hosts[0].split('@')[-1]
    return host_user, host_name


def get_settings_filename():
    host_user, host_name = get_host()
    conf_file = ''
    if host_name in ['dev.abotmi.com', 'dev2.abotmi.com']:
        conf_file = 'settings.dev'
    elif host_name in ['test.abotmi.com']:
        conf_file = 'settings.test'
    elif host_name in ['abotmi.com']:
        conf_file = 'settings.production'
    elif host_name == 'stg.abotmi.com':
        conf_file = 'settings.staging'
    return conf_file


def get_config_filename():
    host_user, host_name = get_host()
    conf_file = ''
    if host_name in ['dev.abotmi.com', 'dev2.abotmi.com']:
        conf_file = 'dev_config.json'
    elif host_name in ['test.abotmi.com']:
        conf_file = 'test_config.json'
    elif host_name == 'abotmi.com':
        conf_file = 'prod_config.json'
    elif host_name == 'stg.abotmi.com':
        conf_file = 'stag_config.json'
    return conf_file


@task
def change_permisson():
    '''
    Changes the file/folder permisson to local users name
    '''
    print "*********** Changin permisson **************"
    host_user, host_name = get_host()
    run('sudo chown -R %s:%s /home/abotmi/env' % (host_user, host_user))
    run('sudo chown -R %s:%s /home/abotmi/abotmi' % (host_user, host_user))
    run('sudo chown -R %s:%s /home/abotmi/static' % (host_user, host_user))


@task
def restore_permission():
    '''
    Restoring the Permissons
    '''
    run('sudo chown -R %s:%s /home/abotmi/env' % ('abotmi', 'abotmi'))
    run('sudo chown -R %s:%s /home/abotmi/abotmi' % ('abotmi', 'abotmi'))
    run('sudo chown -R %s:%s /home/abotmi/static' % ('abotmi', 'abotmi'))


@task
def check_and_create_environment():
    '''
    Checks environment is present or not and creates it
    '''
    if not files.exists('/home/abotmi/env'):
        print "*********** environment is not exists. setting up Environment ***********"
        with cd('/home/abotmi/'):
            run('sudo virtualenv env')


@task
def check_and_create_logs_directory():
    '''
    Checks Log directory is there or not and creates it
    '''
    if not files.exists('/home/abotmi/abotmi/logs'):
        print "************ logs folder is not exists. creating Logs directory **********"
        with cd('/home/abotmi/abotmi/'):
            run('sudo mkdir logs')


@task
def check_and_create_project_directory():
    '''
    Checks project directory is there or not and creates it
    '''
    if not files.exists('/home/abotmi/abotmi'):
        print "*********** creating project directory******************"
        with cd('/home/abotmi/'):
            run('sudo mkdir abotmi')

    if not files.exists('/home/abotmi/static'):
        print "********** creating static directory  ********************"
        with cd('/home/abotmi/'):
            run('sudo mkdir static')


@task
def install_requirements():
    '''
    installing requirements
    '''
    print "********** installing requirements ************"
    run(
        '/home/abotmi/env/bin/pip install -r \
        /home/abotmi/abotmi/requirements_production.txt')


@task
def start_uwsgi():
    '''
    Starts the uWsgi server
    '''
    run('sudo service abotmi start')


@task
def stop_uwsgi():
    '''
    Stops the uWsgi server
    '''
    run('sudo service abotmi stop')


@task
def restart_uwsgi():
    '''
    restarting the uWsgi server
    '''
    execute(stop_uwsgi)
    execute(start_uwsgi)


@task
def collect_static():
    '''
    Copying server static files from project dir to root static dir
    '''
    settings = get_settings_filename()
    config_json = get_config_filename()
    with cd('/home/abotmi/abotmi'):
        with shell_env(ABOTMI_SETTINGS='/home/abotmi/abotmi/config/' + config_json):
            run('/home/abotmi/env/bin/python manage.py collectstatic \
                --settings=reia.' + settings)


@task
def cp():
    '''
    Copying code to server
    '''
    rsync_project(
        remote_dir='/home/abotmi/abotmi/',
        local_dir='.',
        exclude=['.git', '*.pyc', '*.patch', '*.log', '/uploads', '/env']
    )
    config_json = get_config_filename()
    append(
        filename='/home/abotmi/abotmi/webserver/uwsgi/etc/init.d/reia-uwsgi.ini',
        text='env = ABOTMI_SETTINGS=/home/abotmi/abotmi/config/' + config_json,
        use_sudo=True
    )
    setting_name = get_settings_filename()
    sed('/home/abotmi/abotmi/reia/wsgi.py',
        r"\[SETTINGS\]", setting_name, backup='')


@task
def migrate():
    '''
    Migrating the database
    '''
    settings = get_settings_filename()
    config_json = get_config_filename()
    with cd('/home/abotmi/abotmi/'):
        with shell_env(ABOTMI_SETTINGS='/home/abotmi/abotmi/config/' + config_json):
            print '*********** Migrating nfdb database *************'
            run('/home/abotmi/env/bin/python manage.py migrate \
                --settings=reia.' + settings)
            print '*********** Migrating Advisor check database ***********'
            run('/home/abotmi/env/bin/python manage.py migrate \
                --database=advisor_check advisor_check --settings=reia.' + settings)


@task
def deploy():
    '''
    Deploying the code to server
    '''
    execute(check_and_create_environment)
    execute(check_and_create_project_directory)
    execute(change_permisson)
    host_user, host_name = get_host()
    print "************* Copying code into %s *************" % (host_name)
    execute(cp)
    print '************* Copy completed **************'
    execute(install_requirements)
    execute(migrate)
    execute(collect_static)
    execute(restore_permission)
    execute(restart_uwsgi)
