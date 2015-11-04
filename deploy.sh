#!/bin/sh

# Script to deploy php-remote-storage on a Fedora >= 22 installation using DNF.
#
# Tested on Fedora 23

###############################################################################
# VARIABLES
###############################################################################

# VARIABLES
HOSTNAME=storage.example

###############################################################################
# SYSTEM
###############################################################################

sudo dnf clean all
sudo dnf -y update

# set hostname
sudo hostnamectl set-hostname ${HOSTNAME}

###############################################################################
# SOFTWARE
###############################################################################

# enable COPR repos
sudo dnf -y copr enable fkooman/php-base
sudo dnf -y copr enable fkooman/php-remote-storage

# install software
sudo dnf -y install mod_ssl php php-opcache php-fpm httpd openssl php-remote-storage php-webfinger

###############################################################################
# CERTIFICATE
###############################################################################

# Generate the private key
sudo openssl genrsa -out /etc/pki/tls/private/${HOSTNAME}.key 2048
sudo chmod 600 /etc/pki/tls/private/${HOSTNAME}.key

# Create the CSR (can be used to obtain real certificate!)
sudo openssl req -subj "/CN=${HOSTNAME}" -sha256 -new -key /etc/pki/tls/private/${HOSTNAME}.key -out ${HOSTNAME}.csr

# Create the (self signed) certificate and install it
sudo openssl req -subj "/CN=${HOSTNAME}" -sha256 -new -x509 -key /etc/pki/tls/private/${HOSTNAME}.key -out /etc/pki/tls/certs/${HOSTNAME}.crt

###############################################################################
# APACHE
###############################################################################

# empty the default Apache config file
sudo sh -c 'echo "" > /etc/httpd/conf.d/php-remote-storage.conf'

# use the global httpd config file
sudo cp storage.example-httpd.conf /etc/httpd/conf.d/${HOSTNAME}.conf
sudo sed -i "s/storage.example/${HOSTNAME}/" /etc/httpd/conf.d/${HOSTNAME}.conf

# Don't have Apache advertise all version details
# https://httpd.apache.org/docs/2.4/mod/core.html#ServerTokens
sudo sh -c 'echo "ServerTokens ProductOnly" > /etc/httpd/conf.d/servertokens.conf'

###############################################################################
# PHP
###############################################################################

# Set PHP timezone, to suppress errors in the log
sudo sed -i 's/;date.timezone =/date.timezone = UTC/' /etc/php.ini

#https://secure.php.net/manual/en/ini.core.php#ini.expose-php
sudo sed -i 's/expose_php = On/expose_php = Off/' /etc/php.ini

# recommendation from https://php.net/manual/en/opcache.installation.php
sudo sed -i 's/;opcache.revalidate_freq=2/opcache.revalidate_freq=60/' /etc/php.d/10-opcache.ini

# PHP-FPM configuration
sudo sed -i "s|listen = /run/php-fpm/www.sock|listen = [::]:9000|" /etc/php-fpm.d/www.conf
sudo sed -i "s/listen.allowed_clients = 127.0.0.1/listen.allowed_clients = 127.0.0.1,::1/" /etc/php-fpm.d/www.conf

###############################################################################
# APP
###############################################################################

# enable Twig template cache
sudo sed -i 's/;templateCache/templateCache/' /etc/php-remote-storage/server.ini

# Initialize DB
sudo -u apache php-remote-storage-init

# Create storage directory (XXX can we do this from RPM?)
sudo -u apache mkdir -p /var/lib/php-remote-storage/storage

# Enable WebFinger php-remote-storage snippets
sudo cp /etc/php-webfinger/conf.d/php-remote-storage-05.conf.example /etc/php-webfinger/conf.d/php-remote-storage-05.conf
sudo sed -i 's|/php-remote-storage||' /etc/php-webfinger/conf.d/php-remote-storage-05.conf
sudo cp /etc/php-webfinger/conf.d/php-remote-storage-03.conf.example /etc/php-webfinger/conf.d/php-remote-storage-03.conf
sudo sed -i 's|/php-remote-storage||' /etc/php-webfinger/conf.d/php-remote-storage-03.conf

###############################################################################
# DAEMONS
###############################################################################

# enable HTTPD and PHP-FPM on boot
sudo systemctl enable httpd
sudo systemctl enable php-fpm

# start HTTPD and PHP-FPM
sudo systemctl start php-fpm
sudo systemctl start httpd

# ALL DONE!
