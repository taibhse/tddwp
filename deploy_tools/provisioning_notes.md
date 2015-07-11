Provissioning a new site
========================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Debian as root:
    
    apt-get install nginx git python3 python3-pip
    pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Systemd unit file

* see systemd.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
|__sites
    |--SITENAME
        |--database
        |--source
        |--static
        |--virtualenv
