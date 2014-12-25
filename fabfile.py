from __future__ import print_function
import os
from encryptedfiles.encryptedfile import EncryptedFile

from fabric.decorators import task
from fabric.colors import red, green, blue, yellow
from fabric.api import env, run, local, sudo, put
from fabric.context_managers import cd

import subprocess

import boto
import boto.ec2

from config import Config


####
## AMAZON EC2
####

aws_cfg = Config(open("aws.cfg"))

@task
def localhost():
    env.run = local
    env.hosts = ["localhost"]

@task
def target(instance_name, user="ec2-user"):
    """
    Sets the fab environment to the given instance_name.
    Used like: fab target:django1 *some_other_command*.
    """
    conn = connect_ec2()
    reservations = conn.get_all_instances()
    for res in reservations:
        for inst in res.instances:
            name = inst.tags["Name"]
            if name == instance_name:
                env.hosts = [inst.public_dns_name]
                env.key_filename = os.path.expanduser(os.path.join(
                    aws_cfg["key_dir"], "{}.pem".format(inst.key_name)))
    env.user = user
    env.run = run

def connect_ec2():
    return boto.ec2.connect_to_region(aws_cfg["region"],
            aws_access_key_id=aws_cfg["aws_access_key_id"],
            aws_secret_access_key=aws_cfg["aws_secret_access_key"])

@task
def deploy(fresh=True):
    if fresh:
        env.run("sudo yum install git")
        env.run("sudo yum install -y docker ; sudo service docker start")  # https://docs.docker.com/installation/amazon/
    env.run("rm -rf djagolb")
    env.run("git clone https://github.com/Skabed/djagolb djagolb")
    with cd("djagolb"):
        env.run("mkdir -p src/djagolb/config/keys")
        put("src/djagolb/config/keys", "src/djagolb/config/keys")
        env.run("sudo docker build -t djagolb_appserver_deploy .")
        env.run("sudo docker run -p 80:80 djagolb_appserver_deploy")


####
## Utils
####

BASE_CONFIG = os.path.join("src", "djagolb", "config")
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
