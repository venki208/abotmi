'''
Fabric script for upwrdz application setup
'''
import os

from fabric.api import cd, env, put, run, sudo, task, warn_only
from fabric.tasks import execute
from fabric.contrib.files import sed
from fabric.contrib.project import rsync_project


# ----------------------------------------------
# GLOBAL VARIABLES 
# ----------------------------------------------
repo_folder = os.path.dirname(os.path.abspath(__file__))
webserver = repo_folder + "/webserver"
database  = repo_folder + "/database"

# Global Variables for DB
db_root_user_name = "root"
db_root_user_pass = "root"
db_root_host_name = "localhost"
# NFDB DB 
db_host_name = "localhost"
db_user_name = "nfadmin"
db_user_pass = "nfadmin@123#"
# ADVISOR CHECK DB
advisor_db_host_name = db_host_name
advisor_db_user_name = "advisoradmin"
advisor_db_user_pass = "advisoradmin@123#"

env.reia_root = '/home/northfacing/reia'
env.reia_home = '/home/northfacing'
env.nfdb_root = '/home/northfacing/nfdb'

host_name = ""
domain_name = ""
if len(env.hosts) > 0:
    host_name = env.hosts[0].split('@')[-1]

# set domain name from --set domain_name
if 'domain_name' in env:
    domain_name = env.domain_name
    host_name = domain_name
else:
    domain_name = host_name

# Check Server and Set DB Connection
if host_name == 'upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nf1.6fib"
    db_host_name = "nfprod-db-encypt.cgipueh6acrt.ap-south-1.rds.amazonaws.com" # mumbai RDS with ENC
    db_root_user_name = "nfadmin"
    db_root_user_pass = "nf1.6fib"
    db_root_host_name = db_host_name
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'prod.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "10.1.4.61"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'test.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'dev.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'dev1.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'dev2.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
elif host_name == 'demo.upwrdz.com':
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "nf@vol"
    db_root_host_name = "localhost"
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"
else:
    db_user_name = "nfadmin"
    db_user_pass = "nfadmin@123#"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "root"
    db_root_host_name = db_host_name
    advisor_db_host_name = db_host_name
    advisor_db_user_name = "advisoradmin"
    advisor_db_user_pass = "advisoradmin@123#"

# setup nginx
@task
def nginx():
    run('mkdir -p /tmp/reia')
    put(webserver+'/certs/*', '/tmp/reia')
    run('mkdir -p /tmp/reia/etc/nginx/sites-enabled')
    run('mkdir -p /tmp/reia/etc/nginx/keygroup')
    put(webserver+'/nginx/etc/nginx/sites-enabled/default',
        '/tmp/reia/etc/nginx/sites-enabled/')
    put(webserver+'/nginx/etc/nginx/keygroup/dhsecure.pem',
        '/tmp/reia/etc/nginx/keygroup/')
    sed('/tmp/reia/etc/nginx/sites-enabled/default',
        "\[SERVER_NAME\]", host_name, backup='')
    run('sudo cp -r /tmp/reia/* /')
    run('sudo /etc/init.d/nginx restart')

# setup uwsgi
@task
def uwsgi():
    run('mkdir -p /tmp/reia/etc/init.d')
    put(webserver+'/uwsgi/etc/init.d/reia-uwsgi.ini',
        '/tmp/reia/etc/init.d/')
    put(webserver+'/uwsgi/etc/init.d/reia-uwsgi.sh',
        '/tmp/reia/etc/init.d/', mirror_local_mode=True)
    run('sudo cp -r /tmp/reia/etc/init.d/* /etc/init.d/')
    run('sudo chmod 700 /etc/init.d/reia-uwsgi.sh')


# start uwsgi
@task
def start_uwsgi():
    sudo('/etc/init.d/reia-uwsgi.sh start')


# stop uwsgi
@task
def stop_uwsgi():
    sudo('/etc/init.d/reia-uwsgi.sh stop')


# force stop uwsgi
@task
def force_stop_uwsgi():
    sudo('pkill -9 \"uwsgi\"')


