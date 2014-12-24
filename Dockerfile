

from ubuntu:14.04

run apt-get update -y
run apt-get upgrade -y

run apt-get install -y python \
                       python-dev \
                       python-setuptools \
                       python-software-properties \
                       wget \
                       pandoc \
                       git \
                       vim \
                       
                       sqlite3 \
                       nginx \
                       supervisor


add . /webapps/djagolb/

run cd /webapps/djagolb/ && \
    	bash init.sh && \
    	bin/django syncdb --noinput && \
    	ln -s /webapps/djagolb/.server_config/djagolb_nginx.conf /etc/nginx/sites-enabled/ && \
    	ln -s /webapps/djagolb/.server_config/djagolb_supervisor.conf /etc/supervisor/conf.d/


run rm /etc/nginx/sites-enabled/default
run sudo service nginx restart

expose 80
workdir /webapps/djagolb/
cmd bin/fab start