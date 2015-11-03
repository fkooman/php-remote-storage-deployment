# On a server / VM

## Requirements

* [Git](https://www.git-scm.com/downloads)
* Fedora 22+

Clone this repository, run the deploy script

```
git clone git@github.com:fkooman/php-remote-storage-deployment.git && cd php-remote-storage-deployment
./deploy.sh
```

The remotestorage server will be available at on port 443 (self-signed certificate)

# Using Vagrant

## Requirements

* [Git](https://www.git-scm.com/downloads)
* A [recent version of Vagrant](https://www.vagrantup.com/downloads.html) that supports downloading base boxes from
  Vagrant Cloud (1.5+)

Clone this repository, run Vagrant

```
git clone git@github.com:fkooman/php-remote-storage-deployment.git && php-remote-storage-deployment
vagrant up
```

The remotestorage server will be available at [https://localhost:8443/](https://localhost:8443/) from your computer (self-signed certificate)