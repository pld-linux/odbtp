%define		php_ver		%(rpm -q --qf '%%{epoch}:%%{version}' php-devel)

Summary:	Accessing win32-based databases using TCP/IP protocol
Summary(pl):	Dostêp do baz danych opartych na win32 za pomoc± protoko³u TCP/IP
Name:		odbtp
Version:	1.1.2
Release:	3
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	dc34b6454fe94fe08d3c39dda84cfcc3
Patch0:		%{name}-php_ext_confpath.patch
Patch1:		%{name}-php_ext_config_m4.patch
URL:		http://odbtp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	php-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ODBTP is a TCP/IP protocol for connecting to Win32-based databases
from any platform. It is ideal for remotely accessing MS SQL Server,
MS Access, and Visual FoxPro database from Linux or Unix machines.
ODBTP is fast, efficient, and has many features that make it a quality
Open Source solution for database connectivity.

%description -l pl
ODBTP to protokó³ TCP/IP s³u¿±cy do ³±czenia siê z dowolnej platformy
z bazami danych opartych na Win32. Idealnie sprawdza siê w zdalnym
dostêpie do baz MS SQL Server, MS Access, czy Visual FoxPro. ODBTP
jest szybki, wydajny oraz posiada wiele innych cech podnosz±cych
jako¶æ.

%package devel
Summary:	Header files for odbtp library
Summary(pl):	Pliki nag³ówkowe biblioteki odbtp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for odbtp library.

%description devel -l pl
Pliki nag³ówkowe biblioteki odbtp.

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
Summary(pl):	Modu³ odbtp (ze wsparciem dla MSSQL) dla PHP
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php = %{php_ver}
Requires(post,preun):	php-common >= 4.1
Obsoletes:	php-pear-%{name}
Obsoletes:	php-pecl-%{name}

%description -n php-%{name}
This is a Dynamic Shared Object (DSO) for PHP that will add odbtp
support. It is built with MSSQL support enabled.

%description -n php-%{name} -l pl
Modu³ PHP umo¿liwiaj±cy korzystanie z biblioteki odbtp. Modu³
zosta³ zbudowany z w³±czonym wsparciem dla MSSQL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{__cc} odbtp.o sockutil.o -o libodbtp.so -shared

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

install -d $RPM_BUILD_ROOT%{_libdir}/php
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install php/ext/%{name}/modules/%{name}.so $RPM_BUILD_ROOT%{_libdir}/php
install examples/odbtp.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n php-%{name}
%{_sbindir}/php-module-install install odbtp %{_sysconfdir}/php/php.ini

%preun -n php-%{name}
if [ "$1" = "0" ]; then
    %{_sbindir}/php-module-install remove odbtp %{_sysconfdir}/php/php.ini
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.64bitOS docs
%attr(755,root,root) %{_libdir}/libodbtp.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/odbtp.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbtp.a

%files -n php-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/php/odbtp.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/odbtp/odbtp.conf
