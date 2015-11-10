#!/bin/sh

GITHUB_OWNER=`cat $1.spec | grep "%global github_owner" | awk {'print $3'}`
GITHUB_NAME=`cat $1.spec | grep "%global github_name" | awk {'print $3'}`
GITHUB_COMMIT=`cat $1.spec | grep "%global github_commit" | awk {'print $3'}`
NAME=$1
VERSION=`cat $1.spec | grep "Version:" | cut -d ':' -f 2 | tr -d "[:space:]"`
GITHUB_SHORT=`echo ${GITHUB_COMMIT} | head -c 7`
RELEASE=`cat $1.spec | grep "Release:" | awk {'print $2'} | cut -d '%' -f 1`

copr-cli build php-remote-storage https://fkooman.fedorapeople.org/${NAME}/${NAME}-${VERSION}-${RELEASE}.fc22.src.rpm
