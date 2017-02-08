#!/bin/sh

#
# Tested on Fedora >= 25
#

###############################################################################
# VARIABLES
###############################################################################

# VARIABLES
HOSTNAME=storage.example

###############################################################################
# SYSTEM
###############################################################################

sudo dnf -y update

###############################################################################
# SOFTWARE
###############################################################################

# enable COPR repos
sudo dnf -y copr enable fkooman/php-remote-storage

# install software
sudo dnf -y install mod_ssl php-cli php-opcache php-fpm httpd openssl \
    php-remote-storage

###############################################################################
# CERTIFICATE
###############################################################################

# Generate the private key
sudo openssl genrsa -out /etc/pki/tls/private/${HOSTNAME}.key 4096 
sudo chmod 600 /etc/pki/tls/private/${HOSTNAME}.key

# Create the CSR (can be used to obtain real certificate!)
sudo openssl req -subj "/CN=${HOSTNAME}" -sha256 -new -key /etc/pki/tls/private/${HOSTNAME}.key -out ${HOSTNAME}.csr

# Create the (self signed) certificate and install it
sudo openssl req -subj "/CN=${HOSTNAME}" -sha256 -new -x509 -key /etc/pki/tls/private/${HOSTNAME}.key -out /etc/pki/tls/certs/${HOSTNAME}.crt

###############################################################################
# APACHE
###############################################################################

# empty the default Apache config file
sudo sh -c 'echo "# emptied by deploy.sh" > /etc/httpd/conf.d/php-remote-storage.conf'

# use the global httpd config file
sudo cp storage.example-httpd.conf /etc/httpd/conf.d/${HOSTNAME}.conf
sudo sed -i "s/storage.example/${HOSTNAME}/" /etc/httpd/conf.d/${HOSTNAME}.conf

###############################################################################
# PHP
###############################################################################

# Set PHP timezone, to suppress errors in the log
sudo sed -i 's/;date.timezone =/date.timezone = UTC/' /etc/php.ini

###############################################################################
# APP
###############################################################################

# Add a user foo with password bar
sudo php-remote-storage-add-user foo bar

###############################################################################
# DAEMONS
###############################################################################

# enable HTTPD and PHP-FPM on boot
sudo systemctl enable httpd
sudo systemctl enable php-fpm

# start HTTPD and PHP-FPM
sudo systemctl restart php-fpm
sudo systemctl restart httpd
