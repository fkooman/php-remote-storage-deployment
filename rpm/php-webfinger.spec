%global composer_vendor         fkooman
%global composer_project        php-webfinger
%global composer_namespace      %{composer_vendor}/WebFinger

%global github_owner            fkooman
%global github_name             php-webfinger
%global github_commit           2192610af18d6e77e1744f94ddc4f892f7a135c6
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-webfinger
Version:    1.0.0
Release:    0.5%{?dist}
Summary:    WebFinger server written in PHP

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   httpd
Requires:   php(language) >= 5.4
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/json) >= 1.0.0
Requires:   php-composer(fkooman/json) < 2.0.0
Requires:   php-composer(symfony/class-loader)

%description
WebFinger server written in PHP.

%prep
%setup -qn %{github_name}-%{github_commit} 
mkdir -p src/%{composer_namespace}
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -r config/conf.d ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%doc README.md CHANGES.md composer.json
%license agpl-3.0.txt

%changelog
* Thu Nov 05 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.5
- update to 2192610af18d6e77e1744f94ddc4f892f7a135c6

* Tue Oct 27 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.4
- update to f3404984d6dcd14bdfad5dc73e32bb43d3807d57

* Tue Oct 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- rebuilt

* Mon Oct 19 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- rebuilt

* Fri Oct 16 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial release
