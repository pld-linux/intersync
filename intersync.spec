#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
Summary:	InterMezzo filesystem synchronization client
Summary(pl):	Klient do synchronizacji systemów plików InterMezzo
Name:		intersync
Version:	0.9.5
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.inter-mezzo.org/pub/intermezzo/%{name}-%{version}.tar.gz
# Source0-md5:	63e8c651923a62f92d40df3812cdc03f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-aclnoextattr.patch
Patch1:		%{name}-FHS.patch
URL:		http://www.inter-mezzo.org/
BuildRequires:	curl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
%{?with_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
BuildRequires:	libghttp-devel >= 1.0.9-5
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,preun):	/sbin/chkconfig
Requires:	webserver = apache
Provides:	group(intermezzo)
Provides:	user(intermezzo)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
InterSync is a C based InterMezzo client, intended to operate with an
HTTP server (e.g. TUX or Apache) as a server.

%description -l pl
InterSync to napisany w C klient InterMezzo, maj±cy wspó³pracowaæ z
serwerem HTTP (np. TUX lub Apache) jako serwerem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log/intermezzo,%{_sysconfdir}/intermezzo} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install sampleconfigs/intersync.conf $RPM_BUILD_ROOT%{_sysconfdir}/intermezzo

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/intersync
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/intersync

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 45 -r -f intermezzo
%useradd -g intermezzo -u 45 -d /usr/share/empty -s /bin/false intermezzo

%post
/sbin/chkconfig --add intersync

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del intersync
fi

%postun
if [ "$1" = "0" ]; then
	%userremove intermezzo
	%groupremove intermezzo
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS
%doc doc/*.txt doc/*.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/intermezzo
%attr(754,root,root) /etc/rc.d/init.d/intersync
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/intersync
%dir %{_sysconfdir}/intermezzo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/intermezzo/intersync.conf
%{_mandir}/man[458]/*
/var/log/intermezzo

# devel?
#%%{_libdir}/lib*.a
#%%{_includedir}/intermezzo
