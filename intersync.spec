Summary:	InterMezzo filesystem synchronization client
Summary(pl):	Klient do synchronizacji systemów plików InterMezzo
Name:		intersync
Version:	0.9.5
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.inter-mezzo.org/pub/intermezzo/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-aclnoextattr.patch
Patch1:		%{name}-FHS.patch
URL:		http://www.inter-mezzo.org/
BuildRequires:	glib2-devel
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
BuildRequires:	libghttp-devel >= 1.0.9-5
BuildRequires:	pkgconfig
BuildRequires:  e2fsprogs-devel
BuildRequires:  readline-devel
BuildRequires:  curl-devel
Requires(pre):	user-intermezzo
Requires(post,preun):	/sbin/chkconfig
Requires:	apache
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

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/log/intermezzo \
	$RPM_BUILD_ROOT%{_sysconfdir}/intermezzo \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

install sampleconfigs/intersync.conf $RPM_BUILD_ROOT%{_sysconfdir}/intermezzo

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/intersync
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/intersync

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add intersync

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del intersync
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS
%doc doc/*.txt doc/*.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/intermezzo
%attr(754,root,root) /etc/rc.d/init.d/intersync
%attr(640,root,root) /etc/sysconfig/intersync
%dir %{_sysconfdir}/intermezzo
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/intermezzo/intersync.conf
%{_mandir}/man[458]/*
/var/log/intermezzo

# devel?
#%%{_libdir}/lib*.a
#%%{_includedir}/intermezzo
