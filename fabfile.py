from __future__ import print_function
import os
from encryptedfiles.encryptedfile import EncryptedFile
from encryptedfiles.encryptedjson import EncryptedJson

from fabric.decorators import task
from fabric.colors import red, green, blue, yellow
from fabric.api import env, run, local, sudo, put
from fabric.context_managers import cd

import subprocess

import boto
import boto.ec2

from config import Config

from jinja2 import Template


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
    This instance_name has to be the tag "Name" of the ec2 instance
    we want to control.
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



## WEBAPP DEPLOYMENT

@task
def deploy_webapp_run(fresh=True):
    deploy_webapp(fresh)
    run_webapp_container()

@task
def deploy_webapp(fresh=True):
    handle_prerequisites(fresh)
    with cd("djagolb"):
        put("src/djagolb/config/keys/*", "src/djagolb/config/keys/")
        env.run("sudo docker build -t djagolb_appserver_deploy .")
    print(green("Succesfully deployed the djagolb appserver. "
                "Feel free to run 'fab run_webapp_container' ;)."))

def handle_prerequisites(fresh):
    if fresh:
        env.run("sudo yum install git")
        env.run("sudo yum install -y docker ; sudo service docker start")  # https://docs.docker.com/installation/amazon/
    env.run("rm -rf djagolb")
    env.run("git clone https://github.com/Skabed/djagolb djagolb")

@task
def run_webapp_container():
    docker_ps = env.run("sudo docker ps -a")
    if "djagolb_appserver_running" in docker_ps:
        env.run("sudo docker rm -f djagolb_appserver_running")
    env.run("sudo docker run --name djagolb_appserver_running -p 80:80 djagolb_appserver_deploy")

@task
def stop_webapp_container():
    env.run("sudo docker stop djagolb_appserver_running")



## DATABASE DEPLOYMENT

@task
def deploy_db_run(fresh=True):
    deploy_db(fresh)
    run_db_container()

@task
def deploy_db(fresh=True):
    handle_prerequisites(fresh)
    with cd("djagolb"):
        put("src/djagolb/config/keys/*", "src/djagolb/config/keys/")
        env.run("bash init.sh")
        env.run("bin/fab build_db_dockerfile")
    print(green("Succesfully deployed the djagolb database. "
                "Feel free to run 'fab run_db_container' ;)."))

@task
def build_db_dockerfile():
    dockerfile_template = Template(open(".server_config/db/psql_dockerfile.template").read())
    db_settings = get_enc_json("prod_db.json")
    try:
        with open(".server_config/db/psql_dockerfile", "w") as psql_dockerfile:
            psql_dockerfile.write(dockerfile_template.render(
                db_user = db_settings["database"]["USER"],
                db_password = db_settings["database"]["PASSWORD"],
                db_name = db_settings["database"]["NAME"]))
        env.run("sudo docker build -t djagolb_db_deploy - < .server_config/db/psql_dockerfile")
    finally:
        os.remove(".server_config/db/psql_dockerfile")

@task
def run_db_container():
    docker_ps = env.run("sudo docker ps -a")
    if "djagolb_db_running" in docker_ps:
        env.run("sudo docker rm -f djagolb_db_running")
    env.run("sudo docker run --name djagolb_db_running -p 80:80 djagolb_db_deploy")

@task
def stop_db_container():
    env.run("sudo docker stop djagolb_db_running")


####
## Utils
####

BASE_CONFIG = os.path.join("src", "djagolb", "config")
CONFIG_DIRNAME = os.path.join(BASE_CONFIG, "plain")
ENCRYPTED_DIRNAME = os.path.join(BASE_CONFIG, "encrypted")
KEYS_DIR = os.path.join(BASE_CONFIG, "keys")

def get_enc_file(filename):
    return EncryptedFile(os.path.join(ENCRYPTED_DIRNAME, filename), get_key())

def get_enc_json(filename):
    return EncryptedJson(os.path.join(ENCRYPTED_DIRNAME, filename), get_key())

@task
def encrypt_config():
    cfg_filenames = [f for f in os.listdir(CONFIG_DIRNAME)
                     if os.path.isfile(os.path.join(CONFIG_DIRNAME, f))]

    for filename in cfg_filenames:
        if ".gitignore" in filename:
            continue
        with open(os.path.join(CONFIG_DIRNAME, filename), "r") as cfg_file:
            enc_file = EncryptedFile(os.path.join(ENCRYPTED_DIRNAME, filename),
                                     get_key())
            enc_file.write(cfg_file.read())


def get_key():
    with open(os.path.join(KEYS_DIR, "cfg_key.key"), "r") as cfg_key_file:
        return cfg_key_file.read()
