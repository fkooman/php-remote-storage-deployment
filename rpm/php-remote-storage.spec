%global composer_vendor         fkooman
%global composer_project        php-remote-storage
%global composer_namespace      %{composer_vendor}/RemoteStorage

%global github_owner            fkooman
%global github_name             php-remote-storage
%global github_commit           566ffab2317dceb1b8fd8347fa6aa8e8887e61cb
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-remote-storage
Version:    1.0.4
Release:    1%{?dist}
Summary:    remoteStorage server written in PHP

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf
Source3:    %{name}-config.yaml

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-json
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  php-composer(fkooman/http) >= 1.4.0
BuildRequires:  php-composer(fkooman/http) < 2.0.0
BuildRequires:  php-composer(fkooman/config) >= 1.0.0
BuildRequires:  php-composer(fkooman/config) < 2.0.0
BuildRequires:  php-composer(fkooman/io) >= 2.0.0
BuildRequires:  php-composer(fkooman/io) < 3.0.0
BuildRequires:  php-composer(fkooman/json) >= 2.0.0
BuildRequires:  php-composer(fkooman/json) < 3.0.0
BuildRequires:  php-composer(fkooman/oauth) >= 5.0.0
BuildRequires:  php-composer(fkooman/oauth) < 6.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) < 3.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.1.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-form) >= 3.0.1
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-form) < 4.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) >= 1.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) < 2.0.0
%endif

Requires:   httpd
Requires:   mod_xsendfile
Requires:   php(language) >= 5.4
Requires:   php-json
Requires:   php-pdo
Requires:   php-spl
Requires:   php-composer(fkooman/http) >= 1.4.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/io) >= 2.0.0
Requires:   php-composer(fkooman/io) < 3.0.0
Requires:   php-composer(fkooman/json) >= 2.0.0
Requires:   php-composer(fkooman/json) < 3.0.0
Requires:   php-composer(fkooman/oauth) >= 5.0.0
Requires:   php-composer(fkooman/oauth) < 6.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.1.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) >= 3.0.1
Requires:   php-composer(fkooman/rest-plugin-authentication-form) < 4.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.0.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(symfony/class-loader)

Requires(post): %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

%description
This is a remoteStorage server implementation written in PHP. It aims at 
implementing draft-dejong-remotestorage-03.txt and higher.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(
cd bin
for f in `ls *`
do
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_bindir}/%{name}-${f}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/server.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require_once "%{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

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
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md HACKING.md DEVELOPMENT.md SERVER.md composer.json config contrib specification
%license agpl-3.0.txt

%changelog
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
