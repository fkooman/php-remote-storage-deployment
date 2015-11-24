#!/bin/sh
COMMIT=4022a0cc65f675e11113cadaca3b6b49a4071fb2
VERSION=1.0.0

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
