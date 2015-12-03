#!/bin/sh
COMMIT=3e8a190325a457e17a2eeeac389715836873ff88
VERSION=0.9.7

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
