#!/bin/sh
COMMIT=0fc3b2e2ccd528cbe7d2688a65ae9dc42f5a3abe
VERSION=0.9.5

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
