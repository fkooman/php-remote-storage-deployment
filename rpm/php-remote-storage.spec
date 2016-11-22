%global composer_vendor         fkooman
%global composer_project        php-remote-storage
%global composer_namespace      %{composer_vendor}/RemoteStorage

%global github_owner            fkooman
%global github_name             php-remote-storage
%global github_commit           75f38945f6b07bbbccb69752d1c8e62db4e66365
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-remote-storage
Version:    1.0.5
Release:    1%{?dist}
Summary:    remoteStorage server written in PHP

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:    %{name}-httpd.conf
Source2:    %{name}-config.yaml

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-json
BuildRequires:  php-pdo
BuildRequires:  php-spl

Requires:   httpd
Requires:   mod_xsendfile

Requires:   php(language) >= 5.4
Requires:   php-json
Requires:   php-pdo
Requires:   php-spl

Requires(post): %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

%description
This is a remoteStorage server implementation written in PHP. It aims at 
implementing draft-dejong-remotestorage-03.txt and higher.

%prep
%setup -q

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/vendor/autoload.php';|" bin/*
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web vendor views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(
cd bin
for f in `ls *`
do
    g=`basename ${f} .php`
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_bindir}/%{name}-${g}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/server.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%check
%{_bindir}/phpunit

%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/%{name} || :

# remove template cache if it is there
rm -rf %{_localstatedir}/lib/%{name}/tpl/* >/dev/null 2>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/server.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/vendor
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md HACKING.md DEVELOPMENT.md SERVER.md composer.json config contrib specification
%license agpl-3.0.txt

%changelog
* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 1.0.5-1
- update to 1.0.5
- run tests unconditionally
- include vendor/ directory in package, dependencies are kind of a mess

* Sun Aug 07 2016 François Kooman <fkooman@tuxed.net> - 1.0.4-1
- update to 1.0.4

* Wed May 25 2016 François Kooman <fkooman@tuxed.net> - 1.0.3-1
- update to 1.0.3

* Thu Mar 31 2016 François Kooman <fkooman@tuxed.net> - 1.0.2-2
- remove the template cache on install/update

* Fri Mar 25 2016 François Kooman <fkooman@tuxed.net> - 1.0.2-1
- update to 1.0.2

* Thu Jan 07 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- COPR is confused about the tar format, hopefully bump will fix this

* Thu Jan 07 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Sat Dec 19 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release
