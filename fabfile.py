from __future__ import print_function, print_function, unicode_literals


import os
import re
import sys

from contextlib import contextmanager
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from importlib import import_module
from posixpath import join

from fabric.api import abort, env, cd, prefix, sudo as _sudo, run as _run, hide, task, local
from fabric.context_managers import settings as fab_settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.contrib.project import rsync_project
from fabric.colors import yellow, green, blue, red
from fabric.decorators import hosts

from django.conf import settings
 
 
if not hasattr(env, "proj_app"):
    env.proj_app = "study_buddy"
    

##################
# Template setup #
##################

# Each template gets uploaded at deploy time, only if their
# contents has changed, in which case, the reload command is
# also run.


templates = {
    "nginx": {
        "local_path": "deploy/nginx.conf.template",
        "remote_path": "/etc/nginx/sites-enabled/%(proj_name)s.conf",
        "reload_command": "service nginx restart",
    },
    "supervisor": {
        "local_path": "deploy/supervisor.conf.template",
        "remote_path": "/etc/supervisor/conf.d/%(proj_name)s.conf",
        "reload_command": "supervisorctl update gunicorn_%(proj_name)s",
    },
    "cron": {
        "local_path": "deploy/crontab.template",
        "remote_path": "/etc/cron.d/%(proj_name)s",
        "owner": "root",
        "mode": "600",
    },
    "gunicorn": {
        "local_path": "deploy/gunicorn.conf.py.template",
        "remote_path": "%(proj_path)s/gunicorn.conf.py",
    },
    "settings": {
        "local_path": "deploy/local_settings.py.template",
        "remote_path": "%(proj_path)s/%(proj_app)s/local_settings.py",
    },
}

######################################
# Context for virtualenv and project #
######################################

@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    with cd(env.venv_path):
        with prefix("source %s/bin/activate" % env.venv_path):
            yield


@contextmanager
def project():
    """
    Runs commands within the project's directory.
    """
    with virtualenv():
        with cd(env.proj_path):
            yield


def _print(output):
    print()
    print(output)
    print()


def print_command(command):
    _print(blue("$ ", bold=True) +
           yellow(command, bold=True) +
           red(" ->", bold=True))


@task
def run(command, show=True, *args, **kwargs):
    """
    Runs a shell comand on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return fab_run(command, *args, **kwargs)


@task
def sudo(command, show=True, *args, **kwargs):
    """
    Runs a shell command as sudo on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return fab_sudo(command, *args, **kwargs)

@task
def call(command, show=True):
    """
    Runs a command locally.
    """
    if show:
        print_command(command)
    with hide('running'):
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
        print(result)
        return result

@task
def call_venv(command, show=True):
    """
    Runs a command locally through the virtualenv.
    """
    if show:
        print_command(command)
    with hide('running'):
        # venv_command = 'source %s/bin/activate && %s' % (venv_path, command)
        # result = subprocess.Popen(venv_command, shell=True, stdout=subprocess.PIPE).stdout.read()
        with virtualenv():
            result = call(command)
        print(result)
        return result

@task
def execute(task, *args, **kwargs):
    """
    Runs a given task.
    """
    return fab_exexute(task, *args, **kwargs)


    
@task
def python(code, show=True):
    """
    Runs Python code in the project's virtual environment, with Django loaded.
    """
    setup = "import os;" \
            "os.environ[\'DJANGO_SETTINGS_MODULE\']=\'%s.settings\';" \
            "import django;" \
            "django.setup();" % env.proj_app
    full_code = 'python -c "%s%s"' % (setup, code.replace("`", "\\\`"))
    with project():
        if show:
            print_command(code)
        result = run(full_code, show=False)
    return result


def static():
    """
    Returns the live STATIC_ROOT directory.
    """
    return python("from django.conf import settings;"
                  "print(settings.STATIC_ROOT)", show=False).split("\n")[-1]


@task
def manage(command):
    """
    Runs a Django management command.
    """
    return run("%s %s" % (env.manage, command))
    

@task
def apt(packages):
    """
    Installs one or more system packages via apt.
    """
    return sudo("apt-get install -y -q " + packages)


@task
def pip(packages):
    """
    Installs one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return run("pip install %s" % packages)


def postgres(command):
    """
    Runs the given command as the postgres user.
    """
    show = not command.startswith("psql")
    return sudo(command, show=show, user="postgres")


@task
def psql(sql, show=True):
    """
    Runs SQL against the project's database.
    """
    out = postgres('psql -c "%s"' % sql)
    if show:
        print_command(sql)
    return out



@task
def runserver(ip_range='0.0.0.0', port='8080'):
    env.proj_path = settings.ROOT_DIR
    env.venv_path = os.path.join(env.proj_path, '..', 'venv')
    print(env.venv_path)
    