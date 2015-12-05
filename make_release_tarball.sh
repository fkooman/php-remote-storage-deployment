#!/bin/sh
COMMIT=9222616442ddb6b1a512784901490c85a6e67016
VERSION=0.9.8

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
)
