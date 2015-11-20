#!/bin/sh

#
# This script updates the system by stopping Apache and php-fpm, 
# install all the updates and remove the Twig template cache.
# 
sudo systemctl stop httpd
sudo systemctl stop php-fpm

sudo dnf clean expire-cache
sudo dnf -y update

# clear tpl cache
sudo rm -rf /var/lib/php-remote-storage/tpl

sudo systemctl start php-fpm
sudo systemctl start httpd