# restart uwsgi
@task
def restart():
    execute(stop_uwsgi)
    execute(start_uwsgi)


# fore restart uwsgi
@task
def force_restart():
    execute(force_stop_uwsgi)
    execute(start_uwsgi)


# sync all reia and nfdb django files
@task
def cp():
    print('copying reia source')
    rsync_project(remote_dir='/home/northfacing/reia', local_dir='.', exclude=['.git','*.pyc','android','iOS', '.log'])
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[SERVER_NAME\]", host_name, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[SERVER_NAME\]", host_name, backup='')
    # SET DB Host Name
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[DB_HOST_NAME\]", db_host_name, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[DB_HOST_NAME\]", db_host_name, backup='')
    # SET DB User Name
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[DB_USER_NAME\]", db_user_name, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[DB_USER_NAME\]", db_user_name, backup='')
    # SET DB User Pass
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[DB_USER_PASS\]", db_user_pass, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[DB_USER_PASS\]", db_user_pass, backup='')
    # SET ADVISOR DB Host Name
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[ADVISOR_DB_HOST_NAME\]", advisor_db_host_name, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[ADVISOR_DB_HOST_NAME\]", advisor_db_host_name, backup='')
    # SET ADVISOR DB User Name
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[ADVISOR_DB_USER_NAME\]", advisor_db_user_name, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[ADVISOR_DB_USER_NAME\]", advisor_db_user_name, backup='')
    # SET ADVISOR DB User Pass
    sed('/home/northfacing/reia/reia/settings-production.py',
        "\[ADVISOR_DB_USER_PASS\]", advisor_db_user_pass, backup='')
    sed('/home/northfacing/reia/reia/settings.py',
        "\[ADVISOR_DB_USER_PASS\]", advisor_db_user_pass, backup='')
    run('mkdir -p /home/northfacing/reia/log')
    run('mkdir -p /home/northfacing/reia/uploads')
    run('mkdir -p /home/northfacing/reia/media/uploads')
    run('mkdir -p /home/northfacing/media/uploads')


# update datacenter app nfdb -> reia
# @task
# def update_datacenter():
#     run("rsync --exclude '*.pyc' -avz \
#         /home/northfacing/nfdb/datacenter/* \
#         /home/northfacing/reia/datacenter/"
#         )
#     run('grep -rl "managed = True"\
#      /home/northfacing/reia/datacenter/models/\
#       | xargs sed -i "s/managed = True/managed = False/g";')


@task
def static():
    with cd(env.reia_root):
        run('/home/northfacing/nfenv/bin/python \
            manage.py collectstatic -v0 --noinput \
            --settings=reia.settings-production '
            )


# first time setup of database
@task
def setupdb():
    run('mkdir -p /tmp/reia')
    put(database+'/nfdb.sql', '/tmp/reia')
    put(database+'/advisor_db.sql', '/tmp/reia')
    run('mysql -h' + db_root_host_name +
        ' -p' + db_root_user_pass + ' -u ' +
        db_root_user_name + ' < /tmp/reia/nfdb.sql'
        )
    run('mysql -h' + db_root_host_name +
        ' -p' + db_root_user_pass + ' -u ' +
        db_root_user_name + ' < /tmp/reia/advisor_db.sql'
        )

# first time after database setup
@task
def initial_migration():
    """
    used to create initial migrations for default database
    """
    with cd(env.reia_root):
        run('/home/northfacing/nfenv/bin/python manage.py makemigrations \
        --settings=reia.settings-production')


@task
def dbsync():
    """
    will run default database migrations 
    """
    with cd(env.reia_root):
        run('/home/northfacing/nfenv/bin/python manage.py migrate --settings=reia.settings-production')

@task
def migrate_advisor_check():
    with cd(env.reia_root):
        run('/home/northfacing/nfenv/bin/python manage.py migrate \
         --settings=reia.settings-production --database=advisor_check advisor_check')

