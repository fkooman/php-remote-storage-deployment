#!/bin/sh
COMMIT=c830eab7c15f30cf750dbe0aa445570b745045c6
VERSION=0.9.10

(
    rm -rf release
    mkdir release
    cd release
    git clone https://github.com/fkooman/php-remote-storage.git php-remote-storage-${VERSION}
    cd php-remote-storage-${VERSION}
    git checkout ${COMMIT}
    rm -rf .git
    composer install --no-dev
    #cp config/server.dev.yaml.example config/server.yaml
    cd ..
    tar -cJf php-remote-storage-${VERSION}.tar.xz php-remote-storage-${VERSION}
    gpg --sign -b -a php-remote-storage-${VERSION}.tar.xz
    remote-storage-uploader --folder php-remote-storage php-remote-storage-${VERSION}.tar.xz
    remote-storage-uploader --folder php-remote-storage php-remote-storage-${VERSION}.tar.xz.asc
)
