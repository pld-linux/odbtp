Summary:	Accessing win32-based databases using TCP/IP protocol
Summary(pl):	Dostêp do baz danych opartych na win32 za pomoc± protoko³u TCP/IP
Name:		odbtp
Version:	1.1.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/odbtp/%{name}-%{version}.tar.gz
# Source0-md5:	dc34b6454fe94fe08d3c39dda84cfcc3
URL:		http://odbtp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{__cc} libodbtp.a -o libodbtp.so -shared

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install libodbtp.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
