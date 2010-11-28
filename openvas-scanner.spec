Summary: 	Scanner module for OpenVAS
Name:		openvas-scanner
Version:	3.1.1
Release:	%mkrel 1
Source:		http://wald.intevation.org/frs/download.php/561/%name-%version.tar.gz
Source1:	openvas-scanner.init
Source2:	openvas-scanner.logrotate
Group:		System/Servers
Url:		http://www.openvas.org
License:	GPLv2+
BuildRoot:	%{_tmppath}/%name-%{version}-root
BuildRequires:	openvas-devel >= 3.1.0
Obsoletes:	openvas-plugins < 3.0.0
Obsoletes:	openvas-server < 3.0.0
Provides:	openvas-server = %{version}-%{release}

%description
This is the scanner module for the Open Vulnerability Assessment System
(OpenVAS).

%prep
%setup -q -n %name-%version

%build
%serverbuild
%configure2_5x --disable-static \
	--sharedstatedir=%{_localstatedir}/lib --enable-syslog
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

install -D -m644 %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/openvas-scanner
install -D -m744 %SOURCE1 %{buildroot}%{_initrddir}/openvas-scanner

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Generate cert
if [ ! -f  %{_localstatedir}/lib/openvas/CA/servercert.pem ] ; then
        %{_sbindir}/openvas-mkcert -q > /dev/null 2>&1
fi

%_post_service openvas-scanner

%preun
%_preun_service openvas-scanner

%files
%defattr(-,root,root)
%config %{_sysconfdir}/logrotate.d/openvas-scanner
%{_initrddir}/openvas-scanner
%{_libdir}/openvas/plugins
%{_bindir}/openvas-mkcert-client
%{_sbindir}/openvas-adduser
%{_sbindir}/openvas-mkcert
%{_sbindir}/openvas-rmuser
%{_sbindir}/openvassd
%{_sbindir}/openvas-nvt-sync
%{_sbindir}/greenbone-nvt-sync
%{_mandir}/man1/openvas-mkcert-client.1.*
%{_mandir}/man8/openvas-adduser.8.*
%{_mandir}/man8/openvas-mkcert.8.*
%{_mandir}/man8/openvas-rmuser.8.*
%{_mandir}/man8/openvassd.8.*
%{_mandir}/man8/openvas-nvt-sync.8.*
%{_localstatedir}/cache/openvas
%{_localstatedir}/lib/openvas
%config %dir %{_sysconfdir}/openvas
%dir %{_localstatedir}/log/openvas
