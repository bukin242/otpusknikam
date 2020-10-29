# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.contrib.files import exists
from contextlib import contextmanager
from fabfile import env


env.requirements_file = '{project_dir}/requirements.txt'.format(**env)


def once(s):

    if s not in env.command_prefixes:
        return s
    return 'true'


@contextmanager
def vwrap():

    with prefix(once('source /etc/bash_completion.d/virtualenvwrapper')):
        yield


@contextmanager
def virtualenv():

    with vwrap(), prefix(once('workon {name}'.format(**env))):
        yield


def pipinstall():

    if exists(env.requirements_file):
        with virtualenv(), cd(env.project_dir):
            run('pip install -r {requirements_file}'.format(**env))


def pipupdate():

    with lcd(env.project_dir):

        with virtualenv():
            local('pip freeze > {requirements_file}'.format(**env), shell='/bin/bash')

        local('hg add')
        local('hg ci -m "requirements update" {requirements_file}'.format(**env))
        local('hg push {host}'.format(**env))

    with cd(env.project_dir):
        run('hg up')

    pipinstall()


def piplist():

    with virtualenv():
        run('pip freeze')


def mkvirtualenv():

    if not exists(env.virtualenv_dir):
        with vwrap(), settings(warn_only=True):
            run('mkvirtualenv {name}'.format(**env))


def rmvirtualenv():

    if exists(env.virtualenv_dir):
        with vwrap(), settings(warn_only=True):
            run('rmvirtualenv {name}'.format(**env))
