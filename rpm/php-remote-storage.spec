%global composer_vendor         fkooman
%global composer_project        php-remote-storage
%global composer_namespace      %{composer_vendor}/RemoteStorage

%global github_owner            fkooman
%global github_name             php-remote-storage
%global github_commit           879b001e6569efb26452722b50ed02d34617f456
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-remote-storage
Version:    1.0.0
Release:    0.16%{?dist}
Summary:    remoteStorage server written in PHP

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

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
BuildRequires:  php-composer(fkooman/http) >= 1.2.0
BuildRequires:  php-composer(fkooman/http) < 2.0.0
BuildRequires:  php-composer(fkooman/config) >= 1.0.0
BuildRequires:  php-composer(fkooman/config) < 2.0.0
BuildRequires:  php-composer(fkooman/io) >= 1.0.0
BuildRequires:  php-composer(fkooman/io) < 2.0.0
BuildRequires:  php-composer(fkooman/json) >= 1.0.0
BuildRequires:  php-composer(fkooman/json) < 2.0.0
BuildRequires:  php-composer(fkooman/oauth) >= 4.0.0
BuildRequires:  php-composer(fkooman/oauth) < 5.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) >= 1.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) < 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) >= 1.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) < 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-form) >= 1.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-form) < 2.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) >= 1.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) < 2.0.0
%endif

Requires:   httpd
Requires:   mod_xsendfile
Requires:   php(language) >= 5.4
Requires:   php-json
Requires:   php-pdo
Requires:   php-spl
Requires:   php-composer(fkooman/http) >= 1.2.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/io) >= 1.0.0
Requires:   php-composer(fkooman/io) < 2.0.0
Requires:   php-composer(fkooman/json) >= 1.0.0
Requires:   php-composer(fkooman/json) < 2.0.0
Requires:   php-composer(fkooman/oauth) >= 4.0.0
Requires:   php-composer(fkooman/oauth) < 5.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 1.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) >= 1.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) >= 1.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) < 2.0.0
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
cp -pr bin/* ${RPM_BUILD_ROOT}%{_bindir}

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/server.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/server.yaml
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
%doc README.md CHANGES.md composer.json config/server.yaml.example
%license agpl-3.0.txt

%changelog
* Thu Nov 12 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.16
- update to 879b001e6569efb26452722b50ed02d34617f456

* Tue Nov 10 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.15
- update to 7638c0cdc13cd59153d8f88868babfd376152cae
- add mod_xsendfile dependency
- depend on fkooman/http >= 1.2.0

* Mon Nov 09 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.14
- update to 7dfa9333f11764383345af5c71f02a30b4a395bc
- config changed to yaml

* Thu Nov 05 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.13
- update to bc9ba1e8a7775c2674197ac22aaa14c41bc332b6

* Tue Nov 03 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.12
- update to a7276b10472c0e02faf2ba30b902b4cf774c1c31

* Tue Nov 03 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.11
- update to 1eba7ca0f71b0cf287eee26cfb35164c1d8c4de7

* Tue Nov 03 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.10
- update to fdaf628312807f40f5f4339730bf6d3cfaffd228

* Mon Nov 02 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.9
- update to 4f5dbdc615f70187b26757f234af3b7ed37cbce6

* Mon Nov 02 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.8
- update to e72cd9f7db94a53acc0218d5eaec9bb0f2726d08

* Wed Oct 28 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.7
- fix semanage requirement

* Tue Oct 27 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.6
- update to 93b38d15c1be4de8cee5b8f1ec60ee7f444210df

* Fri Oct 23 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.5
- update to 699e9af43cad32c59b58c640dedc120f6373bcfd

* Fri Oct 23 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.4
- update to f4b3e2b31815e271611e4bacaf449fd1506da561
- update the dependencies

* Mon Oct 19 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- update to 940acf9449699a344ba83790037dea44bcfab5d1

* Fri Oct 16 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- rebuilt

* Fri Oct 16 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial release
