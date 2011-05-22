Summary: 	Scanner module for OpenVAS
Name:		openvas-scanner
Version:	3.2.3
Release:	%mkrel 1
Source:		http://wald.intevation.org/frs/download.php/561/%name-%version.tar.gz
Source1:	openvas-scanner.initd
Source2:	openvassd.conf
Source3:	openvas-scanner.logrotate
Source4:	openvas-scanner.sysconfig
Source5:	openvas-nvt-sync-cron
Source6:	openvas-nvt-sync-cronjob
Patch0:		openvas-scanner-3.2.2-install.patch
#Put certs to /etc/pki as suggested by http://fedoraproject.org/wiki/PackagingDrafts/Certificates
#Not reported upstream as it is RedHat/Fedora specific
Patch1:		openvas-scanner-pki.patch

#Put openvas-mkcert-client to bin directory instead of sbin and install its man page
#Reported upstream http://wald.intevation.org/tracker/?func=detail&aid=1941&group_id=29&atid=220
Patch2:		openvas-scanner-mkcertclient.patch

#Allow compile time definition of the directory to store openvassd.rules
#Reported upstream http://wald.intevation.org/tracker/?func=detail&aid=1940&group_id=29&atid=220
Patch3:		openvas-scanner-rulesdir.patch

#Fix compile time errors for F15 where variables set but not used are reported as error
#Reported upstream http://wald.intevation.org/tracker/?func=detail&aid=1942&group_id=29&atid=220
Patch4:		openvas-scanner-notused.patch
Group:		System/Servers
Url:		http://www.openvas.org
License:	GPLv2+
BuildRoot:	%{_tmppath}/%name-%{version}-root
BuildRequires:	openvas-devel >= 4.0
BuildRequires:	cmake
Obsoletes:	openvas-plugins < 3.0.0
Obsoletes:	openvas-server < 3.0.0
Requires:	rsync wget curl

%description
This is the scanner module for the Open Vulnerability Assessment System
(OpenVAS).

%prep
%setup -q -n %name-%version
%patch0 -p0 -b .install
%patch1 -p 1 -b .pkipath
%patch3 -p 1 -b .rules
%patch4 -p 1 -b .notused

sed -i -e 's#-Werror##' `grep -rl Werror *|grep CMakeLists.txt`

%build
%serverbuild
%cmake -DLOCALSTATEDIR=%{_var}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C build

#Config directory
mkdir -p %{buildroot}/%{_sysconfdir}/openvas
chmod 755 %{buildroot}/%{_sysconfdir}/openvas

#Make directories for the certificates
mkdir -p %{buildroot}/%{_sysconfdir}/pki/openvas/CA
chmod 755 %{buildroot}/%{_sysconfdir}/pki/openvas
chmod 755 %{buildroot}/%{_sysconfdir}/pki/openvas/CA
mkdir -p %{buildroot}/%{_sysconfdir}/pki/openvas/private/CA
chmod 700 %{buildroot}/%{_sysconfdir}/pki/openvas/private
chmod 700 %{buildroot}/%{_sysconfdir}/pki/openvas/private/CA

# Install startup script
install -Dp -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/openvas-scanner

# Install initial configuration
sed -e "s:@@OPENVAS_PLUGINS@@:%{_var}/lib/openvas/plugins:g
	s:@@OPENVAS_CACHE@@:%{_var}/cache/openvas:g
	s:@@OPENVAS_LOGDIR@@:%{_var}/log/openvas:g
	s:@@OPENVAS_SYSCONF@@:%{_sysconfdir}/openvas:g
	s:@@OPENVAS_CERT@@:%{_sysconfdir}/pki/openvas:g" %{SOURCE2} > openvassd.conf

install -Dp -m 644 openvassd.conf %{buildroot}/%{_sysconfdir}/openvas/

# install log rotation stuff
install -m 644 -Dp %{SOURCE3} \
	%{buildroot}/%{_sysconfdir}/logrotate.d/openvas-scanner

# Install sysconfig configration
install -Dp -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/openvas-scanner

# Install cront script for update
install -Dp -m 755 %{SOURCE5} %{buildroot}/%{_sbindir}/

# Install cront jobs to periodically update plugins
install -Dp -m 644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/cron.d/openvas-sync-plugins

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
%config(noreplace) %{_sysconfdir}/openvas/openvassd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/openvas-scanner
%config(noreplace) %{_sysconfdir}/cron.d/openvas-sync-plugins
%config(noreplace) %{_sysconfdir}/logrotate.d/openvas-scanner
%dir %{_sysconfdir}/openvas
%dir %{_sysconfdir}/pki/openvas
%dir %{_sysconfdir}/pki/openvas/CA
%dir %{_sysconfdir}/pki/openvas/private
%dir %{_sysconfdir}/pki/openvas/private/CA
%{_initrddir}/openvas-scanner
%{_sbindir}/openvas-adduser
%{_sbindir}/openvas-mkcert
%{_sbindir}/openvas-rmuser
%{_sbindir}/openvassd
%{_sbindir}/openvas-nvt-sync
%{_sbindir}/greenbone-nvt-sync
%{_sbindir}/openvas-mkcert-client
%{_sbindir}/openvas-nvt-sync-cron
%{_mandir}/man8/openvas-adduser.8.*
%{_mandir}/man8/openvas-mkcert.8.*
%{_mandir}/man8/openvas-rmuser.8.*
%{_mandir}/man8/openvassd.8.*
%{_mandir}/man8/openvas-nvt-sync.8.*
%{_mandir}/man8/greenbone-nvt-sync.8*
%dir %{_var}/lib/openvas
%dir %{_var}/lib/openvas/plugins
%dir %{_var}/cache/openvas
