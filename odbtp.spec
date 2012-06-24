# TODO
# - what about php-pecl-odbtp? one of php-odbtp or php-pecl-odbtp must die
Summary:	Accessing win32-based databases using TCP/IP protocol
Summary(pl):	Dost�p do baz danych opartych na win32 za pomoc� protoko�u TCP/IP
Name:		odbtp
Version:	1.1.2
Release:	3.1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	dc34b6454fe94fe08d3c39dda84cfcc3
Patch0:		%{name}-php_ext_confpath.patch
Patch1:		%{name}-php_ext_config_m4.patch
Patch2:		%{name}-libtool.patch
URL:		http://odbtp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	php-devel
BuildRequires:	rpmbuild(macros) >= 1.238
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ODBTP is a TCP/IP protocol for connecting to Win32-based databases
from any platform. It is ideal for remotely accessing MS SQL Server,
MS Access, and Visual FoxPro database from Linux or Unix machines.
ODBTP is fast, efficient, and has many features that make it a quality
Open Source solution for database connectivity.

%description -l pl
ODBTP to protok� TCP/IP s�u��cy do ��czenia si� z dowolnej platformy
z bazami danych opartych na Win32. Idealnie sprawdza si� w zdalnym
dost�pie do baz MS SQL Server, MS Access, czy Visual FoxPro. ODBTP
jest szybki, wydajny oraz posiada wiele innych cech podnosz�cych
jako��.

%package devel
Summary:	Header files for odbtp library
Summary(pl):	Pliki nag��wkowe biblioteki odbtp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for odbtp library.

%description devel -l pl
Pliki nag��wkowe biblioteki odbtp.

%package static
Summary:	Static odbtp library
Summary(pl):	Statyczna biblioteka odbtp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static odbtp library.

%description static -l pl
Statyczna biblioteka odbtp.

%package -n php-%{name}
Summary:	odbtp extension (with MSSQL support) for PHP
Summary(pl):	Modu� odbtp (ze wsparciem dla MSSQL) dla PHP
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}
Obsoletes:	php-pear-DB_odbtp
Obsoletes:	php-pecl-odbtp

%description -n php-%{name}
This is a Dynamic Shared Object (DSO) for PHP that will add odbtp
support. It is built with MSSQL support enabled.

%description -n php-%{name} -l pl
Modu� PHP umo�liwiaj�cy korzystanie z biblioteki odbtp. Modu�
zosta� zbudowany z w��czonym wsparciem dla MSSQL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

ln -s .libs/libodbtp.so libodbtp.so

# build php extension too (with MSSQL support enabled)
sdir=$(pwd)
cd php/ext/odbtp
phpize
%configure \
        --with-odbtp-mssql=../../../
%{__make}
cd $sdir

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install libodbtp.so $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_sysconfdir}/php/conf.d,%{_libdir}/php}
install php/ext/%{name}/modules/%{name}.so $RPM_BUILD_ROOT%{_libdir}/php
install examples/odbtp.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/php/conf.d/odbtp.ini
; Enable ODBTP extension module
extension=odbtp.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n php-%{name}
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun -n php-%{name}
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.64bitOS docs
%attr(755,root,root) %{_libdir}/libodbtp-*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/odbtp.h
%{_libdir}/libodbtp.so
%{_libdir}/libodbtp.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbtp.a

%files -n php-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/php/odbtp.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php/conf.d/odbtp.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/odbtp/odbtp.conf
