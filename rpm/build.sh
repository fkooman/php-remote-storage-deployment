#!/bin/sh

rpmdev-wipetree

GITHUB_OWNER=`cat $1.spec | grep "%global github_owner" | awk {'print $3'}`
GITHUB_NAME=`cat $1.spec | grep "%global github_name" | awk {'print $3'}`
GITHUB_COMMIT=`cat $1.spec | grep "%global github_commit" | awk {'print $3'}`
NAME=$1
VERSION=`cat $1.spec | grep "Version:" | cut -d ':' -f 2 | tr -d "[:space:]"`
GITHUB_SHORT=`echo ${GITHUB_COMMIT} | head -c 7`

(
cp $1* ~/rpmbuild/SOURCES/
mv ~/rpmbuild/SOURCES/$1.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild/SOURCES
curl -O -L https://github.com/${GITHUB_OWNER}/${GITHUB_NAME}/archive/${GITHUB_COMMIT}/${NAME}-${VERSION}-${GITHUB_SHORT}.tar.gz
cd ~/rpmbuild/SPECS/
rpmbuild -bs $1.spec
rpmbuild -bb $1.spec
)
