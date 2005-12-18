Summary:	Accessing win32-based databases using TCP/IP protocol
Summary(pl):	Dostêp do baz danych opartych na win32 za pomoc± protoko³u TCP/IP
Name:		odbtp
Version:	1.1.2
Release:	5
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/odbtp/%{name}-%{version}.tar.gz
# Source0-md5:	dc34b6454fe94fe08d3c39dda84cfcc3
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

%prep
%setup -q
%patch0 -p1

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

# make the .so.0, otherwise bad upgrade problems occour
mv $RPM_BUILD_ROOT%{_libdir}/lib{odbtp-1.1.so,odbtp.so.0}
ln -sf libodbtp.so.0 $RPM_BUILD_ROOT%{_libdir}/libodbtp.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.64bitOS docs
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/odbtp.conf
%attr(755,root,root) %{_libdir}/libodbtp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libodbtp.so
%{_libdir}/libodbtp.la
%{_includedir}/odbtp.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libodbtp.a
