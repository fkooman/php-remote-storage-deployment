# Deployment on VM/Server

We assume you have a clean installation of Fedora 23. We tested it with the
OpenStack image available [here](https://getfedora.org/en/cloud/download/).

    $ curl -L -O https://github.com/fkooman/php-remote-storage-deployment/archive/master.tar.gz
    $ tar -xzf master.tar.gz
    $ cd php-remote-storage-deployment-master

Now you can modify the `deploy.sh` script to change the `HOSTNAME` variable to
your own name of choice, e.g.:

    HOSTNAME=storage.tuxed.net

Now, run the script:

    $ sh deploy.sh

This should set everything up, including a working (self-signed) TLS 
certificate.

## Obtaining a CA Signed Certificate
The script will output a CSR (certificate signing request) in the directory
where you run `deploy.sh` that can be sent to a CA of choice. In this 
example case it would be `storage.tuxed.net.csr`. 

Once you obtain a certificate from your CA you can overwrite 
`/etc/pki/tls/certs/storage.tuxed.net.crt`. Do not forget to also place the 
certificate chain you obtained from the CA in 
`/etc/pki/tls/certs/storage.tuxed.net-chain.crt`, and enable the chain in 
`/etc/httpd/conf.d/storage.tuxed.net.conf`:

    SSLCertificateChainFile /etc/pki/tls/certs/storage.tuxed.net-chain.crt

Now restart Apache and you should be fully up and running!

    $ sudo systemctl restart httpd


# Deployment using Vagrant

## Requirements

* A [recent version of Vagrant](https://www.vagrantup.com/downloads.html) that supports downloading base boxes from
  Vagrant Cloud (1.5+)

Get the content of this repository (or clone it), run Vagrant

    $ curl -L -O https://github.com/fkooman/php-remote-storage-deployment/archive/master.tar.gz
    $ tar -xzf master.tar.gz
    $ cd php-remote-storage-deployment-master
    $ vagrant up

By default `vagrant up` will use the virtualbox provider. 

## Vagrant On Fedora

If you are using Fedora >= 22 on your development system it is also very easy
to use Vagrant to run the software. The default will be the `libvirt` provider.

    $ sudo dnf -y install vagrant vagrant-libvirt
    $ sudo systemctl enable libvirtd
    $ sudo systemctl start libvirtd

Now you can initialize the Vagrant box:

    $ vagrant up
