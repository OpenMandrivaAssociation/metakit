%define name 	metakit
%define version 2.4.9.7
%define release %mkrel 2

%define major 	1
%define libname %mklibname %{name} %{major}
%define soname libmk4.so.1

Summary: 	Embeddable database
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: 	http://www.equi4.com/pub/mk/%{name}-%{version}.tar.gz
Patch0:		metakit-2.4.9.7-flags.patch
Patch1:		metakit-2.4.9.6-alt-soname.patch
URL: 		http://www.equi4.com/metakit/
BuildRequires:	tcl-devel python-devel 

%description
MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %{libname}
Summary: Main library for %{name}, a embeddable database
Group: System/Libraries
Provides: %name = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %{libname}-devel
Summary: Files to compile programs that will use %{name}
Group: Development/C
Requires: %{libname} = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Provides: %libname-devel = %version-%release

%description -n %{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n python-%name
Summary: Python bindings for %name, a embeddable database
Group: System/Libraries
Requires: %libname python
Provides: Mk4py mk4py %name-python
Obsoletes: %name-python

%description -n python-%name
Python bindings for %name

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %name-tcl
Summary: Tcl bindings for %name, a embeddable database
Group: System/Libraries
Requires: %libname tcl
Provides: Mk4tcl mk4tcl

%description -n %name-tcl
Tcl bindings for %name

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.


%prep
%setup -q
%patch0 -p0
%patch1 -p1
rm -rf builds/tests/CVS

%build
cd unix
perl -pi -e "s/^CXXFLAGS.*/CXXFLAGS = $RPM_OPT_FLAGS -fPIC/" Makefile.in
perl -p -i -e "s|python2.3|python%{pyver}||g" configure
cd ../builds
CONFIGURE_TOP="../unix" %configure2_5x --enable-python --with-python=/usr --with-tcl=/usr/include
%make MK4_SONAME=%soname

export LD_LIBRARY_PATH=`pwd`
make test 

%install
rm -rf %buildroot
mkdir -p %buildroot/%py_sitedir
%makeinstall_std -C builds MK4_SONAME=%soname
if [ "%{_prefix}/lib" != "%{_libdir}" ]; then
	mv %buildroot%{_prefix}/lib/Mk4tcl %buildroot%{_libdir}/
fi

%clean
rm -rf %buildroot

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-, root, root)
%doc README
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc README CHANGES doc demos examples 
%{_libdir}/*.so
%{_includedir}/*

%files -n python-%name
%defattr(-, root, root)
%doc README
%py_sitedir/Mk4py.so
%py_sitedir/metakit.py

%files -n %name-tcl
%defattr(-, root, root)
%doc doc/tcl.html doc/tcl.gif doc/e4s.gif
%{_libdir}/Mk4tcl

