#!/bin/sh
COMMIT=83c981cbe58a6cb37a227d57476929ac60c5193e
VERSION=1.0.0

(
  rm -rf release
  mkdir release
  cd release
  git clone https://github.com/fkooman/php-remote-storage.git php-remote-storage-${VERSION}
  cd php-remote-storage-${VERSION}
  git checkout ${COMMIT}
  rm -rf .git
  composer install
  cd ..
  tar -cJf php-remote-storage-${VERSION}.tar.xz php-remote-storage-${VERSION}
)
