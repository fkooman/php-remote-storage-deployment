#!/bin/sh
COMMIT=0c788f5f9b2aeb08318c77082f8271723848d18a
VERSION=0.9.11

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
