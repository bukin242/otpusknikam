# -*- coding: utf-8 -*-
import os
from fabric.api import *
from fabric.contrib.project import rsync_project


env.output_prefix = False
env.name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
env.host_string = 'sv4.abukin.ru'
env.port = 2323
env.user = 'abukin'
env.repository_dir = '/home/{user}/crib'.format(**env)
env.project_dir = '/home/{user}/crib/examples/site/{name}'.format(**env)
env.virtualenv_dir = '/home/{user}/.virtualenvs/{name}'.format(**env)
env.host = 'ssh://{user}@{host_string}:{port}/{project_dir}'.format(**env)
env.dump_dir = '/home/{user}/site/dumps'.format(**env)
env.dump_file = '{dump_dir}/{name}.tgz'.format(**env)


try:
    from fabvirtualenvs import *
except ImportError:
    virtualenv = lambda: 'true'


def init():

    if not os.path.exists('.hg'):
        local('hg init')
        local('hg add')
        local('hg ci -m "Start Project"')
        local('hg tip')


def reload():

    with settings(warn_only=True):
        run('sudo service uwsgi reload')


def restart():

    with settings(warn_only=True):
        run('sudo service uwsgi restart')


def install():

    if not exists(env.project_dir):
        run('mkdir {project_dir}'.format(**env))

        with cd(env.project_dir):
            run('hg init')

    mkvirtualenv()
    init()
    local('hg push {host}'.format(**env))

    with cd(env.project_dir):
        run('hg up')

    pipinstall()

    with virtualenv(), cd(env.project_dir):
        run('mkdir -p media static')
        run('./manage.py collectstatic --noinput')
        run('./manage.py migrate')

    restart()
    piplist()


def mediasync():
    rsync_project('{project_dir}/media/'.format(**env), '{project_dir}/media/'.format(**env))


def pull():
    local('hg pull -u {repository_dir}'.format(**env))


def push():

    with settings(warn_only=True):
        local('hg push {repository_dir} --new-branch'.format(**env))


def deploy():

    value = prompt('Commit: ')
    if value:
        local('hg pull -u')
        local('hg addremove')
        local('hg ci -m "%s"' % value)

    push()

    with virtualenv(), cd(env.project_dir):
        run('hg up')
        run('./manage.py collectstatic --noinput')
        run('./manage.py migrate')

    mediasync()
    reload()


def dumpto():

    with lcd(env.dump_dir):
        local('pg_dump {name} -U {name} > {name}.sql'.format(**env))
        local('tar cfz {name}.tgz {name}.sql'.format(**env))
        local('rm {name}.sql'.format(**env))

    rsync_project(env.dump_file, env.dump_file)

    with cd(env.dump_dir):
        run('tar xfz {name}.tgz'.format(**env))
        run('rm {name}.tgz'.format(**env))
        run('sudo service postgresql reload')
        run('sudo -u postgres dropdb {name}'.format(**env))
        run('sudo -u postgres createdb {name} -O {name}'.format(**env))
        run('psql {name} -U {name} < {name}.sql'.format(**env))
        run('rm {name}.sql'.format(**env))


def dumpfrom():

    with cd(env.dump_dir):
        run('pg_dump {name} -U {name} > {name}.sql'.format(**env))
        run('tar cfz {name}.tgz {name}.sql'.format(**env))
        run('rm {name}.sql'.format(**env))

    rsync_project(env.dump_file, env.dump_file, upload=False)

    with lcd(env.dump_dir):
        local('tar xfz {name}.tgz'.format(**env))
        local('rm {name}.tgz'.format(**env))
        local('sudo service postgresql reload')
        local('sudo -u postgres dropdb {name}'.format(**env))
        local('sudo -u postgres createdb {name} -O {name}'.format(**env))
        local('psql {name} -U {name} < {name}.sql'.format(**env))
