Summary: 	Server module for OpenVAS
Name:		openvas-server
Version:	2.0.3
Release:	%mkrel 3
Source:		http://wald.intevation.org/frs/download.php/561/%name-%version.tar.gz
Source1:	openvas-server.init
Source2:	openvas-server.logrotate
Patch0:		openvas-server-2.0.3-fix-str-fmt.patch
Group:		System/Servers
Url:		http://www.openvas.org
License:	GPLv2+
BuildRoot:	%{_tmppath}/%name-%{version}-root
BuildRequires:	openvas-devel >= 2.0
BuildRequires:	openvas-libnasl-devel >= 2.0
Requires:	openvas-plugins

%description
This is the server module for the Open Vulnerability Assessment System
(OpenVAS).

%package devel
Summary:        Headers for developing programs that will use openvas-server
Group:          Development/C

%description devel
This is the server module for the Open Vulnerability Assessment System
(OpenVAS).

%prep
%setup -q -n %name-%version
%patch0 -p0

%build
%serverbuild
%configure2_5x --disable-static \
	--sharedstatedir=%{_localstatedir}/lib --enable-syslog
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

install -D -m644 %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/openvas-server
install -D -m744 %SOURCE1 %{buildroot}%{_initrddir}/openvas-server

%multiarch_binaries %{buildroot}%{_bindir}/openvasd-config

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Generate cert
if [ ! -f  %{_localstatedir}/lib/openvas/CA/servercert.pem ] ; then
        %{_sbindir}/openvas-mkcert -q > /dev/null 2>&1
fi

%_post_service openvas-server

%preun
%_preun_service openvas-server

%files
%defattr(-,root,root)
%config %{_sysconfdir}/logrotate.d/openvas-server
%{_initrddir}/openvas-server
%{_bindir}/openvas-mkcert-client
%{_bindir}/openvas-mkrand
%{_sbindir}/openvas-adduser
%{_sbindir}/openvas-mkcert
%{_sbindir}/openvas-rmuser
%{_sbindir}/openvasd
%{_mandir}/man1/openvas-mkcert-client.1.*
%{_mandir}/man1/openvas-mkrand.1.*
%{_mandir}/man8/openvas-adduser.8.*
%{_mandir}/man8/openvas-mkcert.8.*
%{_mandir}/man8/openvas-rmuser.8.*
%{_mandir}/man8/openvasd.8.*
%{_localstatedir}/cache/openvas
%{_localstatedir}/lib/openvas
%config %dir %{_sysconfdir}/openvas
%dir %{_localstatedir}/log/openvas

%files devel
%defattr(-,root,root)
%{_bindir}/openvasd-config
%multiarch %{multiarch_bindir}/openvasd-config
%{_mandir}/man1/openvasd-config.1.*
%{_includedir}/openvas/*.h