@task
def apply_fixtures():
    with cd(env.reia_root):
        run('find -iname "*.yaml" -exec \
            /home/northfacing/nfenv/bin/python\
             manage.py loaddata {} \;'
            )
    run('mkdir -p /home/northfacing/database')
    put(database+'/pincodes.sql', '/home/northfacing/database')
    put(database+'/pin_code_master.csv', '/home/northfacing/database')
    run('mysql --local-infile -h' + db_host_name +
        ' -p'+db_user_pass+' -unfadmin < \
        /home/northfacing/database/pincodes.sql')


@task
def change_nfgroup():
    '''
    Used to change the deployed code to nfgroup
    '''
    with cd(env.reia_home):
        run('sudo chown -R %s:%s ./nfenv' %(env.user,env.user))
        run('sudo chown -R %s:%s ./reia' %(env.user,env.user))
        run('sudo chown -R %s:%s ./static' %(env.user,env.user))
        run('sudo chown -R %s:%s ./media' %(env.user,env.user))
        run('sudo chown -R %s:%s ./database' %(env.user,env.user))
        run('sudo chown -R %s:%s ./webserver' %(env.user,env.user))
        run('sudo chmod -R 775 ./reia/log/')

@task
def restore_northfacing_owner():
    '''
    Used to change the ownership to northfacing
    '''
    with cd(env.reia_home):
        run('sudo chown -R northfacing:northfacing ./nfenv')
        run('sudo chown -R northfacing:northfacing ./reia')
        run('sudo chown -R northfacing:northfacing ./static')
        run('sudo chown -R northfacing:northfacing ./media')
        run('sudo chown -R northfacing:northfacing ./database')
        run('sudo chown -R northfacing:northfacing ./webserver')
        run('sudo chmod -R 775 ./reia/log/')


# create super user
@task
def create_super_user():
    with cd(env.reia_root):
        run('less cr_superuser.py | \
            /home/northfacing/nfenv/bin/python\
             manage.py shell --settings=reia.settings-production')


# clear all db
@task
def cleardb():
    execute(setupdb)


# clear all code
@task
def clearcode():
    with cd(env.reia_home):
        run('sudo rm -rf ./reia')


# clearn all static riles
@task
def clearstatic():
    with cd(env.reia_home):
        run('sudo rm -rf ./static')


@task
def set_supervisor():
    """set up supervisor"""
    print('copying supervisord configuration file')
    run('mkdir -p /tmp/reia/supervisor')
    put('webserver/supervisor/reia/*', '/tmp/reia/supervisor/')
    sudo('mv /tmp/reia/supervisor/ /etc/')
    sudo('chmod +x /etc/supervisor/*')


@task
def start_supervisor():
    """start supervisor"""
    run('supervisord')
    run('supervisorctl')


@task
def setup_redis():
    '''set up redis'''
    sudo('apt-get install -y redis-server')
    sudo('echo "requirepass redisAdmin" >> /etc/redis/redis.conf')


# set crontab
@task
def set_crontab():
    with cd(env.reia_root):
        run('crontab < cronjobs.txt')

# clear all code and static files
@task
def clear():
    execute(clearcode)
    execute(clearstatic)


# Clears All the code static and db
@task
def clear_all():
    execute(clearcode)
    execute(clearstatic)
    execute(cleardb)

@task
def create_base_folders():
    '''
    create base folders for project
    '''
    run('sudo mkdir -p /home/northfacing/reia/log')
    run('sudo mkdir -p /home/northfacing/reia/uploads')
    run('sudo mkdir -p /home/northfacing/reia/media/uploads')
    run('sudo mkdir -p /home/northfacing/media/uploads')
    run('sudo mkdir -p /home/northfacing/static/uploads')
    run('sudo mkdir -p /home/northfacing/database')
    run('sudo mkdir -p /home/northfacing/webserver')


@task
def start_fail2ban():
    '''Starts service fail2ban'''    
    sudo('service fail2ban start')


@task
def stop_fail2ban():
    '''Stops service fail2ban'''
    sudo('service fail2ban stop')

