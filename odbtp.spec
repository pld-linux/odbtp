Summary:	Accessing win32-based databases using TCP/IP protocol
Summary(pl.UTF-8):	Dostęp do baz danych opartych na win32 za pomocą protokołu TCP/IP
Name:		odbtp
Version:	1.1.4
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/odbtp/%{name}-%{version}.tar.gz
# Source0-md5:	88f0ff518e450643c07fc4f5108144a8
Patch0:		%{name}-libtool.patch
URL:		http://odbtp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.238
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ODBTP is a TCP/IP protocol for connecting to Win32-based databases
from any platform. It is ideal for remotely accessing MS SQL Server,
MS Access, and Visual FoxPro database from Linux or Unix machines.
ODBTP is fast, efficient, and has many features that make it a quality
Open Source solution for database connectivity.

%description -l pl.UTF-8
ODBTP to protokół TCP/IP służący do łączenia się z dowolnej platformy
z bazami danych opartych na Win32. Idealnie sprawdza się w zdalnym
dostępie do baz MS SQL Server, MS Access, czy Visual FoxPro. ODBTP
jest szybki, wydajny oraz posiada wiele innych cech podnoszących
jakość.

%package devel
Summary:	Header files for odbtp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki odbtp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for odbtp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki odbtp.

%package static
Summary:	Static odbtp library
Summary(pl.UTF-8):	Statyczna biblioteka odbtp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static odbtp library.

%description static -l pl.UTF-8
Statyczna biblioteka odbtp.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install examples/odbtp.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.64bitOS docs
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/odbtp.conf
%attr(755,root,root) %{_libdir}/libodbtp.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libodbtp.so
%{_libdir}/libodbtp.la
%{_includedir}/odbtp.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbtp.a
