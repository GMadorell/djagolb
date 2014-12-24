from __future__ import print_function
import os
from encryptedfiles.encryptedfile import EncryptedFile

from fabric.decorators import task
from fabric.operations import local
from fabric.colors import red, green, blue, yellow

import subprocess


BASE_CONFIG = "src/djagolb/config"
CONFIG_DIRNAME = os.path.join(BASE_CONFIG, "plain")
ENCRYPTED_DIRNAME = os.path.join(BASE_CONFIG, "encrypted")
KEYS_DIR = os.path.join(BASE_CONFIG, "keys")


@task
def encrypt_config():
    cfg_filenames = [f for f in os.listdir(CONFIG_DIRNAME)
                     if os.path.isfile(os.path.join(CONFIG_DIRNAME, f))]

    for filename in cfg_filenames:
        with open(os.path.join(CONFIG_DIRNAME, filename), "r") as cfg_file:
            enc_file = EncryptedFile(os.path.join(ENCRYPTED_DIRNAME, filename),
                                     get_key())
            enc_file.write(cfg_file.read())


def get_key():
    with open(os.path.join(KEYS_DIR, "cfg_key.key"), "r") as cfg_key_file:
        return cfg_key_file.read()

@task
def start():
    # Stop gunicorn if it's running
    if os.path.isfile(os.path.join("gunicorn", "instance.pid")):
        local("bin/gunicornctl stop")
    remove_if_exists(os.path.join("gunicorn", "gunicorn.sock"))

    if not is_nginx_running():
        print(yellow("Trying to restart Nginx before continuing."))
        local("sudo service nginx restart")

    local("supervisord -n")

def is_nginx_running():
    try:
        status = subprocess.check_output("sudo service nginx status", 
                                         stderr=subprocess.STDOUT, 
                                         shell=True)
    except subprocess.CalledProcessError as error:
        status = error.output

    if "is running" in status.lower():
        print(green("Nginx seems to be running."))
        return True
    else:
        print(yellow("Nginx seems to not be running" 
                     "(got status: {}).".format(status.strip("\n"))))
        return False

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path) 