# needed for first time set up of machine
@task
def setup():
    execute(stop_fail2ban)
    execute(change_nfgroup)
    execute(cp)
    run('/home/northfacing/nfenv/bin/pip install -r \
        /home/northfacing/reia/requirements.txt')
    execute(nginx)
    execute(uwsgi)
    execute(setupdb)
    execute(initial_migration)
    execute(dbsync)
    execute(migrate_advisor_check)
    execute(apply_fixtures)
    execute(static)
    execute(create_super_user)
    execute(start_uwsgi)
    execute(restore_northfacing_owner)
    execute(start_fail2ban)


@task
def deploy():
    '''
    code can be deployed to production or testing servers
    fab reia.deploy -H username@domain_name
    '''
    execute(stop_fail2ban)
    execute(change_nfgroup)
    execute(cp)
    run('/home/northfacing/nfenv/bin/pip install -r \
        /home/northfacing/reia/requirements.txt')
    execute(dbsync)
    execute(migrate_advisor_check)
    execute(static)
    execute(restore_northfacing_owner)
    execute(restart)
    # execute(start_fail2ban)


@task
def prod_deploy():
    '''
    code can be deployed to production or testing servers
    fab reia.deploy -H username@domain_name
    '''
    execute(stop_fail2ban)
    execute(change_nfgroup)
    execute(cp)
    run('/home/northfacing/nfenv/bin/pip install -r \
        /home/northfacing/reia/requirements_production.txt' )
    execute(dbsync)
    execute(migrate_advisor_check)
    execute(static)
    execute(restore_northfacing_owner)
    execute(restart)
    # execute(start_fail2ban)


# for giving build
@task
def clean_deploy():
    execute(stop_fail2ban)
    execute(change_nfgroup)
    execute(uwsgi)
    execute(force_stop_uwsgi)
    execute(clear)
    execute(setupdb)
    execute(cp)
    run('/home/northfacing/nfenv/bin/pip install -r \
        /home/northfacing/reia/requirements.txt')
    execute(initial_migration)
    execute(dbsync)
    execute(migrate_advisor_check)
    execute(apply_fixtures)
    execute(static)
    execute(create_super_user)
    execute(restore_northfacing_owner)
    # execute(start_fail2ban)

@task 
def quick_deploy():
    '''
    Used to copy code and static content and do force restart
    '''
    execute(stop_fail2ban)
    execute(change_nfgroup)
    execute(cp)
    execute(static)
    execute(change_nfgroup)
    execute(restore_northfacing_owner)
    execute(force_restart)
    # execute(start_fail2ban)


@task
def check_domain():
    print "your domain_name is %s" %(domain_name)


@task
def apply_nfdb_dump(file_dir, dump_file_name):
    '''
        dumping nfdb into mysql --> command:fab reia.apply_nfdb_dump:<filepath>,<filename> -H xxxx@xxxx.upwrdz.com
        ex:
        fab reia.apply_nfdb_dump:/home/user/northfacing/rnd/sql/upwrdz_prod/,prod_upwrdz_bak_08_11_2017.sql -H venkatesh@dev.upwrdz.com
    '''
    print 'copying ' + dump_file_name + ' from ', file_dir
    print "==============================================="
    execute(change_nfgroup)
    
    run('mkdir -p /tmp/nfdb_dump')
    
    rsync_project(remote_dir='/tmp/nfdb_dump',
                  local_dir=file_dir+'/'+dump_file_name, exclude=['.git', '*.pyc'])
    print "=============================="
    print "dropping nfdb and recreating"
    run('mysql -h' + db_root_host_name +
        ' -p' + db_root_user_pass + ' -u' +
        db_root_user_name +
        ' < /home/northfacing/reia/database/nfdb.sql'
        )
    print "=============================="
    print "applying dump to nfdb"
    run('mysql -h' + db_root_host_name +
        ' -p' + db_root_user_pass + ' -u' +
        db_root_user_name + ' nfdb< /tmp/nfdb_dump/' + dump_file_name
        )
    print "=============================="
    print "removing file copied file from server"
    run('rm -rf ./tmp/nfdb_dump')
    print "=============================="
    print "migrating the database"
    dbsync()
    print "=============================="
    print "restoring the northfacing owner"
    execute(restore_northfacing_owner)
